#!python
# coding=utf-8


from mongoengine import connect, Document, StringField, IntField, ListField, DictField
from qh_ludo.settings import evn_conf


# connect(host='mongodb://admovie:QI23*&ad@13.232.77.146:27017,13.232.77.146:27018,13.232.77.146:27019/movies',
#         replicaSet='repl1')
connect(host=evn_conf.mongodb_host, replicaSet='repl1')


class Room(Document):
    rid = StringField()
    topic = StringField(default='')
    announce = StringField(default='')
    privi = IntField(default=0)
    fee = IntField(default=0)
    feetype = IntField(default=0)
    online = IntField(default=0)
    owner = IntField(default=0)
    area = IntField(default=0)
    display = IntField(default=0)
    btime = IntField(default=0)  # 房主最近的开播时间
    etime = IntField(default=0)  # 房主下播时间
    mtime = IntField(default=0)  # 房间信息修改时间
    theme = IntField(default=0)  # 房间主题
    memnum = IntField(default=0)  # 房间会员人数
    comp = IntField(default=0)  # 是否为竞赛房

    only_fileds = ['rid', 'topic', 'announce', 'privi', 'fee', 'feetype', 'online', 'owner', 'area', 'display', 'btime',
                   'etime', 'mtime', 'theme', 'memnum', 'comp']
    meta = {'collection': 'room', "strict": False}


class Actor(Document):
    gold = IntField(min_value=0, default=0)
    beans = IntField(min_value=0, default=0)
    room = StringField(default='')
    status = IntField(default=0)
    name = StringField(default='')
    head = StringField(default='')
    banner = ListField(default=[])
    gender = IntField(default=1)
    fb_gender = IntField(default=1)
    age = IntField(default=0)
    country = StringField(default='')
    city = StringField(default='')
    phone = StringField(default='')
    rid = IntField(default=0)
    valid = IntField(default=0)
    display = IntField(default=0)
    viprecord = IntField(default=0)
    login = ListField(default=[])
    uid = StringField(default='')
    login_type = IntField(default=0)
    birthday = StringField(default='')
    accept_talk = IntField(default=0)
    vchat_status = IntField(default=0)
    push = DictField(default={})
    video_option = StringField(default='0')
    area = IntField(default=1)
    lang = StringField(default='en_US')
    imsi = StringField(default='')
    imei = StringField(default='')
    ioskey = StringField(default='')
    android_id = StringField(default='')
    os = StringField(default='0')
    mos = IntField(default=0)
    count = IntField(default=0)
    vnumber = IntField(default=0)
    like = IntField(default=0)
    desc = StringField(default='')
    test = IntField(default=0)
    follow_limit = IntField(default=0)

    meta = {'collection': 'actor', "strict": False}


class Notice(Document):
    aid = StringField()
    mtime = IntField()
    official = DictField(default={})

    meta = {'collection': 'notice', "strict": False}


class Rmember(Document):
    roomId = StringField()
    aid = StringField()
    valid = IntField(default=0)
    utype = IntField(default=1)
    name = StringField(default='')
    rid = IntField()
    rname = StringField(default='')
    rrid = IntField()
    devote = IntField(default=0)
    mtime = IntField()

    meta = {'collection': 'rmember', "strict": False}


class GoldDetail(Document):
    uid = StringField()
    action = IntField(default=0)
    gold = IntField(default=0)
    atype = IntField(default=0)
    desc = StringField(default='')
    begold = IntField(default=0)
    bebeans = IntField(default=0)

    meta = {'collection': 'goldDetail', "strict": False}


class Blacklist(Document):
    uid = StringField()  # 操作用户id
    aid = StringField()  # 被拉黑用户id
    ctime = IntField()  # 创建时间

    meta = {'collection': 'blacklist', "strict": False}


class SysConfig(Document):
    """
    全局配置表
    """
    name = StringField(primary_key=True)  # 主键_id别名
    section = DictField(default={})  # 配置项字典

    meta = {'collection': 'sys_config', "strict": False}


class UserLevel(Document):
    """
    用户等级、经验表
    """
    uid = StringField()
    level = IntField(default=0)
    exp = IntField(default=0)
    last_benefit_level = IntField(default=0)  # 记录上次领取福利的等级，确保只发放一次

    meta = {'collection': 'user_level', "strict": False}


class Badge(Document):
    """用户获得的徽章记录"""
    uid = StringField()
    badge_id = IntField()  # 徽章id
    status = IntField()  # 徽章佩戴状态，0为未佩戴，1-3为佩戴序号
    get_time = IntField()  # 徽章获得时间

    meta = {'collection': 'badge', "strict": False}


class BadgeList(Document):
    """可以获得的徽章列表"""
    badge_id = IntField()  # 徽章id
    name = StringField(default='')  # 徽章名字
    ar_name = StringField(default='')  # 阿拉伯语徽章名
    icon = StringField(default='')  # 图标
    desc = StringField(default='')  # 徽章描述
    ar_desc = StringField(default='')  # 阿拉伯语描述
    valid = IntField(default=0)  # 徽章是否启用
    badge_order = IntField(default=0)  # 徽章排序

    meta = {'collection': 'badge_list', "strict": False}

