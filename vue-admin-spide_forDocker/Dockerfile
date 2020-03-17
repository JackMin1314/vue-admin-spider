FROM alpine:latest
LABEL auth=jackmin1314  maintainer="1416825008@qq.com"
RUN mkdir -p /app/BackServer/
WORKDIR /app/BackServer
COPY ./BackServer/ .
RUN chmod  -R 777 /app/BackServer/
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g'  /etc/apk/repositories && \
    apk update && \
    apk add python3 py3-pip python3-dev git gcc g++ linux-headers libstdc++ libffi-dev&& \
    apk add uwsgi-python3 tzdata libxml2-dev libxslt-dev openssl-dev && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    pip3 install --index-url=http://mirrors.aliyun.com/pypi/simple/  --trusted-host mirrors.aliyun.com -r requirements.txt && \
    apk del py3-pip python3-dev git tzdata gcc g++ linux-headers && \
    cd / && \
    rm -rf   ~/.cache/pip /var/cache/apk/*
EXPOSE 9999
CMD ["uwsgi", "--ini", "uwsgi.ini"]