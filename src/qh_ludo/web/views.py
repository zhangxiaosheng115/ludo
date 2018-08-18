# coding=utf-8
from qh_public.vld_param import vld_params, Validator
from qh_public.web import check_login

from qh_ludo.settings import config
from . import app
from qh_ludo.apis.ludo_api import LudoApi

@app.route('/ludo/create_game')
@check_login
def create_game():
    """
    uid         -----   创建者
    game_number -----   游戏人数
    type        -----  经典玩法或者快速玩法
    gold        -----  金额
    :return:
    """
    params = vld_params({
        'uid:str': {'default': None, 'rule': Validator.required},
        'numbers':{'default': config.LUDO_MAX_NUM, },
        'type':{'default': config.SPEEDINESS_TYPE, },
        'cost_gold':{'default':config.GOlD_LIST[0], },
    })
    LudoApi.create_game(**params)


@app.route('/ludo/join_game')
@check_login
def join_game():
    """
    uid
    game_id ----- 进入指定的房间
    :return:
    """
    params = vld_params({
        'uid:str': {'default': None, 'rule': Validator.required},
        'game_id:int': {'default':None, 'rule': Validator.required},
    })

    LudoApi.join_game(**params)


@app.route('/ludo/start_game')
@check_login
def start_game():
    """
    开始游戏只有房主才可以
    :return:
    """
    params = vld_params({
        'uid:str': {'default': None, 'rule': Validator.required},
        'game_id:int': {'default': None, 'rule': Validator.required},
    })

    LudoApi.start_game(**params)


@app.route('/ludo/match_game')
@check_login
def match_game():
    """
    匹配模式进入房间---匹配到直接进
    uid
    :return:
    """
    params = vld_params({
        'uid:str': {'default': None, 'rule': Validator.required},
    })

    LudoApi.match_game(**params)


@app.route('/ludo/exit_game')
@check_login
def exit_game():
    """
    uid
    game_id
    :return:
    """
    pass


@app.route('/ludo/throw_dice')
@check_login
def throw_dice():
    """
    uid
    game_id
    :return:
    """
    params = vld_params({
        'uid:str': {'default': None, 'rule': Validator.required},
        'game_id:int': {'default': None, 'rule': Validator.required},
    })

    LudoApi.throw_dice(**params)


@app.route('/ludo/move_plane')
@check_login
def move_plane():
    """
    uid
    step_number
    :return:
    """
    params = vld_params({
        'uid:str': {'default': None, 'rule': Validator.required},
        'game_id:int': {'default': None, 'rule': Validator.required},
        'plane_num:int': {'default':None, 'rule': Validator.required},
    })
    LudoApi.move_plane(**params)


@app.route('/ludo/get_status')
@check_login
def get_status():
    """
    uid
    game_id
    :return:
    """
    params = vld_params({
        'uid:str': {'default': None, 'rule': Validator.required},
        'game_id:int': {'default': None, 'rule': Validator.required},
    })

    LudoApi.get_game_info(**params)
