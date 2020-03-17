FROM mysql:latest
LABEL auth=jackmin1314 maintainer="1416825008@qq.com"
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone
#WORKDIR /app
# 拷贝mysql_spider的初始化数据库和表的脚本
#COPY ./Mysql_Init_Script.sql /app
COPY ./docker/mysql/Mysql_Init_Script.sql /docker-entrypoint-initdb.d/
RUN chmod -R 775 /docker-entrypoint-initdb.d
RUN touch /var/lib/mysql-files
RUN chmod -R 777 /var/lib/mysql-files