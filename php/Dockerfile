#使用国内网易镜像可以加快构建速度
FROM php7.1.9:fpm-alpine
#FROM php:fpm-alpine
#FROM hub.c.163.com/library/php:fpm-alpine 网络镜像地址

MAINTAINER demon@kilimall.com

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

#国内repo源，让本地构建速度更快。
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories



# 安装nginx

RUN apk add --no-cache nginx \
    && mkdir /run/nginx \
    && rm /etc/nginx/nginx.conf


ADD conf_dir/nginx.conf /etc/nginx/
ADD conf_dir/test.conf /etc/nginx/conf.d/

#ADD conf_dir/test.html /www/webs/
ADD conf_dir/test.php /www/webs/


#安装GD依赖库
RUN apk add --no-cache --virtual .build-deps \
                freetype-dev \
                libjpeg-turbo-dev \
                libpng-dev \
                libmcrypt-dev


#添加php源码中的扩展，添加gd,mysqli,pdo-mysql,opcache,gettext,mcrypt等扩展
RUN set -ex \
        && docker-php-ext-configure gd \
                --with-freetype-dir=/usr/include/freetype2/freetype \
                --with-jpeg-dir=/usr/include \
                --with-png-dir=/usr/include \
        && docker-php-ext-install exif gd bcmath zip opcache pcntl iconv mcrypt pdo pdo_mysql mysqli shmop



#redis属于pecl扩展，需要使用pecl命令来安装，同时需要添加依赖的库
RUN apk add --no-cache --virtual .phpize-deps $PHPIZE_DEPS \
        && pecl install redis \
        && docker-php-ext-enable redis \
        && apk del .phpize-deps

# 安装mongdb
RUN apk add --no-cache --virtual .phpize-deps $PHPIZE_DEPS \
        && pecl install mongodb \
        && docker-php-ext-enable mongodb \
        && apk del .phpize-deps

# 安装swoole 依赖需要 openssl-dev
RUN apk --update add --no-cache openssl-dev libssh2-dev

WORKDIR /
ADD conf_dir/run.sh /
RUN chmod +x /run.sh

#CMD["/usr/sbin/nginx -c /etc/nginx/nginx.conf"]
##CMD ["/usr/local/sbin/php-fpm --daemonize"]
#CMD ["/run.sh"]
EXPOSE 80
#CMD ["/run.sh","run"]
#CMD ["/run.sh"]
ENTRYPOINT ["/run.sh"]
#CMD ["/bin/sh /run.sh"]
