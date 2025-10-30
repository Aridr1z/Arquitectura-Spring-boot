package com.example.demo.repositories;

import com.example.demo.models.Payment;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface PaymentRepository extends MongoRepository<Payment, String> {

    // Método personalizado para buscar pagos por orderId
    // Spring Data lo implementa automáticamente basado en el nombre
    List<Payment> findByOrderId(String orderId);
}