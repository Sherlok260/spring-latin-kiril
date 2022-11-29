FROM openjdk:17
EXPOSE 8080
ADD target/spring-latin-kiril.jar spring-latin-kiril.jar
ENTRYPOINT ["java", "-jar", "/spring-latin-kiril.jar"]