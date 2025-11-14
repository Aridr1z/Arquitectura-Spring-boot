# syntax=docker/dockerfile:1

# Etapa de compilación: compila el binario de Go
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Copia los archivos de dependencias primero para aprovechar la caché
COPY go.mod go.sum ./
RUN go mod download

# Copia el resto del código fuente y compila el binario
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o go-service

# Etapa final: imagen ligera para ejecutar el servicio
FROM alpine:3.20

WORKDIR /app

# Copia el binario compilado desde la etapa anterior
COPY --from=builder /app/go-service ./go-service

# Expone el puerto utilizado por el servicio
EXPOSE 8082

# Comando por defecto al iniciar el contenedor
CMD ["./go-service"]
