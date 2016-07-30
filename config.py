#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-07-30 12:21:48

import hashlib
import ConfigParser
import os

cf = ConfigParser.ConfigParser()
cf.read(os.path.join(os.path.split(os.path.realpath(__file__))[0], "config.conf"))

debug = True
gzip = True
bind = '0.0.0.0'
port = 8923
https = False
cookie_days = 5

class mysql(object):
    host = '192.168.31.183'
    port = '3563'
    database = 'qiandao'
    user = 'qiandao'
    passwd = None

class redis(object):
    host = 'localhost'
    port = 6379
    passwd = None
    db = 1
evil = 100

pbkdf2_iterations = 400
aes_key = hashlib.sha256('binux').digest()
cookie_secret = hashlib.sha256('binux').digest()
check_task_loop = 10000
download_size_limit = 1*1024*1024
proxies = []

mailgun_key = ""
ga_key = ""

# 设置服务器，用户名、口令以及邮箱的后缀
email_section = 'email'

mail_host = cf.get(email_section, 'mail_host')
mail_user = cf.get(email_section, 'mail_user')
mail_pass = cf.get(email_section, 'mail_pass')
mail_postfix = cf.get(email_section, 'mail_postfix')

try:
    from local_config import *
except ImportError:
    pass
