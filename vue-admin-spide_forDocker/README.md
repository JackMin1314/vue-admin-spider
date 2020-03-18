 - [文章目录]()
      - [一、docker安装MySql和Redis并启动](#一docker安装MySql和Redis并启动)
         - [1. docker安装](#1-docker安装)
         - [2. docker启动安装的镜像](#2-docker启动安装的镜像)
         - [3. 查看docker启动镜像的时候所用的命令](#3-查看docker启动镜像的时候所用的命令)
         - [4. 停止和删除镜像容器](#4-停止和删除镜像容器)
         - [5. 登陆和修改、提交镜像](#5-登陆和修改-提交镜像)
      - [二、每个镜像都有资源彼此独立](#二每个镜像都有资源彼此独立)
         - [1. 如何查看docker里面container的ip](#1-如何查看docker里面container的ip)
         - [2. docker创建的容器具有ip的原因和通信方式](#2-docker创建的容器具有ip的原因和通信方式)
         - [3. docker-compose编排容器并启动](#3-docker-compose编排容器并启动)
         - [4. 需要注意mysql和redis的ip修改](#4-需要注意mysql和redis的ip修改)
      - [三、分离部署docker+nginx+uwsgi+mysql+redis](#三分离部署docker+nginx+uwsgi+mysql+redis)
         - [1. 设计图和项目路径](#1-设计图和项目路径)
         - [2. Dockerfile编写](#2-Dockerfile编写)
      - [四、uwsgi和docker爬坑](#四uwsgi和docker爬坑)
         - [1. 报错invalid request block size: xxx...skip](#1-报错invalid-request-block-size:-xxx...skip)
         - [2. 启动出现!!! no internal routing support, rebuild with pcre support !!!](#-2启动出现!!!-no-internal-routing-support-rebuild-with-pcre-support-!!!)
         - [3. uwsgi提示 No such file or directory [core/utils.c line 3654]](#3-uwsgi提示 No such file or directory [core/utils.c line 3654])
         - [4. 提示failed to build: COPY failed: stat /var/lib/docker/tmp:no such file or directory](#4-提示failed-to-build:-COPY-failed:-stat-/var/lib/docker/tmp:no-such-file-or-directory)
         - [5. mysql提示Failed to get stat for directory pointed out by --secure-file-priv](#5-mysql提示Failed-to-get-stat-for-directory pointed-out-by---secure-file-priv)
         - [6. Supplied value : /var/lib/mysql-files](#6-Supplied-value-:-/var/lib/mysql-files)
       - [五、项目展示和项目地址](#五-项目展示和项目地址) 
           - [1. docker-compose编排成功后的截图](#1-docker-compose编排成功后的截图)
           - [2. 项目界面的截图](#2-项目界面的截图)
           - [3.写在最后](#3-写在最后)


       

今天给大家带来前后端分离项目下的docker的部署和启动，到最终的打包提交到dockerhub，以及爬坑记录。旨在解决同道小伙伴们的痛点。
​刚学习docker，不足之处望请谅解，虚心接受大神指点，转注出，诚谢~ 文末附项目效果展示和源码地址。
## 一、docker安装MySql和Redis并启动

官网命令传送门==>[docker命令](https://docs.docker.com/engine/reference/commandline/docker/)
### 1. docker安装

* 查询有哪些镜像
```
$ docker search mysql
```

* 安装指定的镜像(在此之前请先配制好镜像加速)

```
$ docker pull mysql:8.0.18
```

* 安装默认最新镜像
```
$ docker pull mysql
# 或docker pull mysql:latest
```
同理安装Redis

### 2. docker启动安装的镜像

* 查询本地安装了的镜像

```
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
mysql               latest              9b51d9275906        8 days ago          547MB
redis               latest              7eed8df88d3b        2 weeks ago         98.2MB
```

* 启动Mysql

```
# 将docker的mysql镜像以守护进程的方式创建实例mysql-demo(容器)
# 该实例的端口为3306对应的宿主机上的12345，初始化的数据库密码为5201020116.
# 也可以将宿主机的数据库的配置挂载到mysql-demo对应的位置
$ docker run -p 12345:3306 --name mysql-demo -e MYSQL_ROOT_PASSWORD=5201020116 -d mysql
```

因为我的mysql的宿主机环境已经安装了，所以宿主机端口不能在用3306，改为了12345。

* 启动Redis

```
# 默认redis容器里是没有配置文件的(可在容器的/etc/查看redis.conf不存在)，因而需要在创建容器时映射进来
# 设置密码直接使用--requirepass "你的密码"即可
# -i表示以交互模式运行容器，-t表示重新分配伪终端, -d以守护进程方式运行; -v 表示映射文件；-p端口映射
$ docker run -itd --name redis-demo -v /etc/redis/redis.conf:/etc/redis.conf -p 9909:6379
 --restart=always redis:latest redis-server --appendonly yes --requirepass "5201020116"
# 查看刚创建的容器的信息(截取部分)
$ docker ps -l
CONTAINER ID      IMAGE      CREATED     STATUS             PORTS                    NAMES
a83ef0e487e7   redis:latest  4 minutes ago   Up 4 minutes   0.0.0.0:9909->6379/tcp   redis-demo
# 再次进入这个容器
$ docker exec -it a83ef0e487e7 /bin/bash
# 验证是否成功
root@a83ef0e487e7:/data# redis-cli
127.0.0.1:6379> auth 5201020116
OK
127.0.0.1:6379>
```

安装启动nginx同理。

### 3. 查看docker启动镜像的时候所用的命令

```
$ docker ps -a --no-trunc
```

### 4. 停止和删除镜像容器

```
# 查看所有的容器
$ docker ps -a
# 停止/重启/删除容器 （已运行需要先停止再删除）
$ docker container stop/restart/rm  a83ef0e487e7#容器ID
# 直接强制删除
$ docker rm -f a83e#容器ID
# #删除镜像image，删除前需要保证没有container引用这个镜像
$ docker rmi 9b51d9275906	#镜像id
# 删除所有镜像
$ docker rmi $(docker images -q)
# 删除所有没有标签的镜像
$ docker rmi $(docker images -q | awk '/^<none>/ { print $3 }')
```

### 5.  登陆和修改、提交镜像

````
# 登录dockerhub
$ docker login -u jackmin1314	# 你的dockerhub账户名
# 提交前切记修改镜像为 账户名/镜像名:tag
$ docker tag fe2880e71109 jackmin1314/spider_flask:latest
# 提交镜像到本地
$ docker commit -a "jackmin1314 <1416@qq.com>" -m "this is test" 5bca95es95 myubuntu:v1
# 提交到远程dockerhub上面
$ docker push jackmin1314/spider_flask:latest
The push refers to repository [docker.io/jackmin1314/spider_redis]
a64d7a130512: Pushed
0554f8c96c61: Pushed
493605b7d1c9: Pushed
c742d444d284: Pushed
5216338b40a7: Mounted from library/alpine
latest: digest: sha256:0554f8c96c61....ea3c01 size: 1777
````
## 二、每个镜像都有资源，彼此独立

### 1. 如何查看docker里面container的ip

```
$ docker inspect --format '{{ .NetworkSettings.IPAddress }}' 053e4f11df7a
```

因而想要让docker内部容器间访问就需要通过ip来实现。例如后端python项目和mysql交互。

### 2.  docker创建的容器具有ip的原因

>* ​宿主机在安装docker后，docker会在宿主机上生成一张docker虚拟网卡，docker网卡通过NAT的方式为每一个容器分配ip，容器同处于docker网段下，因而容器间通信，可以通过ip。
> * 而容器和宿主机器通信，则是通过docker虚拟网卡进行转发路由。
> * 镜像创建了容器后，容器名会对应容器ip(在该容器的host有映射)，因而可以通过容器名执行相关操作.

如下示意图 ：![container-ip.png](https://upload-images.jianshu.io/upload_images/13876087-d01e023e5340f5ff.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
## 三、前后端分离部署(docker+nginx+uwsgi+mysql+redis)

### 1. 设计图和项目路径

**docker** 的设计示意图.(其中nginx的反向代理协议用的是wsgi，添加了`include uwsgi_params; `，用了`uwsgi_pass`因为后台服务器用uwsgi；正常情况使用`proxy_pass`即可)
![docker-Architecture.png](https://upload-images.jianshu.io/upload_images/13876087-18089ba3179ff96c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
**项目文件** 简易说明

> + BackServer/ ----后端源码项 目
> + vue_admin/ ---- 前端项目
> + dist/ ---- 打包后线上部署的文件
> + docker/ ---- mysql、redis、nginx的配置和dockerfile
> + Dockerfile ---- BackServer托管uwsgi服务器的dockerfile

项目文件说明图：![project_trees.png](https://upload-images.jianshu.io/upload_images/13876087-f3bdb19a5a8b3429.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
### 2. Dockerfile编写

给出各个container的dockerfile,仅供参考。

+ nginx的dockerfile

  ``` dockerfile
  FROM nginx:latest
  LABEL  auth=jackmin1314 	maintainer="1416825008@qq.com"
  RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
      echo "Asia/Shanghai" > /etc/timezone
  # 移除nginx容器的default.conf文件、nginx配置文件
  RUN rm  /etc/nginx/conf.d/default.conf
  RUN rm  /etc/nginx/nginx.conf
  # 把主机的nginx.conf文件复制到nginx容器的/etc/nginx文件夹下
  ADD ./docker/web/nginx.conf /etc/nginx/
  # 容器间暴露8080端口.如果是云服务器部署，记得在安全组添加开放端口8080。
  # 也可以在docker run -p指定具体的，或者-P默认expose暴露的端口
  EXPOSE 8080
  # CMD命令用于容器启动时执行，而不像RUN的镜像构建时候运行
  # 使用daemon off的方式将nginx运行在前台保证镜像不退出
  CMD ["nginx", "-g", "daemon off;"]
  ```

+ redis的dockerfile

  ``` dockerfile
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
  ```

+ mysql的dockerfile

  ``` dockerfile
  FROM mysql:latest
  LABEL 	auth=jackmin1314	maintainer="1416825008@qq.com"
  RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
      echo "Asia/Shanghai" > /etc/timezone
  #WORKDIR /app
  # 拷贝mysql_spider的初始化数据库和表的脚本
  #COPY ./Mysql_Init_Script.sql /app
  COPY ./docker/mysql/Mysql_Init_Script.sql /docker-entrypoint-initdb.d/
  RUN chmod -R 775 /docker-entrypoint-initdb.d
  RUN touch /var/lib/mysql-files
  RUN chmod -R 777 /var/lib/mysql-files
  ```

+ uwsgi的dockerfile

  ``` dockerfile
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
  ```

### 3. docker-compose编排容器并启动

docker-compose.yml编写启动的顺序(依赖关系)要注意 参考`redis -> mysql -> uwsgi -> nginx`。例外，一旦指定了compose的某个service的上下文(主路径),那么dockerfile的路径将以compose设定为准，而不是dockerfile所在目录。

```yaml
version: "3.7"
services:
    redis:
        hostname:   spider-redis
        # 根据BackServer/Config/config.py配置
        container_name: spider-redis    # 不指定则会系统自动分配名称
        restart: always  # always表容器运行发生错误时一直重启
        build:
            context:    ./
            dockerfile: ./docker/redis/Dockerfile 
        #command: /usr/local/bin/redis-server /usr/local/etc/redis.conf
        environment:    # environment 一定要在command下面
            - TZ=Asia/Shanghai
        volumes:
            - /etc/localtime:/etc/localtime:ro  # 设置容器时区与宿主机保持一致
            #- ./docker/redis/redis.conf:/usr/local/etc/redis.conf
        privileged: true
        ports:
            - "6379:6379"
        tty: true

    mysql:
        hostname:   spider-mysql
        container_name: spider-mysql
        restart:    always
        build:
            context: ./
            dockerfile: ./docker/mysql/Dockerfile
        #command:
        environment:
            # 这个根据项目BackServer的Config/config.py里面的设置对应
            - MYSQL_ROOT_PASSWORD=5201020116    # 配置数据库的密码
        volumes:
           # 初始化数据库信息- ./docker/mysql/Mysql_Init_Script.sql:/docker-entrypoint-initdb.d/  
            - ./docker/mysql/my.cnf:/etc/mysql/my.cnf    # 挂载配置文件-
            - /etc/localtime:/etc/localtime:ro  # 设置容器时区与宿主机保持一致
        ports:
            - "3306:3306"

    flask:
        hostname:   spider-flask
        container_name: spider-flask
        restart:    always
        build:  .   # 执行当前的目录下的dockerfile
            # context:    ./
            # dockerfile: ./docker/uwsgi_flask/Dockerfile
        volumes:
            - /etc/localtime:/etc/localtime:ro  # 设置容器时区与宿主机保持一致
        ports:
            - "9999:9999"
        links:
            - mysql
            - redis
        depends_on:
            - mysql
            - redis

    nginx:
        hostname:   spider-nginx
        container_name: spider-nginx
        restart:    always
        build:
            context:    ./
            dockerfile: ./docker/web/Dockerfile
        ports:
            - "8080:8080"   # 根据nginx.conf配置
            - "443:443"
        volumes:
            - ./dist/:/usr/share/nginx/html/dist
        links:
            - flask
        depends_on:
            - flask
```



### 4. 需要注意mysql和redis的ip修改

mysql和redis的ip不能是以前的localhost或者127.0.0.1.要改为`容器名字`作为ip，或者是容器的`ip地址`。

## 四、uwsgi和docker爬坑

### 1. 报错invalid request block size: xxx...skip

这个是比较常见的，问题出在请求的时候`协议`和对应`uwsgi配置或启动`不一致，例如docker里面通过nginx容器访问uwsgi需要通过`.socket`文件来，uwsgi配置的是`http协议`；或者本地开发过程中uwsgi启动或者配置时采用`socket=127.0.0.1:9999`,而浏览器是http请求，也会报错，具体看实际情况。

### 2. 启动出现!!! no internal routing support, rebuild with pcre support !!!

这个是没有内部路由支持，需要通过使用`pcre`重新构建。需要先停掉uwsgi项目，然后重构下载依赖，具体做法为

```
# 卸载原有的uwsgi
pip uninstall uwsgi
# 安装pcre
sudo apt-get install libpcre3 libpcre3-dev
# 重新下载uwsgi --no-cache-dir意思是不从缓存中用上次编译的uwsgi文件
pip install uwsgi --no-cache-dir
```

### 3. uwsgi提示 No such file or directory [core/utils.c line 3654]

我的路径没有问题，而且，可为何还是提示没有这个文件呢？检查文件内容是否有注释，。

> 注意一下几点,但不一定全是:
>
> * 注意启动的时候 `--ini uwsgi_flask.ini` 后面没有空格
> * 检查文件.ini内容是否有注释，将注释全部删除即可
> * 检查文件.ini内容是否有空格，将空格全部删除
> * 路径有误！将当前含有uwsgi_flask.ini的目录挂载到容器里(我的uwsgi.ini在BackServer里面)
>
> ```
> # When I fixed it, all started work as expected.
> docker run -itd --name flask_env_container2 -v $PWD/BackServer:/app -p 9999:9999 flask_env:latest uwsgi --plugin=python3  --ini uwsgi.ini
> ```

### 4. 提示failed to build: COPY failed: stat /var/lib/docker/tmp:no such file or directory

本质上还是路径不对，检查文件别写错了。例外注意**`/dirname`**跟**`/dirname/`**区别

> * dockerfile没有指定上下文(就是你运行的dockerfile所在目录就是主路径，后面复制文件等操作以此相对应)
>
> * docker-compose文件已经指定了上下文，后面你又执行了某个路径下的dockerfile，那么对于当前service而言，你的dockerfile的上下文不再是dockerfile所在目录，而是你compose所指定的路径(context:)
> * 就是copy 或者add 后面的路径没有/ 例如 `copy a /mydir` 应该改成 `copy a /mydir/`

### 5. mysql提示Failed to get stat for directory pointed out by --secure-file-priv

```
vim /etc/my.cnf 	# (数据库配置文件)
secure-file-priv="/" 	# (即可将数据导出到任意目录)
```

如果是通过配置文件添加的，则修改my.cnf

```
# 添加[mysqld]
secure_file_priv=""
```

### 6. Supplied value : /var/lib/mysql-files 

/var/lib/mysql-files 文件是否存在或者权限问题

```
touch /var/lib/mysql-files
chown -R 777 /var/lib/mysql-files
```



## 五、项目展示和项目地址

### 1. docker-compose编排成功后的截图
flask成功创建界面：![flask_docker启动成功界面.png](https://upload-images.jianshu.io/upload_images/13876087-91058339ef43c9b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)redis和mysql创建页面：![mysql初始化成功图片.png](https://upload-images.jianshu.io/upload_images/13876087-6998284c37a5d563.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![redis初始化成功.png](https://upload-images.jianshu.io/upload_images/13876087-e0d15b8e91aa756a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
### 2\. 项目界面

基于python flask和前端Vue.js、Element-ui等前后端分离的后台用户管理,整合爬虫项目。提供了CSRF防护，权限验证，数据库备份导出excel，日志记录，定时任务，邮箱发送等功能，详见[Github](https://github.com/JackMin1314/vue-admin-spider)
一两个月的努力，希望大家能够支持，谢谢。期待您的start~

登陆界面：![登录界面.png](https://upload-images.jianshu.io/upload_images/13876087-4021981cc18feb19.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

注册界面：![注册界面.png](https://upload-images.jianshu.io/upload_images/13876087-f15f67a12cab533a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

爬取和下载界面:![dashboard.png](https://upload-images.jianshu.io/upload_images/13876087-27b30593ce81d14a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

用户权限管理界面:![user_permission.png](https://upload-images.jianshu.io/upload_images/13876087-072f9e6a879c115e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

日志备份下载和清空界面:![logging_backup.png](https://upload-images.jianshu.io/upload_images/13876087-7d331803e3a5928b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###3.写在最后
由于时间关系，开发文档没有来的及编写，但代码注释说明写的很详细，项目可分成三部分使用本地开发、线上部署、和docker环境 (对于爬虫那块需要自行部署selenium和chromium)部署。欢迎大家相互学习交流，评论区留言或github提issue。项目地址>>[Github](https://github.com/JackMin1314/vue-admin-spider)
