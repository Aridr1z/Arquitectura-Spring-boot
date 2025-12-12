# gRPC Python service (Products + Greeter)

Este proyecto implementa un servidor gRPC en Python que se conecta **directamente a la misma base de datos MongoDB** usada por el demo de Spring Boot en `/demo`.

## Base de datos detectada
- Motor: MongoDB
- Host/puerto (docker-compose): `db:27017`
- Usuario/contraseña: `root` / `root`
- Base: `ecommerce`
- Colección usada por el CRUD: `products`
- Esquema (Spring): campos `_id`, `sellerId`, `type`, `title`, `price`, `details` (objeto), `createdAt` (fecha). Datos iniciales en `demo/init-mongo.js`.

## Estructura
```
python/
├── proto/ecommerce.proto          # Servicios Greeter + CRUD de productos
├── server/app.py                  # Servidor gRPC
├── server/ecommerce_pb2.py        # Stubs protobuf generados
├── server/ecommerce_pb2_grpc.py   # Stubs gRPC (manual)
├── db/connection.py               # Cliente Mongo
├── db/product_repository.py       # DAO CRUD
├── requirements.txt
└── Dockerfile
```

## Configuración de entorno
El servidor lee estas variables (con valores por defecto que coinciden con `docker-compose.yml`):
- `DB_HOST` (por defecto `db`)
- `DB_PORT` (por defecto `27017`)
- `DB_USER` (por defecto `root`)
- `DB_PASS` (por defecto `root`)
- `DB_NAME` (por defecto `ecommerce`)
- `GRPC_PORT` (por defecto `50051`)

## Instalación y generación de stubs (local)
Requiere acceso a PyPI.
```bash
pip install -r requirements.txt
protoc -I=proto --python_out=server proto/ecommerce.proto  # (ya generado)
```

## Ejecutar localmente (sin Docker)
```bash
export DB_HOST=localhost DB_PORT=27017 DB_USER=root DB_PASS=root DB_NAME=ecommerce
export GRPC_PORT=50051
python server/app.py
```

## Docker
Construir solo el servicio Python:
```bash
docker build -t python-grpc-service .
docker run --rm -p 50051:50051 \
  -e DB_HOST=db -e DB_PORT=27017 -e DB_USER=root -e DB_PASS=root -e DB_NAME=ecommerce \
  python-grpc-service
```

`docker-compose.yml` en la raíz ya incluye el servicio `python-grpc` conectado a la misma red y base de datos que Spring Boot.

## Probar en Postman (gRPC)
### Endpoint
`grpc://localhost:50051`
Importa el archivo [`proto/ecommerce.proto`](./proto/ecommerce.proto).

### Greeter/SayHello
- Servicio: `ecommerce.Greeter`
- Método: `SayHello`
- Payload de ejemplo (JSON):
```json
{
  "name": "Ada"
}
```
- Respuesta esperada:
```json
{
  "message": "Hello, Ada!"
}
```

### CRUD de productos
Servicio: `ecommerce.ProductService`

1) **CreateProduct**
```json
{
 "product": {
    "id": "prd_custom",      // opcional, se genera UUID si no se envía
    "seller_id": "usr_1",
    "type": "DIGITAL",
    "title": "Nuevo curso",
    "price": 199.99,
    "details": {"format": "PDF"},
    "created_at": "2024-05-08T10:00:00"
  }
}
```
- Respuesta: `ProductResponse` con el documento creado.
- Errores: `INVALID_ARGUMENT` (campos requeridos), `ALREADY_EXISTS` (id duplicado).

2) **GetProductById**
```json
{"id": "prd_1"}
```
- Respuesta: `ProductResponse`.
- Errores: `INVALID_ARGUMENT` (id vacío), `NOT_FOUND` (no existe).

3) **UpdateProduct**
```json
{
  "product": {
    "id": "prd_1",
    "title": "Título actualizado",
    "seller_id": "usr_1",
    "type": "DIGITAL",
    "price": 210.0,
    "details": {"format": "PDF", "duration": "10h"},
    "created_at": "2024-05-08T10:00:00"
  }
}
```
- Respuesta: `ProductResponse` con valores posteriores al update.
- Errores: `INVALID_ARGUMENT` (id faltante), `NOT_FOUND`.

4) **DeleteProduct**
```json
{"id": "prd_2"}
```
- Respuesta: `{ "deleted": true }`
- Errores: `INVALID_ARGUMENT`, `NOT_FOUND`.

5) **ListProducts**
```json
{"page": 1, "page_size": 10}
```
- Respuesta:
```json
{
  "products": [ /* array */ ],
  "page": 1,
  "page_size": 10,
  "total": 3
}
```

### Códigos de error
- `INVALID_ARGUMENT`: datos faltantes o id vacío.
- `NOT_FOUND`: recurso no existe.
- `ALREADY_EXISTS`: id duplicado en creación.
- `INTERNAL`: errores inesperados de base de datos.

## Notas
- El servidor usa la colección `products` existente; no crea colecciones nuevas.
- Asegúrate de que el contenedor `db` esté corriendo (mismo `docker-compose.yml`).
