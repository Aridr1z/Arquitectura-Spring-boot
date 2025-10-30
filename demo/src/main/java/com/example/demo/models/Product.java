// ¡PAQUETE CORREGIDO! Ahora coincide con la carpeta
package com.example.demo.models;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.util.Map;
import java.util.Date;
import lombok.Data;

@Document(collection = "products")
@Data
public class Product {

    @Id
    private String id; // "prd_1"

    private String sellerId;
    private String type;
    private String title;
    private double price;
    private Map<String, Object> details; // Campo flexible
    private Date createdAt;
}
