package com.example.demo.models;

import lombok.Data;

// Esta es una clase simple (POJO) para el subdocumento.
// No es una colección principal, por eso no lleva @Document.
@Data
public class OrderItem {
    private String productId;
    private int qty;
    private double price;
}