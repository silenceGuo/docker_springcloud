MAINTAINER demon@kilimall.com
FROM 10.0.1.133:5000/jdk
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
RUN mkdir -pv /app
ARG jarName
ARG envName
ARG dockerport
COPY ${jarName}  /app/${jarName}
ENV envName $envName
ENV jarName $jarName

EXPOSE ${dockerport}

CMD java -jar /app/${jarName} --spring.profiles.active=${envName}

#ENTRYPOINT ["java","-jar","/app/activity-eureka-1.0.1.jar"]
