FROM jeanblanchard/alpine-glibc
MAINTAINER GuoZQ
RUN mkdir -pv /data/jdk1.8.0_121
COPY jdk1.8.0_121 /data/jdk1.8.0_121
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV JAVA_HOME /data/jdk1.8.0_121
ENV JAVA_BIN /data/jdk1.8.0_121/bin
ENV JRE_HOME /data/jdk1.8.0_121/jre
ENV PATH $JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
ENV CLASSPATH $JAVA_HOME/jre/lib:$JAVA_HOME/lib:$JAVA_HOME/jre/lib/charsets.jar
ENV JAVA_OPTS "$JAVA_OPTS -Duser.timezone=Asia/Shanghai"