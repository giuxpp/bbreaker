import pygame
import sys

# Configuración de pantalla
ancho, alto = 1200, 800
pantalla, reloj = None, None

# Variables globales
terminar_programa = False
logs_activados = False

botones = {
    "izquierda": "liberado",
    "derecha": "liberado",
    "arriba": "liberado",
    "abajo": "liberado"
}

# Variables de posición de la Barra
barra_ancho, barra_alto = 100, 20
barra_x = (ancho - barra_ancho) // 2
barra_y_def = alto - barra_alto - 10
barra_y = barra_y_def
barra_step_def = 0.25
barra_y_punch = 10
barra_step_inc = barra_step_def  # Incremento del paso de movimiento de la barra
barra_step_max = 20  # Máximo paso de movimiento de la barra
barra_step = barra_step_def

# Variables usadas en el efecto de desaceleración de la barra al soltarla
desaceleracion = "ninguno"  # Variable para controlar el desaceleracion de la barra
desacel_cntr_def = 0  # Valor default del contador de desaceleración
desacel_cntr = 0 # Contador para la desaceleración de la barra

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
    global barra_step, desaceleracion, desacel_cntr
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_LEFT:
                if botones["izquierda"] == "liberado":
                    log("Tecla izquierda presionada")
                    botones["izquierda"] = "presionado"
                    desaceleracion = "ninguno"
                    barra_step = barra_step_def
            elif event.key == pygame.K_RIGHT:
                if botones["derecha"] == "liberado":
                    log("Tecla derecha presionada")
                    botones["derecha"] = "presionado"
                    desaceleracion = "ninguno"
                    barra_step = barra_step_def
            elif event.key == pygame.K_UP:
                log("Tecla arriba presionada")
                botones["arriba"] = "presionado"
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                log("Tecla izquierda liberada")
                botones["izquierda"] = "liberado"
                if botones["derecha"] == "liberado":
                    desaceleracion = "izquierda"
            elif event.key == pygame.K_RIGHT:
                log("Tecla derecha liberada")
                botones["derecha"] = "liberado"
                if botones["izquierda"] == "liberado":
                    desaceleracion = "derecha"
            elif event.key == pygame.K_UP:
                log("Tecla arriba liberada")
                botones["arriba"] = "liberado"
            elif event.key == pygame.K_DOWN:
                log("Tecla abajo liberada")
    # Resetear el contador de desaceleración
    if botones["izquierda"] == "presionado" or botones["derecha"] == "presionado":
        desacel_cntr = min(desacel_cntr + 1, 20)

# Función para dibujar la barra en la posición especificada por las variables globales
def dibujar_barra():
    global barra_x, barra_y, barra_ancho, barra_alto, barra_step, desaceleracion, desacel_cntr, barra_y_def
    # Limitar la barra dentro de los bordes de la pantalla
    barra_x = max(0, min(barra_x, ancho - barra_ancho))
    # Aceleración
    if desaceleracion == "ninguno" and (botones["izquierda"] == "presionado" or botones["derecha"] == "presionado"):
        if barra_step < barra_step_max:
            barra_step += barra_step_inc
    # Desaceleración
    elif desaceleracion in ("izquierda", "derecha"):
        if barra_step > 0:
            barra_step -= barra_step_inc * 3
        if desacel_cntr > 0:
            desacel_cntr -= 3
        else:
            desaceleracion = "ninguno"
            desacel_cntr = 0
    # Ajuste vertical si se presion boton UP
    if botones["arriba"] == "presionado":
        barra_y = max(0, barra_y_def - barra_y_punch)  # Mover hacia arriba
    elif botones["arriba"] == "liberado":
        barra_y = min(alto - barra_alto, barra_y_def)  # Mover hacia abajo
    # Movimiento
    if (botones["izquierda"] == "presionado" and barra_x > 0) or desaceleracion == "izquierda":
        barra_x -= barra_step
    elif (botones["derecha"] == "presionado" and barra_x < ancho - barra_ancho) or desaceleracion == "derecha":
        barra_x += barra_step
    # Limitar la barra nuevamente después del movimiento
    barra_x = max(0, min(barra_x, ancho - barra_ancho))
    # Dibujar la barra
    pygame.draw.rect(pantalla, (255, 255, 255), (barra_x, barra_y, barra_ancho, barra_alto))


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