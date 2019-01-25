FROM jdk
RUN mkdir -pv /app
COPY git_spring_cloud/activity-eureka-1.0.1.jar /app/activity-eureka-1.0.1.jar
EXPOSE 7020
CMD java -jar /app/activity-eureka-1.0.1.jar

#ENTRYPOINT ["java","-jar","/app/activity-eureka-1.0.1.jar"]
