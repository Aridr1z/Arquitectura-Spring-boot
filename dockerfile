# --- ETAPA 1: Construcción (Compilar el .jar) ---
# Usamos una imagen de Maven con Java 17 para compilar el código
FROM maven:3.9-eclipse-temurin-17 AS build

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos el archivo de dependencias primero (para caché de Docker)
COPY pom.xml .
# Descarga las dependencias para que estén cacheadas si pom.xml no cambia
RUN mvn dependency:go-offline

# Copiamos el resto del código fuente
COPY src ./src

# Compilamos la aplicación, empaquetándola en un .jar
# El "clean" es importante para evitar errores de compilación previa
# -DskipTests acelera la compilación al saltarse las pruebas unitarias
RUN mvn clean install -DskipTests

# --- ETAPA 2: Ejecución (El contenedor final) ---
# Usamos una imagen mínima de JRE (Java Runtime) para ejecutar, es más ligera
FROM eclipse-temurin:17-jre-focal

WORKDIR /app

# Copiamos SOLO el .jar compilado de la etapa anterior
# IMPORTANTE: Asegúrate que el nombre (demo-0.0.1-SNAPSHOT.jar) coincida con el <artifactId> y <version> en tu pom.xml
COPY --from=build /app/target/demo-0.0.1-SNAPSHOT.jar app.jar

# Exponemos el puerto en el que corre la app
EXPOSE 8080

# El comando para iniciar la aplicación cuando arranque el contenedor
ENTRYPOINT ["java", "-jar", "app.jar"]

