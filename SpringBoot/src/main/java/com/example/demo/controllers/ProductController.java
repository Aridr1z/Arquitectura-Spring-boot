package com.example.demo.controllers;

import com.example.demo.models.Product;
import com.example.demo.repositories.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired; // Para inyección de dependencias
import org.springframework.http.HttpStatus; // Para códigos de estado HTTP (201 CREATED, 404 NOT_FOUND)
import org.springframework.http.ResponseEntity; // Para respuestas HTTP con estado y cuerpo
import org.springframework.web.bind.annotation.*; // Para @RestController, @RequestMapping, @GetMapping, etc.
import java.util.List;
import java.util.Optional; // Para manejar resultados que pueden no existir

@RestController // Indica que esta clase manejará peticiones REST
@RequestMapping("/api/products") // Todas las rutas en esta clase empezarán con /api/products
public class ProductController {

    // Spring inyectará automáticamente una instancia de ProductRepository aquí
    @Autowired
    private ProductRepository productRepository;

    // --- LEER TODOS (Read) ---
    // Mapea peticiones GET a /api/products
    @GetMapping
    public List<Product> getAllProducts() {
        // Usa el método findAll() que nos da MongoRepository
        return productRepository.findAll();
    }

    // --- LEER UNO (Read) ---
    // Mapea peticiones GET a /api/products/{id} (ej: /api/products/prd_1)
    @GetMapping("/{id}")
    public ResponseEntity<Product> getProductById(@PathVariable String id) {
        // @PathVariable toma el valor de {id} en la URL y lo pasa como argumento
        Optional<Product> product = productRepository.findById(id);

        // Si el producto existe (isPresent), devuelve 200 OK con el producto.
        // Si no, devuelve 404 Not Found.
        return product.map(ResponseEntity::ok) // Forma corta de: p -> ResponseEntity.ok(p)
                      .orElseGet(() -> ResponseEntity.notFound().build());
    }

    // --- AGREGAR (Create) ---
    // Mapea peticiones POST a /api/products
    @PostMapping
    public ResponseEntity<Product> createProduct(@RequestBody Product product) {
        // @RequestBody toma el JSON del cuerpo de la petición y lo convierte en un objeto Product
        try {
            Product newProduct = productRepository.save(product);
            // Devuelve 201 Created con el nuevo producto en el cuerpo
            return ResponseEntity.status(HttpStatus.CREATED).body(newProduct);
        } catch (Exception e) {
            // Si algo falla (ej. datos inválidos), devuelve 400 Bad Request
            return ResponseEntity.badRequest().build();
        }
    }

    // --- ACTUALIZAR (Update) ---
    // Mapea peticiones PUT a /api/products/{id}
    @PutMapping("/{id}")
    public ResponseEntity<Product> updateProduct(@PathVariable String id, @RequestBody Product productDetails) {
        // Busca el producto existente por su ID
        Optional<Product> optionalProduct = productRepository.findById(id);
        
        if (optionalProduct.isPresent()) {
            // Si existe, obtén el objeto
            Product existingProduct = optionalProduct.get();
            
            // Actualiza los campos con los nuevos detalles
            // (Nota: No actualizamos el ID, sellerId, o createdAt)
            existingProduct.setTitle(productDetails.getTitle());
            existingProduct.setPrice(productDetails.getPrice());
            existingProduct.setDetails(productDetails.getDetails());
            existingProduct.setType(productDetails.getType());

            // Guarda el producto actualizado en la base de datos
            Product updatedProduct = productRepository.save(existingProduct);
            return ResponseEntity.ok(updatedProduct);
        } else {
            // Si no se encuentra el producto, devuelve 404
            return ResponseEntity.notFound().build();
        }
    }


    // --- ELIMINAR (Delete) ---
    // Mapea peticiones DELETE a /api/products/{id}
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProduct(@PathVariable String id) {
        // Primero, verificamos si el producto existe
        if (productRepository.existsById(id)) {
            // Si existe, lo eliminamos
            productRepository.deleteById(id);
            // Devuelve 204 No Content (éxito sin cuerpo de respuesta)
            return ResponseEntity.noContent().build();
        } else {
            // Si no existe, devuelve 404 Not Found
            return ResponseEntity.notFound().build();
        }
    }
}