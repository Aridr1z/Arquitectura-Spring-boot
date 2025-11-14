package main

import (
	"github.com/gin-gonic/gin" // Importa el framework Gin
)

func main() {
	// 1. Inicia un router de Gin con la configuración por defecto
	r := gin.Default()

	// 2. Define una ruta (endpoint)
	// Cuando alguien visite GET /api/go/saludo...
	r.GET("/api/go/saludo", func(c *gin.Context) {

		// ...responde con este JSON
		c.JSON(200, gin.H{
			"mensaje": "¡Hola desde el servicio de Go con Gin!",
		})
	})

	// 3. Inicia el servidor
	// Spring (demo) usa :8080
	// Vue (frontend) usa :5173
	// Go usará :8082
	r.Run(":8082") // Escucha en el puerto 8082
}
