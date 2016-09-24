#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-08-07 22:00:27

import socket
import struct

def ip2int(addr):                                                               
    return struct.unpack("!I", socket.inet_aton(addr))[0]                       

def int2ip(addr):                                                               
    return socket.inet_ntoa(struct.pack("!I", addr))                            


import umsgpack
import functools

def func_cache(f):
    _cache = {}

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        key = umsgpack.packb((args, kwargs))
        if key not in _cache:
            _cache[key] = f(*args, **kwargs)
        return _cache[key]

    return wrapper

def method_cache(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_cache'):
            self._cache = dict()
        key = umsgpack.packb((args, kwargs))
        if key not in self._cache:
            self._cache[key] = fn(self, *args, **kwargs)
        return self._cache[key]

    return wrapper

import datetime

def format_date(date, gmt_offset=-8*60, relative=True, shorter=False, full_format=False):
    """Formats the given date (which should be GMT).

    By default, we return a relative time (e.g., "2 minutes ago"). You
    can return an absolute date string with ``relative=False``.

    You can force a full format date ("July 10, 1980") with
    ``full_format=True``.

    This method is primarily intended for dates in the past.
    For dates in the future, we fall back to full format.
    """
    if not date:
        return '-'
    if isinstance(date, float) or isinstance(date, int):
        date = datetime.datetime.utcfromtimestamp(date)
    now = datetime.datetime.utcnow()
    local_date = date - datetime.timedelta(minutes=gmt_offset)
    local_now = now - datetime.timedelta(minutes=gmt_offset)
    local_yesterday = local_now - datetime.timedelta(hours=24)
    local_tomorrow = local_now + datetime.timedelta(hours=24)
    if date > now:
        later = u"后"
        date, now = now, date
    else:
        later = u"前"
    difference = now - date
    seconds = difference.seconds
    days = difference.days

    format = None
    if not full_format:
        if relative and days == 0:
            if seconds < 50:
                return u"%(seconds)d 秒" % {"seconds": seconds} + later

            if seconds < 50 * 60:
                minutes = round(seconds / 60.0)
                return u"%(minutes)d 分钟" % {"minutes": minutes} + later

            hours = round(seconds / (60.0 * 60))
            return u"%(hours)d 小时" % {"hours": hours} + later

        if days == 0:
            format = "%(time)s"
        elif days == 1 and local_date.day == local_yesterday.day and \
                relative and later == u'前':
            format = u"昨天" if shorter else u"昨天 %(time)s"
        elif days == 1 and local_date.day == local_tomorrow.day and \
                relative and later == u'后':
            format = u"明天" if shorter else u"明天 %(time)s"
        #elif days < 5:
            #format = "%(weekday)s" if shorter else "%(weekday)s %(time)s"
        elif days < 334:  # 11mo, since confusing for same month last year
            format = "%(month_name)s-%(day)s" if shorter else \
                "%(month_name)s-%(day)s %(time)s"

    if format is None:
        format = "%(year)s-%(month_name)s-%(day)s" if shorter else \
            "%(year)s-%(month_name)s-%(day)s %(time)s"

    str_time = "%d:%02d:%02d" % (local_date.hour, local_date.minute, local_date.second)

    return format % {
        "month_name": local_date.month,
        "weekday": local_date.weekday(),
        "day": str(local_date.day),
        "year": str(local_date.year),
        "time": str_time
    }

def utf8(string):
    if isinstance(string, unicode):
        return string.encode('utf8')
    return string

import urllib
import config
from tornado import httpclient
import smtplib
from email.mime.text import MIMEText

def send_mail(to, subject, text=None, html=None, async=False, _from=u"签到提醒 <noreply@mail.qiandao.today>"):
    me = config.mail_user + "<" + config.mail_user + "@" + config.mail_postfix + ">"
    if text:
        msg = MIMEText(utf8(text))
    elif html:
        msg = MIMEText(utf8(html))
    else:
        raise Exception('need text or html')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = utf8(to)
    try:
        s = smtplib.SMTP()
        s.connect(config.mail_host)
        s.login(config.mail_user, config.mail_pass)
        s.sendmail(me, utf8(to), msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

import chardet
from requests.utils import get_encoding_from_headers, get_encodings_from_content


def find_encoding(content, headers=None):
    # content is unicode
    if isinstance(content, unicode):
        return 'unicode'

    encoding = None

    # Try charset from content-type
    if headers:
        encoding = get_encoding_from_headers(headers)
        if encoding == 'ISO-8859-1':
            encoding = None

    # Try charset from content
    if not encoding:
        encoding = get_encodings_from_content(content)
        encoding = encoding and encoding[0] or None

    # Fallback to auto-detected encoding.
    if not encoding and chardet is not None:
        encoding = chardet.detect(content)['encoding']

    if encoding and encoding.lower() == 'gb2312':
        encoding = 'gb18030'

    return encoding or 'latin_1'


def decode(content, headers=None):
    encoding = find_encoding(content, headers)
    if encoding == 'unicode':
        return content

    try:
        return content.decode(encoding, 'replace')
    except Exception as e:
        return None


def quote_chinese(url, encodeing="utf-8"):
    if isinstance(url, unicode):
        return quote_chinese(url.encode("utf-8"))
    res = [b if ord(b) < 128 else '%%%02X' % (ord(b)) for b in url]
    return "".join(res)


import hashlib
md5string = lambda x: hashlib.md5(utf8(x)).hexdigest()

jinja_globals = {
    'md5': md5string,
    'quote_chinese': quote_chinese,
    'utf8': utf8,
}
