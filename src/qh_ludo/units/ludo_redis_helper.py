# -*- coding:utf-8 -*-
from flask import json

from qh_ludo.settings import config
from qh_ludo.units.redis_tools import ludo_reds


class LudoHelper(object):

    # 管理游戏id
    max_game_id = "ludo_max_id"
    game_str_key = "game_"
    rds = ludo_reds

    @classmethod
    def get_key(cls, game_id):
        return cls.game_str_key + str(game_id)

    @classmethod
    def gen_game_id(cls):
        """
        max游戏id
        :return:
        """
        if not cls.rds.exists(cls.max_game_id):
            cls.rds.set(cls.max_game_id, config.BEGIN_GAME_ID)
            return config.BEGIN_GAME_ID

        return int(cls.rds.incr(cls.max_game_id))

    @classmethod
    def get_game(cls, game_id):
        """
        获取游戏信息
        :param game_id:
        :return: 一个字典
        """
        json_data = cls.rds.get(cls.get_key(game_id))
        return json.loads(json_data)

    @classmethod
    def update_game(cls, game_id, **kwargs):
        data = cls.get_game(game_id)
        if not data:
            return False

        data_dict = json.loads(data)
        data_dict.update(kwargs)
        cls.rds.set(cls.get_key(game_id), data_dict)
        return data_dict

    @classmethod
    def set_game(cls, game_id, **kwargs):
        """
        创建游戏时调用
        :param game_id:
        :param kwargs:
        :return:
        """
        cls.rds.set(cls.get_key(game_id), kwargs)

    @classmethod
    def del_game(cls, game_id):
        """
        删除游戏
        :param game_id:
        :return:
        """
        cls.rds.delete(cls.get_key(game_id))