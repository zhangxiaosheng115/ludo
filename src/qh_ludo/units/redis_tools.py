# coding=utf-8
import redis

from qh_ludo.settings.evn_conf import redis_6379, redis_6380, redis_6381, redis_6382, redis_6383, redis_6384


configCli = redis.StrictRedis(db=2, **redis_6379)

cam_rds = redis.StrictRedis(db=1, **redis_6382)
rlvl_rds = redis.StrictRedis(db=2, **redis_6382)
room_other_rds = redis.StrictRedis(db=3, **redis_6382)
list_cache_rds = redis.StrictRedis(db=4, **redis_6382)
vip_rds = redis.StrictRedis(db=0, **redis_6382)

rcli = redis.StrictRedis(db=5, **redis_6380)
sub_rds = redis.StrictRedis(db=0, **redis_6380)

en_user_pool_rds = redis.StrictRedis(db=0, **redis_6384)
ar_user_pool_rds = redis.StrictRedis(db=1, **redis_6384)
rec_cache_reds = redis.StrictRedis(db=2, **redis_6384)

ludo_reds = redis.StrictRedis(db=3, **redis_6384)