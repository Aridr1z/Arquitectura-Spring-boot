package com.example.demo.models;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.util.Date;
import java.util.List; // Importante: para manejar el array de items
import lombok.Data;

@Document(collection = "orders") // Conecta a la colección "orders"
@Data
public class Order {

    @Id
    private String id; // "ord_101"

    private String userId;
    
    // Aquí le decimos a Java que "items" es una Lista
    // de objetos OrderItem (nuestro subdocumento)
    private List<OrderItem> items;

    private String status;
    private Date createdAt;
}