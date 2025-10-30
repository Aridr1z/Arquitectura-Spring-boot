package com.example.demo; // Asegúrate que esto coincida con tu paquete

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LibroController {

    @GetMapping("/")
    public String holaMundo() {
        return "¡Hola Mundo desde Spring Boot!";
    }
}