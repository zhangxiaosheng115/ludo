# -*- coding;utf-8 -*-


from qh_ludo.units.redis_tools import ludo_reds
from qh_ludo.settings import config


class GameSet(object):
    game_set_first = "ludo_set_first"
    game_set_second = "ludo_set_second"
    rds = ludo_reds

    @classmethod
    def get_type(cls, numbers):
        if numbers == config.FOUR_PLAYERS:
            rds_key = cls.game_set_second
        else:
            rds_key = cls.game_set_first

        return rds_key

    @classmethod
    def create(cls, numbers, game_id):
        rds_key = cls.get_type(numbers)
        cls.rds.zadd(rds_key, 1, str(game_id))

    @classmethod
    def update(cls, numbers, game_id, type=1):
        """
        更新人数
        :param type:增加或者减少
        :param numbers:
        :param game_id:
        :return:
        """
        rds_key = cls.get_type(numbers)
        amount = 1 if type == 1 else -1
        current_num = cls.get_game_numbers(numbers, game_id)
        if amount == 1 and current_num >= numbers:
            return False

        return cls.rds.zincrby(rds_key, game_id, amount=amount)

    @classmethod
    def delete(cls, numbers, game_id):
        rds_key = cls.get_type(numbers)
        cls.rds.zrem(rds_key, game_id)

    @classmethod
    def get_game_numbers(cls, numbers, game_id):
        rds_key = cls.get_type(numbers)
        return int(cls.rds.zscore(rds_key, game_id))

    @classmethod
    def get_all_free(cls):
        """
        获取所有人数不足的游戏id
        :return:
        """
        game_list = []
        game_list.append(cls.rds.zrangebyscore(cls.game_set_first, 0, 1))
        game_list.append(cls.rds.zrangebyscore(cls.game_set_second, 0, 3))
        return game_list