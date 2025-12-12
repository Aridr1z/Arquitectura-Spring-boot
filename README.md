# Proyecto

# Arquitectura Spring Boot


Proyecto de ejemplo para un backend de e-commerce construido con Spring Boot y MongoDB. Incluye un entorno de desarrollo reproducible con Docker Compose y datos iniciales para probar los endpoints REST.

## Requisitos previos

- Docker 20.10+ y Docker Compose v2.
- Java 17 y Maven 3.9+ (solo si deseas ejecutar el proyecto sin Docker).

## Ejecución con Docker Compose

1. En la raíz del repo ejecuta:
   ```bash
   docker compose up -d --build
   ```
   Levanta los servicios frontend, API en Go, Spring Boot, MongoDB y el servidor gRPC de Python.
2. Verifica que los contenedores estén arriba:
   ```bash
   docker compose ps
   ```
3. Confirma que el servidor gRPC está escuchando y sin errores:
   ```bash
   docker logs python-grpc-1
   ```
   Si el nombre del contenedor difiere, revisa el mostrado por `docker compose ps`.
4. Cuando termines, detén los servicios:
   ```bash
   docker compose down
   ```

> El archivo `docker-compose.yml` define los servicios `web` (Spring Boot), `frontend` (Vite), `go-service`, `db` (Mongo) y `python-grpc` (gRPC Python conectado a MongoDB `db`).

### Servicio gRPC en Python

El servicio `python-grpc` expone un Greeter y un CRUD de productos usando la misma base de datos MongoDB que Spring Boot.

- Código fuente: [`python/server/app.py`](python/server/app.py)
- Proto: [`python/proto/ecommerce.proto`](python/proto/ecommerce.proto)
- Puerto: `50051` (puede cambiarse con la variable `GRPC_PORT`).
- Variables de conexión a Mongo (con valores por defecto de `docker-compose.yml`):
  - `DB_HOST=db`
  - `DB_PORT=27017`
  - `DB_USER=root`
  - `DB_PASS=root`
  - `DB_NAME=ecommerce`

#### Ejecutar solo el servicio de Python

```bash
cd python
docker build -t python-grpc-service .
docker run --rm -p 50051:50051 \
  -e DB_HOST=db -e DB_PORT=27017 -e DB_USER=root -e DB_PASS=root -e DB_NAME=ecommerce \
  python-grpc-service
```

Si corres todo el stack con `docker compose up`, no necesitas construir la imagen manualmente: Compose usa el `Dockerfile` de esta carpeta.

#### Probar el gRPC (Postman o cliente gRPC)

1. Usa el endpoint `grpc://localhost:50051`.
2. Importa [`python/proto/ecommerce.proto`](python/proto/ecommerce.proto) en Postman/Insomnia.
3. Prueba el Greeter con el método `ecommerce.Greeter/SayHello` enviando `{ "name": "Ada" }`.
4. Prueba el CRUD de productos (`ecommerce.ProductService`):
   - **CreateProduct**: envía un `product` con `seller_id`, `type`, `title`, `price` y `details` (opcional). Si no envías `id`, se genera un UUID.
   - **GetProductById**: consulta cualquier documento de la colección `products` (`prd_1`, `prd_2` vienen en los datos iniciales).
   - **UpdateProduct**, **DeleteProduct**, **ListProducts**: cubren el resto del CRUD y devuelven los códigos de error estándar (`INVALID_ARGUMENT`, `NOT_FOUND`, `ALREADY_EXISTS`, `INTERNAL`).

Con Compose, los datos iniciales se cargan desde `demo/init-mongo.js` y son compartidos por Spring Boot y Python.

## Ejecución local con Maven

Si prefieres ejecutar la aplicación sin contenedores:

```bash
cd demo
./mvnw spring-boot:run
```

Asegúrate de definir la variable `MONGO_URI` apuntando a tu instancia de MongoDB o adapta `src/main/resources/application.properties` con tus credenciales. Para usar la configuración de desarrollo incluida, activa el perfil `dev`:

```bash
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
```

## Configuración de Spring

- `src/main/resources/application.properties`: Configuración por defecto orientada a despliegues (puerto, `MONGO_URI`, base de datos `ecommerce`).
- `src/main/resources/application-dev.properties`: Se activa con el perfil `dev` y conecta a la base MongoDB del contenedor `db` (`mongodb://root:root@db:27017/ecommerce?authSource=admin`).

## Datos iniciales

El archivo `init-mongo.js` crea:
- Un usuario (`usr_1`) con perfil de ejemplo.
- Dos productos (`prd_1`, `prd_2`).
- Una orden (`ord_101`) ligada al usuario anterior.
- Un pago (`pay_1001`) asociado a la orden.

## Probar el servidor gRPC en Postman

- Endpoint: `grpc://localhost:50051`
- Importa el archivo `python/proto/ecommerce.proto`.
- Métodos disponibles:
  - `ecommerce.Greeter/SayHello`: envía `{ "name": "Ada" }` y espera `{ "message": "Hello, Ada!" }`.
  - `ecommerce.ProductService/*`: CRUD completo de productos respaldado por la colección `products` en MongoDB.

## Estructura principal del código Java (`src/main/java/com/example/demo`)

### Clase de arranque
- **`EcommerceApplication.java`**: Punto de entrada de Spring Boot. Habilita el escaneo de repositorios MongoDB en `com.example.demo.repositories` y arranca el contexto de la aplicación.

### Controladores (`controllers`)
- **`UserController.java`**: CRUD para usuarios (`/api/users`). Permite crear, listar, obtener, actualizar y eliminar usuarios.
- **`ProductController.java`**: CRUD para productos (`/api/products`). Incluye endpoints para crear, listar, obtener, actualizar y eliminar productos.
- **`OrderController.java`**: Gestiona órdenes (`/api/orders`). Ofrece creación, lectura, eliminación y una ruta personalizada para consultar órdenes por `userId`.
- **`PaymentController.java`**: Maneja pagos (`/api/payments`). Permite crear, listar, consultar por id, consultar pagos por `orderId` y eliminar.

### Modelos (`models`)
- **`User.java`**: Documento principal de la colección `users`. Contiene email, hash de contraseña, perfil y fecha de creación.
- **`Profile.java`**: Subdocumento embebido en `User` con nombre y país.
- **`Product.java`**: Documento de la colección `products`. Incluye vendedor, tipo, título, precio y un mapa flexible `details`.
- **`Order.java`**: Documento de la colección `orders`. Relaciona un usuario con una lista de `OrderItem`, estado y fecha de creación.
- **`OrderItem.java`**: Subdocumento con producto, cantidad y precio usado dentro de `Order`.
- **`Payment.java`**: Documento de la colección `payments`. Representa un pago ligado a una orden, con monto, estado, proveedor y timestamp.

### Repositorios (`repositories`)
- **`UserRepository.java`**: Extiende `MongoRepository<User, String>` para proveer CRUD automático sobre usuarios.
- **`ProductRepository.java`**: Extiende `MongoRepository<Product, String>` para las operaciones CRUD de productos.
- **`OrderRepository.java`**: Extiende `MongoRepository<Order, String>` y añade `findByUserId` para consultar órdenes por usuario.
- **`PaymentRepository.java`**: Extiende `MongoRepository<Payment, String>` con `findByOrderId` para buscar pagos por orden.

## Endpoints principales

| Recurso   | Método | Ruta                            | Descripción                               |
|-----------|--------|---------------------------------|-------------------------------------------|
| Usuarios  | POST   | `/api/users`                    | Crea un usuario.
| Usuarios  | GET    | `/api/users`                    | Lista todos los usuarios.
| Usuarios  | GET    | `/api/users/{id}`               | Obtiene un usuario por id.
| Usuarios  | PUT    | `/api/users/{id}`               | Actualiza un usuario.
| Usuarios  | DELETE | `/api/users/{id}`               | Elimina un usuario.
| Productos | POST   | `/api/products`                 | Crea un producto.
| Productos | GET    | `/api/products`                 | Lista todos los productos.
| Productos | GET    | `/api/products/{id}`            | Obtiene un producto por id.
| Productos | PUT    | `/api/products/{id}`            | Actualiza un producto.
| Productos | DELETE | `/api/products/{id}`            | Elimina un producto.
| Órdenes   | POST   | `/api/orders`                   | Crea una orden.
| Órdenes   | GET    | `/api/orders`                   | Lista todas las órdenes.
| Órdenes   | GET    | `/api/orders/{id}`              | Obtiene una orden por id.
| Órdenes   | GET    | `/api/orders/by-user/{userId}`  | Lista órdenes por `userId`.
| Órdenes   | DELETE | `/api/orders/{id}`              | Elimina una orden.
| Pagos     | POST   | `/api/payments`                 | Crea un pago.
| Pagos     | GET    | `/api/payments`                 | Lista todos los pagos.
| Pagos     | GET    | `/api/payments/{id}`            | Obtiene un pago por id.
| Pagos     | GET    | `/api/payments/by-order/{orderId}` | Lista pagos por `orderId`.
| Pagos     | DELETE | `/api/payments/{id}`            | Elimina un pago.