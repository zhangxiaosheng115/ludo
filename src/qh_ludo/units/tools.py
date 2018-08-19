# coding=utf-8
from qh_public.money_tool import MoneyTool

from qh_ludo.settings import config


def getLogger(name="root"):
    import logging.config
    from qh_ludo.settings import log_conf
    logging.config.dictConfig(log_conf.LOGGING)
    return logging.getLogger(name=name)


def change_gold(uid, gold):
    """
    游戏开始时扣钱
    :param uid:
    :param gold:
    :return:
    """
    if gold < 0:
        desc = "play ludo cost {}".format(gold)
    else:
        desc = "play ludo win {}".format(gold)

    MoneyTool.change_gold(uid=uid, changed=gold, atype=config.LUDO_GOLD_FLAG, adesc=desc)
