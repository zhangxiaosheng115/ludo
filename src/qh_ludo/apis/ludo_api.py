# -*- coding:utf-8 -*-
import json
import random
from qh_public.api import ApiResult, DistributedLock
from qh_public.async import broadcast_message

from qh_ludo.models.mongo_models import Actor
from qh_ludo.settings import errorCode, config
from qh_ludo.units import tools
from qh_ludo.units.game_set import GameSet
from qh_ludo.units.ludo_redis_helper import LudoHelper
from qh_ludo.units.player import Player

log = tools.getLogger("ludo_web")

class LudoApi(object):

    @classmethod
    def create_game(cls, uid, numbers, type, cost_gold):
        """
        创建游戏
        :return:
        """
        result = ApiResult.get_inst()
        actor = Actor.objects(id=uid).first()
        if not actor:
            return result.error(errorCode.CODE_PARAMETER_ERR)

        left_gold = actor.gold
        if left_gold < cost_gold:
            return result.error(errorCode.GOLD_NOT_ENOUGH)

        # 生成game_id
        game_id = LudoHelper.gen_game_id()
        if not game_id:
            return result.error(errorCode.FAIL_GEN_ID)

        game_dict = dict(
            g_room='',
            game_id=game_id,
            uids=[uid],
            max_numbers=numbers,
            gold=cost_gold,
            status=config.LUDO_CREATE,
            current_player="",
            creator=uid,
            winner="",
            win_gold=0,
        )

        # 设置玩家初始信息
        Player.init(uid, game_id)
        # 设置棋桌信息
        LudoHelper.set_game(game_id, **game_dict)
        player_info = Player.get_player_info(uid, game_id)
        player_dict = dict()
        player_dict[uid] = player_info
        log.debug("uid: %s, game_id: %s, player_dict: %s", uid, game_id, player_dict)

        # 在sorted_set中记录
        GameSet.create(numbers, game_id)
        return result.success(data={"game_info":game_dict, "players_info": player_dict})

    @classmethod
    def start_game(cls, uid, game_id):
        """
        开始游戏
        :param uid:
        :param game_id:
        :return:
        """
        result = ApiResult.get_inst()

        game_info = LudoHelper.get_game(game_id)
        if not game_info:
            return result.error(errorCode.CODE_PARAMETER_ERR)

        if uid not in game_info['uids']:
            return result.error(errorCode.CODE_PARAMETER_ERR)

        if game_info['creator'] != uid:
            return result.error(errorCode.CODE_PARAMETER_ERR)

        numbers = game_info['max_numbers']
        if len(game_info['uids']) < numbers:
            return result.error(errorCode.PLAYER_NOT_ENOUGH)

        if game_info['status'] != config.LUDO_READY:
            return result.error(errorCode.PLAYER_NOT_READY)

        update_dict = dict()
        update_dict['status'] = config.LUDO_RUN
        update_dict['current_player'] = uid
        game = LudoHelper.update_game(game_id, **update_dict)

        player_dict = dict()
        for p in game['uids']:
            # todo 看情况是否要进行异步
            tools.change_gold(p, -game_info['gold'])
            player_info = Player.get_player_info(p, game_id)
            player_dict[p] = player_info

        log.debug("uid: %s, game_id: %s, game: %s", uid, game_id, game)
        uid_list = game['uids']
        cls.broadcast_to_uids(uid_list.pop(uid), data={"game_info":game, "players_info": player_dict})
        log.debug("uid: %s, game_id: %s, game_info: %s, player_dict: %s", uid, game_id, game_info, player_dict)
        return result.success(data={"game_info":game, "players_info": player_dict})

    @classmethod
    def throw_dice(cls, uid, game_id):
        """
        扔色子
        :param uid:
        :param game_id:
        :return:
        """
        result = ApiResult.get_inst()
        game_info = LudoHelper.get_game(game_id)

        if uid not in game_info['uids']:
            return result.error(errorCode.CODE_PARAMETER_ERR)

        if uid != game_info['current_player']:
            return result.error(errorCode.CURRENT_PLAYER_ERROR)

        if game_info['status'] != config.LUDO_RUN:
            return result.error(errorCode.CURRENT_PLAYER_ERROR)

        player_info = Player.get_player_info(uid, game_id)
        if not player_info:
            return result.error(errorCode.CURRENT_PLAYER_ERROR)

        dice_num = random.randint(1, 6)
        can_flys = cls.count_flys(dice_num, player_info)

        if not can_flys:
            if dice_num != config.MAX_DICE_NUM:
                next_uid = cls.get_next_uid(uid, game_info)
                game_info = LudoHelper.update_game(game_id, current_player=next_uid)
                Player.update_info(uid, game_id, current_dice_num=dice_num, history=[], can_flys=[])

            else:
                flag = cls.judge_recall(player_info, game_info)
                if flag:
                    cls.recall_player(player_info, game_id)
                    # 变为下一个玩家操作
                    next_uid = cls.get_next_uid(uid, game_info)
                    game_info = LudoHelper.update_game(game_id, current_player=next_uid)
                    Player.update_info(uid, game_id, can_flys=[])

                else:
                    # 客户端根据当前操作者和可以移动的飞机2项判断是扔色子还是移动飞机
                    history = player_info['history'].append({'step':0, 'name':'plane_first_steps'})
                    Player.update_info(uid, game_id, current_dice_num=dice_num, history=history ,can_flys=[])

        else:
            if dice_num == config.MAX_DICE_NUM:
                flag = cls.judge_recall(player_info, game_info)
                if flag:
                    cls.recall_player(player_info, game_id)
                    # 变为下一个玩家操作
                    next_uid = cls.get_next_uid(uid, game_info)
                    game_info = LudoHelper.update_game(game_id, current_player=next_uid)
                    Player.update_info(uid, game_id, history=[], can_flys=[])

                else:
                    Player.update_info(uid, game_id, current_dice_num=dice_num, history=[], can_flys=can_flys)

            else:
                Player.update_info(uid, game_id, current_dice_num=dice_num, history=[], can_flys=can_flys)

        player_dict = dict()
        for p in game_info['uids']:
            player_dict[p] = Player.get_player_info(p, game_id)

        uid_list = game_info['uids']
        cls.broadcast_to_uids(uid_list.pop(uid), data={"game_info":game_info, "players_info": player_dict})
        log.debug("uid: %s, game_id: %s, game_info: %s, player_dict: %s", uid, game_id, game_info, player_dict)
        return result.success(data={"game_info":game_info, "players_info": player_dict})

    @classmethod
    def broadcast(cls, uid, data):
        """
        广播给其他玩家,发送到web_socket
        :return:
        """
        msg_body = {"uid": uid, "topic": "ludo message", "data": data}
        broadcast_message(channel='send_msg_to_ws', msg_body=msg_body)

    @classmethod
    def count_flys(cls, dice_num, player_info):
        """
        计算可移动的飞机
        :param dice_num:
        :param player_info:
        :return:
        """
        log.debug("dice_num: %s, player_info: %s", dice_num, player_info)

        flys_list = list()
        if dice_num == config.MAX_DICE_NUM:
            for n, v in config.PLANE_NAME.items():
                if player_info[v] > 51:
                    continue
                flys_list.append(v)

        else:
            for n, v in config.PLANE_NAME.items():
                if player_info[v] == 0:
                    continue

                if player_info[v] >= 52 and player_info[v] + dice_num != 57:
                    continue
                flys_list.append(v)

        log.debug("count_flys, dice_num: %s, player_info: %s", dice_num, player_info)
        return flys_list

    @classmethod
    def get_next_uid(cls, uid, game_info):
        """
        获取下一个操作的玩家
        :param uid:
        :param game_info:
        :return:
        """
        index = game_info['uids'].index(uid)
        if index == len(game_info['uids']) - 1:
            return game_info['uids'][0]

        else:
            return game_info['uids'][index+1]

    @classmethod
    def judge_recall(cls, player_info, game_info):
        """
        判断是否对玩家进行撤回操作
        :param uid:
        :param game_id:
        :return:
        """
        if len(player_info['history']) == 2:
            return True

        return False

    @classmethod
    def recall_player(cls, player_info, game_id):
        """
        history = [
            {"plane": 1, "step":1, "dice_num":6, "name": "plane_first_steps"},
            {"plane": 1, "step":6, "dice_num":6, "name": "plane_first_steps"},
        ]
        """
        history = player_info['history']
        player_update = dict()

        for s in history[::-1]:
            step = s['step']
            player_update[s['name']] = player_info['plane_first_steps'] - step
            player_update['current_dice_num'] = 0

        player_update['history'] = list()
        log.debug("player_update: %s, player_info: %s, game_id: %s", player_update, player_info, game_id)
        Player.update_info(player_info['uid'], game_id, **player_update)

    @classmethod
    def join_game(cls, uid, game_id):
        result = ApiResult.get_inst()
        actor = Actor.objects(id=uid).first()

        if not actor:
            return result.error(errorCode.CODE_PARAMETER_ERR)

        game_info = LudoHelper.get_game(game_id)
        if actor.gold < game_info['gold']:
            return result.error(errorCode.GOLD_NOT_ENOUGH)

        if game_info['status'] > config.LUDO_READY:
            return result.error(errorCode.GAME_IS_RUNNING)

        if len(game_info['uids']) >= game_info['max_numbers']:
            return result.error(errorCode.REACH_MAX_PLAYER)

        update_dict = dict()
        # 要进行加锁
        with DistributedLock("ludo_game_{}".format(game_id), timeout=1, ex=30, slp=0.1) as lock:
            Player.init(uid, game_id)

            update_dict['uids'] = game_info['uids'].append(uid)
            update_dict['status'] = config.LUDO_READY
            game = LudoHelper.update_game(game_id, **update_dict)

        player_dict = dict()
        for p in game['uids']:
            player_info = Player.get_player_info(p, game_id)
            player_dict[p] = player_info

        log.debug("uid: %s, game_id: %s, game_info: %s, player_dict: %s", uid, game_id, game, player_dict)
        uid_list = game['uids']
        cls.broadcast_to_uids(uid_list.pop(uid), data={"game_info":game, "players_info": player_dict})
        return result.success(data={"game_info":game, "players_info": player_dict})

    @classmethod
    def broadcast_to_uids(cls, uid_list, data):
        for p in uid_list:
            cls.broadcast(p, data=data)

    @classmethod
    def match_game(cls, uid):
        pass

    @classmethod
    def get_game_info(cls, uid, game_id):
        result = ApiResult.get_inst()

        game_info = LudoHelper.get_game(game_id)
        if not game_info:
            return result.success()

        if uid not in game_info['uids']:
            return result.error(errorCode.CODE_PARAMETER_ERR)

        player_dict = dict()
        for p in game_info.uids:
            player_info = Player.get_player_info(p, game_id)
            if not player_info:
                continue

            player_dict[p] = player_info

        log.debug("uid: %s, game_id: %s, game_info: %s, player_dict: %s", uid, game_id, game_info, player_dict)

        return result.success(data={"game_info": game_info, "players_info": player_dict})

    @classmethod
    def move_plane(cls, uid, game_id, plane_num):
        """
        移动飞机
        :param uid:
        :param game_id:
        :param plane_num:移动第几架飞机
        :return:
        """
        result = ApiResult.get_inst()
        game_info = LudoHelper.get_game(game_id)

        if not game_info:
            return result.error(errorCode.CODE_PARAMETER_ERR)

        if uid not in game_info['uids']:
            return result.error(errorCode.CODE_PARAMETER_ERR)

        if game_info['current_player'] != uid:  # 不是当前操作者
            return result.error(errorCode.CURRENT_PLAYER_ERROR)

        if game_info['status'] != config.LUDO_RUN:
            return result.error(errorCode.CURRENT_PLAYER_ERROR)

        player_info = Player.get_player_info(uid, game_id)
        if not player_info:
            return result.error(errorCode.CURRENT_PLAYER_ERROR)

        # 计算移动的步数
        steps = cls.count_steps(plane_num, player_info)
        if not steps:  # 扔色子过程已经计算过有无飞机可以移动
            return result.error(errorCode.PLANE_MOVE_ERROR)

        else:
            dice_num = player_info['current_dice_num']

            update_dict = dict()
            name = config.PLANE_NAME.get(plane_num)
            plane_sum_steps = player_info[name] + steps
            # 判断飞机是否到达终点
            if plane_sum_steps == config.MAX_SUM_STEPS:
                update_dict['plane_on_des'] = config.PLANE_ON_DES

            update_dict[name] = plane_sum_steps
            update_dict['current_dice_num'] = 0

            if dice_num == 6:
                update_dict['history'] = player_info['history'].append({'step':steps, 'name':name})

            # 撞机处理
            location = cls.get_location(player_info['seat_id'], plane_sum_steps)
            flag = cls.strike_handle(location, uid, game_id)
            if flag:
                update_dict['is_dislodge'] = config.SUCCESS_DISLODGE

            p_info = Player.update_info(uid, game_id, **update_dict)

            win = cls.is_win(p_info)
            if win:
                win_gold = cls.settle_accounts(uid, game_info)
                game_info = LudoHelper.update_game(game_id, winner=uid, win_gold=win_gold, status=config.LUDO_END)

            else:
                next_uid = cls.get_next_uid(uid, game_info)
                game_info = LudoHelper.update_game(game_id, current_player=next_uid)

        player_dict = dict()
        for p in game_info['uids']:
            player_dict[p] = Player.get_player_info(uid, game_id)

        log.debug("uid: %s, game_id: %s, player_dict: %s, game_info: %s", uid, game_id, player_dict, game_info)
        uid_list = game_info['uids']
        cls.broadcast_to_uids(uid_list.pop(uid), data={"game_info":game_info, "players_info": player_dict})
        return result.success(data={"game_info":game_info, "players_info": player_dict})

    @classmethod
    def settle_accounts(cls, uid, game_info):
        total_gold = game_info['gold'] * len(game_info['uids'])
        sys_get = int(total_gold * config.SYS_GET)
        tools.change_gold(uid, total_gold-sys_get)
        return total_gold - sys_get

    @classmethod
    def is_win(cls, play_info):
        """
        判断是否胜利
        :param play_info:
        :return:
        """
        if play_info['is_dislodge'] and play_info['plane_on_des']:
            return True
        return False

    @classmethod
    def get_location(cls, seat_id, plane_steps):
        location = config.LOCATION_DICT[seat_id][plane_steps]
        return location

    @classmethod
    def strike_handle(cls, location, uid, game_id):
        """
        判断是否撞机
        :return:
        """
        game_info = LudoHelper.get_game(game_id)
        if not game_info:
            log.error("judge_strike, game not exist !!!!!, game_id: %s", game_id)
            return False

        if location in config.SAFE_PLACE:
            return False

        for p in game_info['uids']:
            if p == uid:
                continue

            player_info = Player.get_player_info(p, game_id)
            location_list = cls.get_user_locations(player_info)
            if location in location_list:
                index = location.index(location)
                update = dict()
                update[config.PLANE_NAME[index+1]] = 0
                Player.update_info(p, game_id, **update)
                break

        return True


    @classmethod
    def get_user_locations(cls, player_info):
        location_list = list()
        if not player_info:
            return location_list

        for name in config.PLANE_NAME_LIST:
            location = cls.get_location(player_info['seat_id'], player_info[name])
            location_list.append(location)

        log.debug("player_info: %s, location_list: %s", player_info, location_list)
        return location_list

    @classmethod
    def count_steps(cls, plane_num, player_info):
        """
        计算移动的步数
        :param plane_num:飞机编号
        :param player_info:玩家信息
        :return:
        """
        name = config.PLANE_NAME.get(plane_num)
        dice_num = player_info['current_dice_num']

        if player_info[name] == 0 and dice_num == 6:
            return 1

        if player_info[name] == 0 and dice_num != 6:
            log.error("count_steps, steps error !!!!, player_info: %s", player_info)
            return 0

        if player_info[name] != 0:
            if player_info[name] + dice_num > config.MAX_SUM_STEPS:
                return 0

            else:
                return dice_num

    @classmethod
    def delete_game(cls, uid, game_id):
        result = ApiResult.get_inst()

        game_info = LudoHelper.get_game(game_id)
        if not game_info:
            return result.error(errorCode.GAME_NOT_EXIST)

        if uid != game_info['creator']:
            return result.error(errorCode.CODE_PARAMETER_ERR)

        if game_info['status'] not in [config.LUDO_CREATE, config.LUDO_END]:
            return result.error(errorCode.CODE_PARAMETER_ERR, msg="can not delete game")

        for p in game_info['uids']:
            Player.del_info(p, game_id)
            if p == uid:
                continue

            cls.broadcast(p, data={'msg': 'The game has been delete'})

        LudoHelper.del_game(game_id)
        GameSet.delete(game_info['max_numbers'], game_id)

        return result.success()
