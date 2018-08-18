# coding=utf-8

from qh_ludo.web import app
from qh_public.web import set_trans_resources
from qh_ludo.settings import *


if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True)