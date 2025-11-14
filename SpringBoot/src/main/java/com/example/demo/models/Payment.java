package com.example.demo.models;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.util.Date;
import lombok.Data;

@Document(collection = "payments") // Conecta a la colección "payments"
@Data
public class Payment {

    @Id
    private String id; // "pay_1001"

    private String orderId;
    private String userId;
    private double amount;
    private String status;
    private String provider;
    private Date ts; // Timestamp
}