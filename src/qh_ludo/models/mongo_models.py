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


class GoldDetail(Document):
    uid = StringField()
    action = IntField(default=0)
    gold = IntField(default=0)
    atype = IntField(default=0)
    desc = StringField(default='')
    begold = IntField(default=0)
    bebeans = IntField(default=0)

    meta = {'collection': 'goldDetail', "strict": False}


class SysConfig(Document):
    """
    全局配置表
    """
    name = StringField(primary_key=True)  # 主键_id别名
    section = DictField(default={})  # 配置项字典

    meta = {'collection': 'sys_config', "strict": False}


class LudoRecord(Document):
    """
    计算记录流水
    """
    room_id = StringField(default=0)
    game_id = IntField(default=0)
    uid_list = ListField(default=[])
    winner = StringField(default="")
    win_gold = IntField(default=0)
    sys_get = IntField(default=0)
    ctime = IntField(default=0)

    meta = {'collection': 'ludo_record', "strict": False}