## 自动签到--树莓派版
1. 修改签到重试间隔时间为1 3 6 min
2. 替换邮件发送为自己邮箱模式
    邮箱配置文件 `config.conf`:  
    ```
    [email]  
    mail_host = smtp.126.com  
    mail_user = xiaoming  
    mail_pass = xxxx  
    mail_postfix = 126.com  
    ```
**注意**
现在网易邮箱需要开启客户端授权码才能发送邮件，否则会出现503错误。
>授权码
 授权码是用于登录第三方邮件客户端的专用密码。
 适用于登录以下服务: POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务。

### 安装
```bash
apt-get install python-dev
virtualenv ./
source ./bin/activate
pip install http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.0.4.zip#md5=3df394d89300db95163f17c843ef49df
pip install tornado u-msgpack-python jinja2 chardet requests mysql-connector-python redis pbkdf2 pycrypto
mysql < qiandao.sql
./worker.py &
./web.py
```

***************

qiandao
=======

签到 —— 一个自动签到框架 base on an HAR editor

HAR editor 使用指南：https://github.com/binux/qiandao/blob/master/docs/har-howto.md

qiandao.py
==========

```
pip install tornado u-msgpack-python jinja2 chardet requests
./qiandao.py tpl.har [--key=value]* [env.json]
```

Web
===

需要 Mysql
可选 redis

```
apt-get install python-dev
pip install http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.0.4.zip#md5=3df394d89300db95163f17c843ef49df
pip install tornado u-msgpack-python jinja2 chardet requests mysql-connector-python redis pbkdf2 pycrypto
mysql < qiandao.sql
./worker.py &
./web.py
```

设置管理员

在数据库中，将用户的 role 改为 admin

鸣谢
====

+[雪月秋水](https://plus.google.com/u/0/+%E9%9B%AA%E6%9C%88%E7%A7%8B%E6%B0%B4%E9%85%B1) [GetCookies项目](https://github.com/acgotaku/GetCookies)

许可
====

MIT
