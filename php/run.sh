#!/bin/sh
/usr/sbin/nginx -c /etc/nginx/nginx.conf
/usr/local/sbin/php-fpm -c /usr/local/etc/php-fpm.conf
