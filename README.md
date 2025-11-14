# Proyecto

# Arquitectura Spring Boot


Proyecto de ejemplo para un backend de e-commerce construido con Spring Boot y MongoDB. Incluye un entorno de desarrollo reproducible con Docker Compose y datos iniciales para probar los endpoints REST.

## Requisitos previos

- Docker 20.10+ y Docker Compose v2.
- Java 17 y Maven 3.9+ (solo si deseas ejecutar el proyecto sin Docker).

## Ejecución con Docker Compose

1. Sitúate en el directorio `SpringBoot/`:
   ```bash
   cd SpringBoot
   ```
2. Construye y levanta los servicios (aplicación y MongoDB):
   ```bash
   docker compose up --build
   ```
3. Espera a que la aplicación muestre el mensaje `Started EcommerceApplication`. 
4. Los endpoints REST quedarán disponibles en `http://localhost:8080/api/...`.
5. Los datos iniciales se cargan automáticamente gracias al script `init-mongo.js`. Puedes inspeccionarlos conectándote a MongoDB en `mongodb://root:root@localhost:27017` (base de datos `ecommerce`).
6. Cuando termines, detén los servicios:
   ```bash
   docker compose down
   ```

> El archivo `docker-compose.yml` define dos servicios:
> - `web`: Construye la imagen usando el `dockerfile` del proyecto, expone el puerto 8080 y activa el perfil `dev` de Spring.
> - `db`: Usa la imagen oficial de MongoDB, crea el usuario `root` con contraseña `root`, ejecuta `init-mongo.js` y persiste los datos en el volumen `mongo-data`.

## Ejecución local con Maven

Si prefieres ejecutar la aplicación sin contenedores:

```bash
cd SpringBoot
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

## Estructura principal del código Java (`SpringBoot/src/main/java/com/example/demo`)

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