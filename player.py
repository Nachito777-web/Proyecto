import pygame
import config as c # Usamos 'config' por las correcciones de errores previas. Si tu archivo de constantes se llama 'constantes.py', cámbialo a 'import constantes as c'
import os
import random

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # TAMAÑO DEL SPRITE (AUMENTADO A 60x60 para que se vea más grande)
        self.width = 80
        self.height = 100

        # movimiento
        self.speed = c.PLAYER_SPEED

        # stats
        self.level = 1
        self.xp = 0
        self.max_health = c.PLAYER_BASE_HEALTH
        self.health = self.max_health
        self.damage = c.PLAYER_BASE_DAMAGE

        # personaje inicial
        self.personaje = c.PERSONAJES_104[0] # Empezamos con el primer personaje de la lista

        # --- GESTIÓN DE SPRITE: Se carga y ESCALA inmediatamente ---
        self.sprite = self.load_player_sprite() 

        # Texto flotante (daño recibido)
        self.floating_text = []

    # ---------------------------------------------
    # CARGAR SPRITE DEL JUGADOR (AHORA CON ESCALADO)
    # ---------------------------------------------
    def load_player_sprite(self):
        # Construye la ruta de manera segura: /ruta/actual/sprites/player/Personaje.png
        SPRITES_DIR = os.path.join(os.getcwd(), "sprites", "player")
        file_name = f"{self.personaje}.png"
        file_path = os.path.join(SPRITES_DIR, file_name)
        
        try:
            # 1. Cargar la imagen con transparencia
            image = pygame.image.load(file_path).convert_alpha()
            # 2. ESCALAR la imagen al tamaño definido (self.width, self.height)
            return pygame.transform.scale(image, (self.width, self.height))
        except pygame.error:
            # Placeholder temporal si el archivo no se encuentra
            print(f"Advertencia: No se encontró el sprite de jugador: {file_path}. Usando placeholder azul.")
            surf = pygame.Surface((self.width, self.height))
            surf.fill((60, 150, 255))
            return surf
            
    # ---------------------------------------------
    # CAMBIAR PERSONAJE/ACTUALIZAR SPRITE
    # ---------------------------------------------
    def set_personaje(self, new_personaje_name):
        self.personaje = new_personaje_name
        self.sprite = self.load_player_sprite() # Recarga el sprite (escalado)

    # ---------------------------------------------
    # RECT (colisión)
    # ---------------------------------------------
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    # ---------------------------------------------
    # MOVIMIENTO
    # ---------------------------------------------
    # ---------------------------------------------
    # MOVIMIENTO
    # ---------------------------------------------
    def move(self, keys, dt): # <--- ¡Añadimos dt aquí!
        
        # El movimiento ahora se multiplica por dt
        # Si dt es 16 (FPS 60), el movimiento es normal. Si baja el FPS, el movimiento se mantiene.
        movement_amount = self.speed * dt
        
        if keys[pygame.K_w]:
            self.y -= movement_amount
        if keys[pygame.K_s]:
            self.y += movement_amount
        if keys[pygame.K_a]:
            self.x -= movement_amount
        if keys[pygame.K_d]:
            self.x += movement_amount
            
        # límites pantalla
        self.x = max(0, min(self.x, c.ANCHO_VENTANA - self.width))
        self.y = max(0, min(self.y, c.ALTO_VENTANA - self.height))

    # ---------------------------------------------
    # ATAQUE AL TITÁN
    # ---------------------------------------------
    def attack_titan(self, titan):
        titan.take_damage(self.damage)

    # ---------------------------------------------
    # RECIBIR DAÑO
    # ---------------------------------------------
    def take_damage(self, dmg):
        self.health -= dmg
        if self.health < 0:
            self.health = 0

    # ---------------------------------------------
    # SUBIR DE NIVEL
    # ---------------------------------------------
    def gain_xp(self, amount):
        self.xp += amount

        while self.xp >= c.XP_PER_LEVEL:
            self.xp -= c.XP_PER_LEVEL
            self.level += 1

            # mejoras al subir nivel
            self.max_health += 10
            self.damage += 3
            self.health = self.max_health

            # cambiar personaje cada 3 niveles
            idx = min(self.level // 3, len(c.PERSONAJES_104)-1)
            new_personaje = c.PERSONAJES_104[idx]
            
            if new_personaje != self.personaje:
                self.set_personaje(new_personaje) # Recarga el sprite

    # ---------------------------------------------
    # ESTADO MUERTO
    # ---------------------------------------------
    def is_dead(self):
        return self.health <= 0

    # ---------------------------------------------
    # DIBUJAR PLAYER
    # ---------------------------------------------
    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
        
        # Barra de vida
        hp_ratio = self.health / self.max_health
        bar_width = self.width
        bar_height = 5
        
        # Color dinámico
        if hp_ratio > 0.6:
            color = (50, 255, 50)  # verde
        elif hp_ratio > 0.3:
            color = (255, 200, 30)  # amarillo
        else:
            color = (255, 50, 50)  # rojo

        # Fondo de la barra
        pygame.draw.rect(screen, (30, 30, 30), (self.x, self.y - 10, bar_width, bar_height))
        # Nivel de vida
        pygame.draw.rect(screen, color, (self.x, self.y - 10, bar_width * hp_ratio, bar_height))
        # Borde
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y - 10, bar_width, bar_height), 1)

        # Texto flotante (daño recibido)
        font = pygame.font.SysFont(c.FONT_NAME, 16)
        
        # Mover y limpiar texto flotante
        self.floating_text = [
            t for t in self.floating_text if t['timer'] > 0
        ]
        
        for t in self.floating_text:
            t['timer'] -= 1
            t['y'] -= 0.5 # Subir lentamente
            
            text_surf = font.render(t['text'], True, t['color'])
            # Oscurecer texto con el tiempo
            alpha = int(255 * (t['timer'] / 60))
            text_surf.set_alpha(alpha)
            screen.blit(text_surf, (t['x'] - text_surf.get_width() // 2, t['y']))
#Revisa estos puntos antes de ejecutar:

#1.  Asegúrate de que tu carpeta de sprites esté en la ruta correcta: **`Proyecto/sprites/player/`**.
#2.  Si tu archivo de constantes se llama `constantes.py`, asegúrate de que la línea de importación diga **`import constantes as c`** (aunque en el código de arriba está como `config`, puedes cambiarlo para que coincida con tu nombre de archivo).

#¡Debería funcionar ahora! Dime si el tamaño es correcto.