import pygame, random
import config as c
from player import Player
from titan import Titan
import sys 
import os # ¡NUEVO! Necesario para la gestión de rutas del fondo

pygame.init()
screen = pygame.display.set_mode((c.ANCHO_VENTANA, c.ALTO_VENTANA))
pygame.display.set_caption("Shingeki no Pygame")
clock = pygame.time.Clock()
font = pygame.font.SysFont(c.FONT_NAME, 20)

invul_time = 1000
start_time = pygame.time.get_ticks()

def draw_text(s, t, x, y, size=20, color=c.BLANCO):
    f = pygame.font.SysFont(c.FONT_NAME, size)
    s.blit(f.render(t, True, color), (x, y))


# -----------------------------------------
# SPAWN DE TITANES
# -----------------------------------------
def spawn_titans(level, player):
    titans = []
    cantidad = 5 + level // 2

    for _ in range(cantidad):
        t = Titan(level)

        safe_dist = 200
        # Asegura que el titán no aparezca justo encima del jugador
        while ((t.x - player.x) ** 2 + (t.y - player.y) ** 2) ** 0.5 < safe_dist:
            t.x = random.randint(0, c.ANCHO_VENTANA - t.size)
            t.y = random.randint(0, c.ALTO_VENTANA - t.size)

        titans.append(t)

    return titans

# --- NUEVO: CARGAR Y ESCALAR IMAGEN DE FONDO ---
# ASUME que la imagen está en la ruta: Proyecto/sprites/fondo_tierra_anime.jpg
try:
    FONDO_PATH = os.path.join(os.getcwd(), "sprites", "fondo_tierra_anime.jpg")
    background_image = pygame.image.load(FONDO_PATH).convert()
    # Escalar la imagen al tamaño de la ventana (800x600)
    background_image = pygame.transform.scale(background_image, (c.ANCHO_VENTANA, c.ALTO_VENTANA))
    USE_BACKGROUND = True
    print("Fondo cargado con éxito.")
except pygame.error:
    print("Advertencia: No se encontró la imagen de fondo 'fondo_tierra_anime.jpg' en la carpeta 'sprites'. Se usará un color sólido.")
    USE_BACKGROUND = False
# ---------------------------------------------


# -----------------------------------------
# MAIN
# -----------------------------------------
def main():

    run = True
    player = Player(c.ANCHO_VENTANA // 2, c.ALTO_VENTANA // 2)

    level = 1
    titans = spawn_titans(level, player)

    last_attack = 0
    cooldown = 0.25
    game_over = False

    # ---------------------------------
    # FUNCIONES DE AYUDAS DE DIBUJO
    # ---------------------------------
    def draw_circle_alpha(surface, color, center, radius):
        """Dibuja un círculo transparente (para el rango de ataque)"""
        temp = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp, color, (radius, radius), radius)
        surface.blit(temp, (center[0] - radius, center[1] - radius))

    # ========================================================
    # ==================== BUCLE PRINCIPAL ===================
    # ========================================================
    while run:
        dt = clock.tick(c.FPS) / 16

        # ---------------------------------------------
        #  CAPTURAR TODOS LOS EVENTOS EN UNA SOLA LISTA
        # ---------------------------------------------
        events = pygame.event.get() 
        
        for e in events:
            if e.type == pygame.QUIT:
                run = False

        # --------------- GAME OVER ---------------
        if game_over:
            screen.fill((0, 0, 0)) # Fondo negro

            # --- DIBUJAR TEXTO DE GAME OVER (CENTRADOS PERFECTAMENTE) ---
            
            # Título: "GAME OVER" (Grande y rojo)
            font_go = pygame.font.SysFont(c.FONT_NAME, 72)
            text_surf_go = font_go.render("GAME OVER", True, (255, 50, 50))
            # Usamos get_rect() y center para centrar automáticamente
            text_rect_go = text_surf_go.get_rect(center=(c.ANCHO_VENTANA // 2, c.ALTO_VENTANA // 2 - 100))
            screen.blit(text_surf_go, text_rect_go)

            # Nivel Final (Mediano)
            font_lvl = pygame.font.SysFont(c.FONT_NAME, 36)
            text_surf_lvl = font_lvl.render(f"Nivel Final: {level}", True, (200, 200, 200))
            # Centrado X en el medio de la pantalla
            text_rect_lvl = text_surf_lvl.get_rect(center=(c.ANCHO_VENTANA // 2, c.ALTO_VENTANA // 2))
            screen.blit(text_surf_lvl, text_rect_lvl)
            
            # Instrucciones (Pequeño)
            font_inst = pygame.font.SysFont(c.FONT_NAME, 24)
            text_surf_inst = font_inst.render("Pulsa ENTER para Reiniciar o ESC para Salir", True, (150, 150, 150))
            # Centrado X en el medio de la pantalla
            text_rect_inst = text_surf_inst.get_rect(center=(c.ANCHO_VENTANA // 2, c.ALTO_VENTANA // 2 + 50))
            screen.blit(text_surf_inst, text_rect_inst)
            
            pygame.display.flip() # Actualizar la pantalla de Game Over

            # Aquí también debes usar 'events' en lugar de un nuevo pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    run = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        player = Player(c.ANCHO_VENTANA // 2, c.ALTO_VENTANA // 2)
                        level = 1
                        titans = spawn_titans(level, player)
                        game_over = False
                    if e.key == pygame.K_ESCAPE:
                        run = False
            continue
        # ---------------------------------
        #        GAMEPLAY NORMAL
        # ---------------------------------

        keys = pygame.key.get_pressed()
        player.move(keys, dt)

        # ========== SISTEMA DE ATAQUE (Click de Mouse) ==========
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: # Clic izquierdo
                now = pygame.time.get_ticks() / 1000
                if now - last_attack >= cooldown:

                    rango = 250
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    objetivo = None
                    dist_min = 99999

                    for t in titans:
                        dist = ((t.x - player.x) ** 2 + (t.y - player.y) ** 2) ** 0.5

                        if dist <= rango: 
                            # Criterio del "Cono de ataque" (Producto punto)
                            # Vector al ratón (dirección de ataque)
                            dx_m = mouse_x - player.x
                            dy_m = mouse_y - player.y
                            # Vector al Titán
                            dx_t = t.x - player.x
                            dy_t = t.y - player.y
                            
                            # Producto punto (Si es positivo, el titán está frente al ratón)
                            dot = dx_m * dx_t + dy_m * dy_t

                            if dot > 0:
                                if dist < dist_min:
                                    dist_min = dist
                                    objetivo = t

                    if objetivo:
                        player.attack_titan(objetivo)
                        last_attack = now
        # ================================================

        # ACTUALIZAR TITANES
        for t in titans:
            t.update(player, dt)

        # Eliminar titanes muertos
        titans = [t for t in titans if not t.is_dead()]

        # SIGUIENTE NIVEL
        if not titans:
            level += 1
            titans = spawn_titans(level, player)
            player.gain_xp(120)

        # SI MUERE EL JUGADOR
        if player.is_dead():
            game_over = True

        # ---------------------------------
        #          DIBUJO
        # ---------------------------------
        
        # --- DIBUJAR FONDO (MODIFICADO) ---
        if USE_BACKGROUND:
            screen.blit(background_image, (0, 0)) # Dibujar la imagen de fondo escalada
        else:
            screen.fill((20, 20, 40)) # Fondo oscuro por defecto

        player_center = (player.x + player.width // 2, player.y + player.height // 2)

        # Dibujar rango de ataque (círculo rojo semi-transparente)
        draw_circle_alpha(screen, (255, 0, 0, 80), player_center, 250)

        for t in titans:
            t.draw(screen)

        player.draw(screen)

        # Interfaz de Usuario
        draw_text(screen, f"Nivel Jugador: {player.level} ({player.personaje})", 10, 10)
        draw_text(screen, f"XP: {player.xp}/{c.XP_PER_LEVEL}", 10, 30)
        draw_text(screen, f"Etapa: {level}", 10, 50)

        pygame.display.flip()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        pygame.quit()
        sys.exit()