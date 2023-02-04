import bombjack.sprites as sprites
import bombjack.settings as settings
import pygame

sWidth = settings.sWidth
sHeight = settings.sHeight

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.sprite = pygame.transform.scale(sprites.bomb_spr, (self.width, self.height))
        self.sprite_special = pygame.transform.scale(sprites.bomb_special_spr, (self.width, self.height))

        self.isSpecial = False


    def draw(self, window):
        if self.isSpecial:
            window.blit(self.sprite_special, (self.x, self.y))

        else:
            window.blit(self.sprite, (self.x, self.y))

