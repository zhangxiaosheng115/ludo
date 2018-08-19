# -*- coding -*-

# 游戏最大人数
LUDO_MAX_NUM = 4

# 游戏玩法
CLASSICS_TYPE = 0
SPEEDINESS_TYPE = 1

# 金币配置列表
GOlD_LIST = [100, 1000, 5000, 10000, 50000, 200000, 500000, 1000000]

# 游戏id开始值
BEGIN_GAME_ID = 100000

# 游戏状态
LUDO_CREATE = 0
LUDO_READY = 1
LUDO_RUN = 2
LUDO_END = 3

# 棋盘配置
PLAYER_A_PATH = []

# 飞机的初始步数
PLANE_BEGIN_STEP = 0

# 玩家刚开始走的总步数
SUM_STEPS = 0

# 游戏设置的最大人数
TWO_PLAYERS = 2
FOUR_PLAYERS = 4

# 是否是托管
NOT_AUTO_PLAY = 0
AUTO_PLAY = 1

# 玩家是否有驱逐地方飞机
NOT_DISLODGE = 0
SUCCESS_DISLODGE = 1

# 是否有飞机已经到达终点
PLANE_NOT_ON_DES = 0
PLANE_ON_DES = 1

# 色子的点数为6
MAX_DICE_NUM = 6

# 飞机编号与玩家信息中名称映射
PLANE_NAME = {
    1: "plane_first_steps",
    2: "plane_second_steps",
    3: "plane_third_steps",
    4: "plane_fourth_steps",
}

# 列表
PLANE_NAME_LIST = ['plane_first_steps', 'plane_second_steps', 'plane_third_steps', 'plane_fourth_steps']

# 最大总步数，加上了最后一步的
MAX_SUM_STEPS = 57

# 玩家路线坐标点,每一个数字代表路线上的一个点
FIRST_PLAYER = ['0', 'A13', 'A10', 'A7', 'A4', 'A1', 'D16', 'D13', 'D10', 'D7', 'D4', 'D1', 'D2', 'D3', 'D6', 'D9', 'D12',
                'D15', 'D18', 'C16', 'C13', 'C10', 'C7', 'C4', 'C1', 'C2', 'C3', 'C6', 'C9', 'C12', 'C15', 'C18',
                'B16', 'B13', 'B10', 'B7', 'B4', 'B1', 'B2', 'B3', 'B6', 'B9', 'B12', 'B15', 'B18', 'A3', 'A6', 'A9',
                'A12', 'A15', 'A18', 'A17', 'A14', 'A11', 'A8', 'A5', 'A2', 'A100']

SECOND_PLAYER = ['0', 'B6', 'B9', 'B12', 'B15', 'B18', 'A3', 'A6', 'A9', 'A12', 'A15', 'A18', 'A17', 'A16', 'A13', 'A10',
                 'A7', 'A4', 'A1',  'D13', 'D10', 'D7', 'D4', 'D1', 'D2', 'D3', 'D6', 'D9', 'D12', 'D15', 'D18',
                 'C16', 'C13', 'C10', 'C7', 'C4', 'C1', 'C2', 'C3', 'C6', 'C9', 'C12', 'C15', 'C18', 'B16', 'B13',
                 'B10', 'B7', 'B4', 'B1', 'B2', 'B5', 'B8', 'B11', 'B14', 'B17', 'B100']

THIRD_PLAYER = ['0', 'C6', 'C9', 'C12', 'C15', 'C18', 'B16', 'B13', 'B10', 'B7', 'B4', 'B1', 'B2', 'B3', 'B6', 'B9', 'B12',
                'B15', 'B18', 'A3', 'A6', 'A9', 'A12', 'A15', 'A18', 'A17', 'A16', 'A13', 'A10','A7', 'A4', 'A1',
                'D16', 'D13', 'D10', 'D7', 'D4', 'D1', 'D2', 'D3', 'D6', 'D9', 'D12', 'D15', 'D18', 'C16', 'C13', 'C10',
                'C7', 'C4', 'C1', 'C2', 'C5', 'C8', 'C11', 'C14', 'C17', 'C100']

FOURTH_PLAYER = ['0', 'D6', 'D9', 'D12', 'D15', 'D18', 'C16', 'C13', 'C10', 'C7', 'C4', 'C1', 'C2', 'C3', 'C6', 'C9', 'C12',
                 'C15', 'C18', 'B16', 'B13', 'B10', 'B7', 'B4', 'B1', 'B2', 'B3', 'B6', 'B9', 'B12', 'B15', 'B18',
                 'A3', 'A6', 'A9', 'A12', 'A15', 'A18', 'A17', 'A16', 'A13', 'A10', 'A7', 'A4', 'A1', 'D16', 'D13',
                 'D10', 'D7', 'D4', 'D1', 'D2', 'D5', 'D8', 'D11', 'D14', 'D17']

# 座位号对应的坐标
LOCATION_DICT = {
    1:FIRST_PLAYER,
    2:SECOND_PLAYER,
    3:THIRD_PLAYER,
    4:FOURTH_PLAYER,
}

# 安全区
SAFE_PLACE = ['0', 'A13', 'B6', 'C6', 'D6', 'A12', 'B7', 'C7', 'D7']

# 系统回收比例
SYS_GET = 0.1

# 游戏金币消耗标记码
LUDO_GOLD_FLAG = 512