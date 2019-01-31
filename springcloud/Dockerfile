FROM 10.0.1.133:5000/jdk
RUN mkdir -pv /app
ARG jarName
ARG envName
COPY ${jarName}  /app/${jarName}
ENV envName $envName
ENV jarName $jarName

EXPOSE 7020

CMD java -jar /app/${jarName} --spring.profiles.active=${envName}

#ENTRYPOINT ["java","-jar","/app/activity-eureka-1.0.1.jar"]
