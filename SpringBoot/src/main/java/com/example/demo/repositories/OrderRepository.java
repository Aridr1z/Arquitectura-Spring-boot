package com.example.demo.repositories;

import com.example.demo.models.Order;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface OrderRepository extends MongoRepository<Order, String> {

    // --- ¡MAGIA DE SPRING DATA! ---
    // Si defines un método con este nombre, Spring automáticamente
    // crea la consulta para buscar en la colección de "orders"
    // todos los documentos donde el campo "userId" coincida.
    List<Order> findByUserId(String userId);
}