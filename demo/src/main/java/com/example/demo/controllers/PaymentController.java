package com.example.demo.controllers;

import com.example.demo.models.Payment;
import com.example.demo.repositories.PaymentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/payments") // Prefijo para todos los endpoints
public class PaymentController {

    @Autowired
    private PaymentRepository paymentRepository;

    // --- CREAR (Create) ---
    // POST /api/payments
    @PostMapping
    public ResponseEntity<Payment> createPayment(@RequestBody Payment payment) {
        try {
            Payment newPayment = paymentRepository.save(payment);
            return ResponseEntity.status(HttpStatus.CREATED).body(newPayment);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    // --- LEER TODOS (Read) ---
    // GET /api/payments
    @GetMapping
    public List<Payment> getAllPayments() {
        return paymentRepository.findAll();
    }

    // --- LEER UNO (Read) ---
    // GET /api/payments/pay_1001
    @GetMapping("/{id}")
    public ResponseEntity<Payment> getPaymentById(@PathVariable String id) {
        Optional<Payment> payment = paymentRepository.findById(id);
        
        return payment.map(ResponseEntity::ok)
                      .orElseGet(() -> ResponseEntity.notFound().build());
    }

    // --- ENDPOINT PERSONALIZADO ---
    // LEER pagos por ID de Orden
    // GET /api/payments/by-order/ord_101
    @GetMapping("/by-order/{orderId}")
    public ResponseEntity<List<Payment>> getPaymentsByOrderId(@PathVariable String orderId) {
        List<Payment> payments = paymentRepository.findByOrderId(orderId);
        if (payments.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(payments);
    }

    // --- ELIMINAR (Delete) ---
    // DELETE /api/payments/pay_1001
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletePayment(@PathVariable String id) {
        if (paymentRepository.existsById(id)) {
            paymentRepository.deleteById(id);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}

