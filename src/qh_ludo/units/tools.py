# coding=utf-8


def getLogger(name="root"):
    import logging.config
    from qh_ludo.settings import log_conf
    logging.config.dictConfig(log_conf.LOGGING)
    return logging.getLogger(name=name)






