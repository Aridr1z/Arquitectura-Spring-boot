package com.example.demo.controllers;

import com.example.demo.models.User;
import com.example.demo.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/users") // Todas las rutas aquí empiezan con /api/users
public class UserController {

    @Autowired // Inyecta la dependencia del repositorio
    private UserRepository userRepository;

    // --- CREAR (Create) ---
    // POST /api/users
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        try {
            // El pwdHash debería ser hasheado aquí en un proyecto real
            // Por ahora, solo guardamos lo que venga
            User newUser = userRepository.save(user);
            return ResponseEntity.status(HttpStatus.CREATED).body(newUser);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    // --- LEER TODOS (Read) ---
    // GET /api/users
    @GetMapping
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    // --- LEER UNO (Read) ---
    // GET /api/users/usr_1
    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable String id) {
        Optional<User> user = userRepository.findById(id);
        
        return user.map(ResponseEntity::ok) // Si lo encuentra, devuelve 200 OK
                   .orElseGet(() -> ResponseEntity.notFound().build()); // Si no, 404
    }

    // --- ACTUALIZAR (Update) ---
    // PUT /api/users/usr_1
    @PutMapping("/{id}")
    public ResponseEntity<User> updateUser(@PathVariable String id, @RequestBody User userDetails) {
        
        Optional<User> optionalUser = userRepository.findById(id);
        
        if (optionalUser.isPresent()) {
            User existingUser = optionalUser.get();
            
            // Actualizamos los campos (no actualizamos el ID ni createdAt)
            existingUser.setEmail(userDetails.getEmail());
            existingUser.setPwdHash(userDetails.getPwdHash());
            existingUser.setProfile(userDetails.getProfile());
            
            User updatedUser = userRepository.save(existingUser);
            return ResponseEntity.ok(updatedUser);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    // --- ELIMINAR (Delete) ---
    // DELETE /api/users/usr_1
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable String id) {
        if (userRepository.existsById(id)) {
            userRepository.deleteById(id);
            return ResponseEntity.noContent().build(); // 204 No Content
        } else {
            return ResponseEntity.notFound().build(); // 404 Not Found
        }
    }
}