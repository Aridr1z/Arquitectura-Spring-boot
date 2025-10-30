// Script para cargar datos iniciales en el contenedor de MongoDB
db = db.getSiblingDB('ecommerce'); // Crea/Usa la base de datos 'ecommerce'

// --- Colección de Usuarios ---
db.users.insertMany([
  {
    "_id": "usr_1",
    "email": "ana@example.com",
    "pwdHash": "<argon2_hash_simulado>", // En un proyecto real, esto sería un hash seguro
    "profile": { "name": "Ana", "country": "MX" },
    "createdAt": new Date("2025-09-20T18:00:00Z")
  }
]);

// --- Colección de Productos ---
db.products.insertMany([
  {
    "_id": "prd_1",
    "sellerId": "usr_1",
    "type": "DIGITAL",
    "title": "Curso de Java",
    "price": 500.00,
    "details": { "format": "PDF", "sizeMB": 25 },
    "createdAt": new Date("2025-09-20T18:10:00Z")
  },
  {
    "_id": "prd_2",
    "sellerId": "usr_1",
    "type": "PHYSICAL",
    "title": "Taza de Programador",
    "price": 250.50,
    "details": { "color": "blanco", "material": "ceramica" },
    "createdAt": new Date("2025-09-21T10:00:00Z")
  }
]);

// --- Colección de Órdenes ---
db.orders.insertMany([
  {
    "_id": "ord_101",
    "userId": "usr_1",
    "items": [
      { "productId": "prd_1", "qty": 1, "price": 500.00 }
    ],
    "status": "PENDING",
    "createdAt": new Date("2025-09-20T18:20:00Z")
  }
]);

// --- Colección de Pagos ---
db.payments.insertMany([
  {
    "_id": "pay_1001",
    "orderId": "ord_101",
    "userId": "usr_1",
    "amount": 500.00,
    "status": "AUTHORIZED",
    "provider": "STRIPE_SANDBOX",
    "ts": new Date("2025-09-20T18:21:00Z")
  }
]);

print("✅ Datos iniciales cargados en la base de datos 'ecommerce'.");