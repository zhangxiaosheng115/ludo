# -*- coding:utf-8 -*-
from flask import json

from qh_ludo.settings import config
from qh_ludo.units.redis_tools import ludo_reds


class Player(object):
    """
    玩家信息
    """
    player_key = "player_"
    rds = ludo_reds

    @classmethod
    def init(cls, uid, game_id):
        """
        玩家信息初始化
        """
        player_info = dict(
            uid=uid,
            plane_first_steps=config.PLANE_BEGIN_STEP,
            plane_second_steps=config.PLANE_BEGIN_STEP,
            plane_third_steps=config.PLANE_BEGIN_STEP,
            plane_fourth_steps=config.PLANE_BEGIN_STEP,

            # 是否在桌子里, 1----在  0----不在
            in_desk = 1,
            # 座位号
            seat_id=0,
            # 当前扔的色子数值
            current_dice_num=0,
            # 是否托管，默认不托管
            auto_play=config.NOT_AUTO_PLAY,
            # 是否有驱逐敌方飞机
            is_dislodge=config.NOT_DISLODGE,
            # 是否有飞机到达终点
            plane_on_des=config.PLANE_NOT_ON_DES,
            # 历史记录，只记录点数为6的情况,用来判断是否要撤回,结构为飞机和对应移动的步数
            history=list(),
            # 可移动的飞机编号
            can_flys=list(),
        )

        cls.rds.set(cls.get_key(uid, game_id), player_info)

    @classmethod
    def get_key(cls, uid, game_id):
        return cls.player_key + str(uid) + "_" + str(game_id)

    @classmethod
    def get_player_info(cls, uid, game_id):
        return cls.rds.get(cls.get_key(uid, game_id))

    @classmethod
    def update_info(cls, uid, game_id, **kwargs):
        info = cls.get_player_info(uid, game_id)
        if not info:
            return False

        info_dict = json.loads(info)
        info_dict.update(kwargs)
        cls.rds.set(cls.get_key(uid, game_id), info_dict)
        return info_dict

    @classmethod
    def del_info(cls, uid, game_id):
        cls.rds.delete(cls.get_key(uid, game_id))
