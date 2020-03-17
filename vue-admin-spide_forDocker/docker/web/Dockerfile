FROM nginx:latest
LABEL auth=jackmin1314 maintainer="1416825008@qq.com"
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone
# 移除nginx容器的default.conf文件、nginx配置文件
RUN rm  /etc/nginx/conf.d/default.conf
RUN rm  /etc/nginx/nginx.conf
# 把主机的nginx.conf文件复制到nginx容器的/etc/nginx文件夹下
ADD ./docker/web/nginx.conf /etc/nginx/
# 容器间暴露8080端口.如果是云服务器部署，记得在安全组添加开放端口8080。也可以在docker run -p指定具体的，或者-P默认expose暴露的端口
EXPOSE 8080
# CMD命令用于容器启动时执行，而不像RUN的镜像构建时候运行
# 使用daemon off的方式将nginx运行在前台保证镜像不退出
CMD ["nginx", "-g", "daemon off;"]