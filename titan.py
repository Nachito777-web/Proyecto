import pygame, random
import config as c
import os 

class Titan:
    def __init__(self, level): 
        # --- NIVEL ---
        self.level = level

        # --- TAMAÑOS Y ESTADÍSTICAS ---
        # ¡CORRECCIÓN CLAVE! Aumentamos el tamaño base para que se vea bien.
        self.size = 120 + level * 6 
        self.speed = c.TITAN_BASE_SPEED + (level * 0.03)

        # --- VIDA ---
        self.base_health = int(c.TITAN_BASE_HEALTH * (1 + level * 0.2))
        self.max_health = self.base_health
        self.health = self.max_health
        self.display_health = float(self.health)

        # daño que hace el titán
        self.damage = int(c.TITAN_BASE_DAMAGE * (1 + level * 0.12))

        # --- POSICIÓN ALEATORIA ---
        self.x = random.randint(0, c.ANCHO_VENTANA - self.size)
        self.y = random.randint(0, c.ALTO_VENTANA - self.size)

        # --- SPRITE ---
        self.sprite = self.load_sprite()

        # --- TEXTO FLOTANTE (daño recibido) ---
        self.floating_text = []

    # -----------------------------------------
    # SPRITE (CARGA CON MANEJO DE RUTA Y ERROR)
    # -----------------------------------------
    def load_sprite(self):
        SPRITES_DIR = os.path.join(os.getcwd(), "sprites")
        
        # ... (código para construir titan_name y file_path) ...
        titan_name = c.TITAN_PURO_SPRITE_NAME 

        if self.level % 20 == 0 and self.level > 0:
            idx = (self.level // 20 - 1) % len(c.TITANES_CAMBIANTES)
            titan_name = c.TITANES_CAMBIANTES[idx]
            
        file_path = os.path.join(SPRITES_DIR, "titan", f"{titan_name}.png")

        try:
            # 1. Cargar la imagen
            loaded_sprite = pygame.image.load(file_path)
            
            # 2. Establecer el color blanco como clave de transparencia (R, G, B)
            # Asume que el color de fondo es blanco puro (255, 255, 255).
            loaded_sprite.set_colorkey((255, 255, 255))
            
            # 3. Optimizar y escalar la imagen con transparencia
            final_sprite = loaded_sprite.convert_alpha()
            
            # 4. Devolver la imagen escalada
            return pygame.transform.scale(final_sprite, (self.size, self.size))
            
        except pygame.error:
            # 2. PLACEHOLDER (Si el archivo no se encuentra o es un cambiante sin sprite)
            print(f"Advertencia: No se encontró el sprite para el Titán: {file_path}. Usando placeholder.")
            surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            surf.fill((140, 40, 40, 255)) 
            # Barra verde para nuca 
            pygame.draw.rect(surf, (0, 200, 0), (self.size // 4, 0, self.size // 2, self.size // 6))
            return surf

    # -----------------------------------------
    # COLLISION RECT
    # -----------------------------------------
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    # -----------------------------------------
    # MOVIMIENTO HACIA EL JUGADOR
    # -----------------------------------------
    def update(self, player, dt):
        px = player.x + player.width / 2
        py = player.y + player.height / 2

        dx = px - self.x
        dy = py - self.y
        dist = max(1, (dx * dx + dy * dy) ** 0.5)

        self.x += (dx / dist) * self.speed * dt
        self.y += (dy / dist) * self.speed * dt

        # dañar jugador si lo toca
        if self.rect().colliderect(player.rect()):
            if self.rect().colliderect(player.rect()):
                player.take_damage(self.damage)

    # -----------------------------------------
    # RECIBIR DAÑO
    # -----------------------------------------
    def take_damage(self, dmg):
        self.health -= dmg
        if self.health < 0:
            self.health = 0

        self.add_floating_text(dmg)

    def is_dead(self):
        return self.health <= 0

    # -----------------------------------------
    # TEXTO FLOTANTE (daño recibido)
    # -----------------------------------------
    def add_floating_text(self, dmg):
        self.floating_text.append({
            "text": f"-{dmg}",
            "x": self.x + self.size / 2,
            "y": self.y - 10,
            "alpha": 255,
            "offset": 0
        })

    # -----------------------------------------
    # DRAW (sprite + barra + daño flotante)
    # -----------------------------------------
    def draw(self, screen):

        # sprite del titán
        screen.blit(self.sprite, (self.x, self.y))

        # --- ANIMACIÓN DE BARRA ---
        speed = 0.1
        if self.display_health > self.health:
            self.display_health -= (self.display_health - self.health) * speed
        else:
            self.display_health = self.health

        # --- BARRA DE VIDA ---
        bar_width = 70 if self.level % 20 == 0 else 60
        bar_height = 8

        hp_percent = self.display_health / self.max_health
        hp_width = int(bar_width * hp_percent)

        bar_x = self.x - 10
        bar_y = self.y - 15

        # fondo
        pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height))

        # color dinámico
        if hp_percent > 0.6:
            color = (50, 255, 50)  # verde
        elif hp_percent > 0.3:
            color = (255, 200, 30)  # amarillo
        else:
            color = (255, 50, 50)  # rojo

        pygame.draw.rect(screen, color, (bar_x, bar_y, hp_width, bar_height))

        # borde
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)

        # --- TEXTO FLOTANTE ---
        for ft in self.floating_text[:]:
            font = pygame.font.SysFont(None, 22)
            surf = font.render(ft["text"], True, (255, 50, 50))
            surf.set_alpha(ft["alpha"])

            screen.blit(surf, (ft["x"], ft["y"] - ft["offset"]))

            ft["offset"] += 0.6
            ft["alpha"] -= 4

            if ft["alpha"] <= 0:
                self.floating_text.remove(ft)