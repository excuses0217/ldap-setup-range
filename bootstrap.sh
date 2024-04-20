#!/bin/bash
set -e

# 等待 OpenLDAP 服务器启动
sleep 15

# 导入用户
ldapadd -x -D "cn=admin,dc=example,dc=com" -w adminpassword -f /container/service/slapd/assets/test/users.ldif

# 给权限
ldapmodify -x -D "cn=admin,cn=config" -w config -f /container/service/slapd/assets/test/acl.ldif
