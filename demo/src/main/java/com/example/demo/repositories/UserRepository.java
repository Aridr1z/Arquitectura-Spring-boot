package com.example.demo.repositories;

import com.example.demo.models.User;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends MongoRepository<User, String> {
    // Al extender MongoRepository<User, String>, Spring Data nos da
    // automáticamente todo el CRUD para la clase User
    // (findAll, findById, save, deleteById, etc.)
}