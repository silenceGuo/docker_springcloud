# Dockfile for tomcat7:base
FROM jdk
MAINTAINER demon@kilimall.com
RUN mkdir -pv /data/tomcat8
COPY tomcat-8 /data/tomcat8
RUN chmod +x /data/tomcat8/tomcat/bin/*
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
EXPOSE 8080
CMD ["/data/tomcat8/tomcat/bin/catalina.sh","run"]