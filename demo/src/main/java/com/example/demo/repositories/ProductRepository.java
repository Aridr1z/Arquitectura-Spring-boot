package com.example.demo.repositories;

import com.example.demo.models.Product;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProductRepository extends MongoRepository<Product, String> {
    // Spring Data MongoDB crea el CRUD por nosotros
}