import bombjack.sprites as sprites
import bombjack.settings as settings
import pygame

sWidth = settings.sWidth
sHeight = settings.sHeight

class Platform:
    def __init__(self, x, y, x2, y2):
        self.x = x
        self.y = y

        self.x2 = x2
        self.y2 = y2

        self.xDiff = x - x2
        self.yDiff = y - y2

        self.width = abs(x - x2)
        self.height = abs(y - y2)

        if self.xDiff > 0:
            self.x -= self.xDiff

        if self.yDiff > 0:
            self.y -= self.yDiff


        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.sprite = pygame.transform.scale(sprites.platform_spr, (self.width, self.height))

        

    def draw(self, window):
        window.blit(self.sprite, (self.x, self.y))
        