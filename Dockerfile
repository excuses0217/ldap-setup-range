FROM osixia/openldap:1.5.0

# 复制 LDIF 文件和脚本到镜像中
COPY users.ldif /container/service/slapd/assets/test/users.ldif
COPY acl.ldif /container/service/slapd/assets/test/acl.ldif
COPY bootstrap.sh /container/service/slapd/assets/test/bootstrap.sh

# 设置环境变量，确保脚本在启动时运行
ENV LDAP_ADMIN_PASSWORD=adminpassword
ENV LDAP_ORGANISATION="My Org"
ENV LDAP_DOMAIN=example.com
ENV LDAP_RFC2307BIS_SCHEMA=true

# 调整启动脚本以运行自定义脚本
RUN chmod +x /container/service/slapd/assets/test/bootstrap.sh

