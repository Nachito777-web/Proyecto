import pygame

class Equipamiento:
    def __init__(self):
        self.tipo = "blades"
        self.folder = "assets/player/equip/"

        self.imagenes = {
            "blades": pygame.image.load(self.folder + "blades.png").convert_alpha(),
            "thunderspear": pygame.image.load(self.folder + "thunderspear.png").convert_alpha()
        }

    def set_equip(self, tipo):
        if tipo in self.imagenes:
            self.tipo = tipo

    def draw(self, screen, player_rect):
        img = self.imagenes[self.tipo]
        screen.blit(img, (player_rect.x - 5, player_rect.y + 10))