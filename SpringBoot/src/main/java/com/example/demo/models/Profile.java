package com.example.demo.models;

import lombok.Data;

// No necesita @Document porque no es una colección principal.
// Solo es una clase de datos para el perfil.
@Data
public class Profile {
    private String name;
    private String country;
}