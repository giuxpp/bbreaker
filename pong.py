import pygame
import sys

# Configuración de pantalla
ancho, alto = 1200, 800
pantalla, reloj = None, None

# Variables globales
terminar_programa = False
logs_activados = False

botones = {
    "izquierdo": "liberado",
    "derecho": "liberado",
    "arriba": "liberado",
    "abajo": "liberado"
}

# Variables de posición de la Barra
barra_ancho, barra_alto = 100, 20
barra_x = (ancho - barra_ancho) // 2
barra_y = alto - barra_alto - 10
barra_step_def = 0.25
barra_step_inc = barra_step_def  # Incremento del paso de movimiento de la barra
barra_step_max = 20  # Máximo paso de movimiento de la barra
barra_step = barra_step_def

def log(mensaje):
    global logs_activados
    if logs_activados:
        print(mensaje)

# Descripción del juego
log ("Este es un juego de pong hecho por Giuxx")

# Inicializar Pygame
def game_init():
    pygame.init()
    global ancho, alto, pantalla, reloj    
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Pong Game - By Giuxpp")
    reloj = pygame.time.Clock()

# Manejador de eventos del juego
# Captura eventos de teclado y cierre de ventana
# Actualiza la posición de la barra según las teclas presionadas
def manejador_eventos():
    global barra_x, barra_y, barra_ancho, barra_alto, barra_step
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_LEFT and botones["derecho"] == "liberado":
                log("Tecla izquierda presionada")                
                botones["izquierdo"] = "presionado"
            elif event.key == pygame.K_RIGHT:
                log("Tecla derecha presionada")
                botones["derecho"] = "presionado"
            elif event.key == pygame.K_UP:
                log("Tecla arriba presionada")
            elif event.key == pygame.K_DOWN:
                log("Tecla abajo presionada")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                log("Tecla izquierda liberada")
                botones["izquierdo"] = "liberado"
                barra_step = barra_step_def  # Reiniciar paso al soltar la tecla
            elif event.key == pygame.K_RIGHT:
                log("Tecla derecha liberada")
                botones["derecho"] = "liberado"
                barra_step = barra_step_def  # Reiniciar paso al soltar la tecla
            elif event.key == pygame.K_UP:
                log("Tecla arriba liberada")
            elif event.key == pygame.K_DOWN:
                log("Tecla abajo liberada")

# Función para dibujar la barra en la posición especificada por las variables globales
def dibujar_barra():
    global barra_x, barra_y, barra_ancho, barra_alto, barra_step
    if barra_step < barra_step_max: barra_step += barra_step_inc
    if botones["izquierdo"] == "presionado" and barra_x > 0:
        barra_x -= barra_step
        log("Barra movida a la izquierda")
    elif botones["derecho"] == "presionado" and barra_x < ancho - barra_ancho:
        barra_x += barra_step
        log("Barra movida a la derecha")
    pygame.draw.rect(pantalla, (255, 255, 255), (barra_x, barra_y, barra_ancho, barra_alto))
    log(f"Barra dibujada en posición: ({barra_x}, {barra_y})")

# Función principal del juego
def main():
    game_init()
    log("Pygame inicializado correctamente.")
    log(f"Resolución de pantalla: {ancho}x{alto}")

    # Bucle principal del juego
    while True:
        # Manejo de eventos
        manejador_eventos()
        # Actualizar estado del juego aquí

        pantalla.fill((0, 0, 0))  # Fondo negro

        # Dibujar objetos aquí
        dibujar_barra()

        pygame.display.flip()     # Mostrar todo en pantalla
        reloj.tick(60)            # Limita a 60 FPS

if __name__ == "__main__":
    main()