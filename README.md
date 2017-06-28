# What is DDNS-PYTHON

DDNS(Dynamic DNS) 可以将你变动的 IP 地址同步到你的域名解析网站。

## Notice

* Python = 2.7
* 此脚本仅用于拥有 DNSPOD 的用户。
* 请确保运行脚本的用户对脚本所在文件夹有读写权限。

## How to use ?

1. git clone
2. 配置 `config.ini` 文件
3. `$ python ddns.py`

如果需要将多个子域名指向同一个非静态 IP 的主机上，可以选择将其中一个作为默认子域名并于DDNS-Python关联，而其它的子域名的记录类型设置为CNAME并指向到默认子域名上。

## FEEDBACK

有疑问或发现 bugs，请截图 email(zlyang65@gmail.com), 3X.