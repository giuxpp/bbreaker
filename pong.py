import pygame
import sys
import math

# Configuración de pantalla
ancho, alto = 1200, 800
pantalla, reloj = None, None

# Variables globales
terminar_programa = False
logs_activados = True
game_over = False  # Variable para controlar el estado del juego

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
barra_punched = False

# Variables posición de la Pelota
bola_radio = 10
bola_centro = (ancho // 2, alto // 2)
bola_color = (255, 0, 0)  # Color de la pelota
bola_angulo = 45  # Ángulo de movimiento de la pelota (en grados)
bola_rapida = 10  # Velocidad de la pelota al ser golpeada
bola_despacio = 5  # Velocidad de la pelota al no ser golpeada
bola_step = bola_despacio  # Paso de movimiento de la pelota

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

def mover_en_direccion(centro, angulo_grados, distancia):
    angulo_rad = math.radians(angulo_grados)
    x, y = centro
    nuevo_x = x + math.cos(angulo_rad) * distancia
    nuevo_y = y + math.sin(angulo_rad) * distancia
    return (nuevo_x, nuevo_y)

# Inicializar Pygame
def pygame_config():
    global ancho, alto, pantalla, reloj
    pygame.init()
    reloj = pygame.time.Clock()    
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Pong Game - By Giuxpp")

def game_init():
    global ancho, alto, bola_centro, barra_ancho, barra_y_def, game_over, bola_step
    bola_centro = (ancho // 2, alto // 2)
    barra_x = (ancho - barra_ancho) // 2
    barra_y = barra_y_def
    game_over = False  # Reiniciar el juego al presionar Enter
    bola_step = bola_despacio

# Manejador de eventos del juego
# Captura eventos de teclado y cierre de ventana
# Actualiza la posición de la barra según las teclas presionadas
def manejador_eventos():
    global barra_step, desaceleracion, desacel_cntr, barra_punched
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:                
                game_init()
            elif event.key == pygame.K_ESCAPE:
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
                barra_punched = True
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
                barra_punched = False
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

def colision_circulo_rect(cx, cy, radio, rect):
    # Verifica si un círculo colisiona con un rectángulo
    # cx, cy: coordenadas del centro del círculo
    # radio: radio del círculo
    # rect: objeto rectángulo de Pygame (pygame.Rect)
    # Si el rect no es un objeto Rect, retorna False
    if not isinstance(rect, pygame.Rect):
        log("Error: El rectángulo debe ser un objeto pygame.Rect")
        return False
    # Encuentra el punto más cercano del rect al círculo
    punto_mas_cercano_x = max(rect.left, min(cx, rect.right))
    punto_mas_cercano_y = max(rect.top,  min(cy, rect.bottom))
    # Calcula distancia entre el centro del círculo y ese punto
    dx = cx - punto_mas_cercano_x
    dy = cy - punto_mas_cercano_y
    return (dx*dx + dy*dy) < (radio*radio)

def dibujar_bola():
    global bola_centro, bola_radio, bola_color, bola_angulo, game_over, bola_step, bola_despacio
    # Mover la bola en una dirección arbitraria
    bola_centro = mover_en_direccion(bola_centro, bola_angulo, bola_step)  # Mover la bola en una dirección arbitraria
    # Limitar la bola dentro de los bordes de la pantalla
    bola_centro = (
        max(bola_radio, min(bola_centro[0], ancho - bola_radio)),
        max(bola_radio, min(bola_centro[1], alto - bola_radio))
    )
    # Si la bola toca un borde de la pantalla, invertir su dirección
    if bola_centro[0] <= bola_radio or bola_centro[0] >= ancho - bola_radio:
        # Invertir la dirección de la bola sentido horizontal
        bola_angulo = (180 - bola_angulo) % 360
    if bola_centro[1] <= bola_radio or bola_centro[1] >= alto - bola_radio:
        # Invertir la dirección de la bola sentido vertical
        bola_angulo = (-bola_angulo) % 360
    # Terminar el juego si la bola toca el borde inferior
    if bola_centro[1] >= alto - bola_radio: game_over = True 
    # Dibujar la bola
    pygame.draw.circle(pantalla, bola_color, bola_centro, bola_radio)

def bola_colision_barra():
    global bola_centro, bola_radio, barra_x, barra_y, barra_ancho, barra_alto, bola_angulo, bola_step, bola_rapida, bola_despacio, barra_punched
    # Comprobar si la bola colisiona con la barra
    if colision_circulo_rect(bola_centro[0], bola_centro[1], bola_radio, pygame.Rect(barra_x, barra_y, barra_ancho, barra_alto)):
        # Invertir la dirección de la bola al colisionar con la barra
        bola_angulo = (-bola_angulo) % 360
        log("Colisión detectada entre la bola y la barra.")
        # Ajustar la posición 'y' de la bola al colisionar, para que no se quede pegada a la barra
        bola_centro = (bola_centro[0], barra_y - bola_radio)
        # Si la barra fue golpeada con fuerza, aumentar la velocidad de la bola
        if barra_punched:
            bola_step = bola_rapida
            log("Bola golpeada con fuerza.")            
        # Si la barra fue golpeada suavemente, mantener la velocidad normal
        else:        
            bola_step = bola_despacio
            log("Bola golpeada suavemente.")
        log("Barra_Punched: " + str(barra_punched))

def game_over_display():
    global game_over
    # Crear fuente
    fuente = pygame.font.SysFont(None, 80)  # None usa la fuente por defecto, 80 es el tamaño
    # Renderizar el texto
    texto = fuente.render("GAME OVER", True, (255, 0, 0))  # Texto rojo
    rect_texto = texto.get_rect(center=(ancho // 2, alto // 2))  # Centrado
    # Mostrar pantalla con texto
    pantalla.fill((0, 0, 0))              # Fondo negro
    pantalla.blit(texto, rect_texto)      # Dibujar texto
    pygame.display.flip()                 # Actualizar pantalla
    # Esperar unos segundos antes de salir
    while game_over:        
        manejador_eventos()

# Función principal del juego
def main():
    global game_over
    game_init() # Inicializar el juego (variables globales etc)
    pygame_config()  # Configurar Pygame
    log("Pygame inicializado correctamente.")
    log(f"Resolución de pantalla: {ancho}x{alto}")

    # Bucle principal del juego
    while True:
        # Manejo de eventos
        manejador_eventos()
        bola_colision_barra()

        # Actualizar estado del juego aquí
        if game_over: game_over_display()           

        pantalla.fill((0, 0, 0))  # Fondo negro

        # Dibujar barra tomando en cuenta su movimiento
        dibujar_barra()
        # Dibujar la pelota tomando en cuenta su movimiento y rebotes con el borde de la pantalla
        dibujar_bola()
        pygame.display.flip()     # Mostrar todo en pantalla
        reloj.tick(60)            # Limita a 60 FPS

if __name__ == "__main__":
    main()