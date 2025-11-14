package com.example.demo.models;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.util.Date;
import lombok.Data;

@Document(collection = "users") // Conecta esto a la colección "users"
@Data
public class User {

    @Id
    private String id; // El "_id" ("usr_1")

    private String email;
    private String pwdHash;
    
    // Aquí le decimos a Java que el campo "profile"
    // usará la estructura de nuestra clase Profile
    private Profile profile; 
    
    private Date createdAt;
    
    // Nota: Omitimos el array "orders" a propósito.
    // Es mucho más limpio y eficiente buscar en la colección "orders"
    // todos los que tengan un "userId" específico.
}