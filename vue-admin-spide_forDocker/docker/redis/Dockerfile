FROM    redis:latest
WORKDIR /app/redis/
LABEL   auth=jackmin1314    maintainer="1416825008@qq.com"
RUN rm -rf /etc/redis/redis.conf
RUN mkdir -p   /var/log/redis/
RUN touch   /var/log/redis/redis-server.log
RUN chmod -R 777 /var/log/redis/
RUN chmod 777 /var/log/redis/redis-server.log
COPY ./docker/redis/redis.conf .
EXPOSE  6379
#CMD ["/usr/local/bin/redis-server", "/app/redis/redis.conf"]