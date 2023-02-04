import pygame
import bombjack.sprites as sprites
import bombjack.settings as settings
import time
import random
import math
import json

sWidth = settings.sWidth
sHeight = settings.sHeight

class Walker:
    def __init__(self, x, y, platforms, level):

        self.state = 'normal'
        self.ballInit = True

        self.spawnX = x
        self.spawnY = y
        
        self.x = x
        self.y = y

        self.width = 45
        self.height = 45
        
        self.constSpeed = 0.2 + (level * 0.1)
        self.speed = self.constSpeed

        self.constReturnTime = 0.002  # The higher the faster
        self.returnTime = 0.002  

        self.gravity = 0.1

        self.direction = 1

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.sprite = pygame.transform.scale(sprites.walker_spr, (self.width, self.height))
        self.ballSprite = pygame.transform.scale(sprites.ball_walker_spr, (self.width, self.height))

        self.platforms = platforms




    def checkPlatform(self):
        for platform in self.platforms:
            if self.y + 1 > platform.y and self.y + 1 < platform.y + platform.height:
                if self.x < platform.x:
                    self.direction = self.direction * -1
                if self.x > platform.x + platform.width:
                    self.direction = self.direction * -1

    def check_grounded(self):
        if (self.y + self.height) >= settings.GAME_FLOOR:
            return True

        for platform in self.platforms:
            if pygame.Rect(self.x, self.y, self.width, self.height + 1).colliderect(platform.rect):
                return True
                        
        return False

    def checkCollision(self):
        # Check floor
        if self.y + self.height > settings.GAME_FLOOR:
            self.y = settings.GAME_FLOOR - self.height
            
            # Respawn walker
            self.state = 'ball'

        # Check ceiling
        if self.y < settings.GAME_CEILING:
            self.y = settings.GAME_CEILING
        
        # Check left wall
        if self.x < 0:
            self.x = 0
        
        # Check right wall
        if self.x + self.width > sWidth:
            self.x = sWidth - self.width

        if self.state == 'normal':
            # Check platforms
            for platform in self.platforms:

                if self.y + self.height > platform.y and self.y < platform.y + platform.height:
                    if self.x > platform.x and self.x < platform.x + platform.width:

                        if self.y < platform.y:
                            self.y = platform.y - self.height
                        else:
                            self.y = platform.y + platform.height

                    elif self.x + self.width > platform.x and self.x < platform.x + platform.width:
                        if self.y < platform.y:
                            self.y = platform.y - self.height
                        else:
                            self.y = platform.y + platform.height


    def move(self, dt):
        if self.state == 'normal':
            self.returnTime = self.constReturnTime
            self.speed = self.constSpeed

            for platform in self.platforms:
                if not pygame.Rect(self.x, self.y, self.width, self.height + 1).colliderect(platform.rect):
                    self.speed = self.constSpeed / 3

            # Gravity
            if self.check_grounded() is False:
                self.y += self.gravity * dt

            randomNum = random.randint(0, 100)
            if randomNum == 50:
                self.direction = self.direction * -1

            self.x += self.speed * self.direction * dt

        if self.state == 'ball':

            if self.spawnX - 2 <= self.x <= self.spawnX + 2: 
                if self.spawnY - 2 <= self.y <= self.spawnY + 2:
                    self.state = 'normal'


            returnX = self.spawnX - self.x
            returnY = self.spawnY - self.y


            self.x += returnX * self.returnTime * dt
            self.y += returnY * self.returnTime * dt

            
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        #pygame.draw.rect(window, (255, 255, 0), self.rect, 2)

        if self.state == 'normal':
            window.blit(self.sprite, (self.x, self.y))
        else:
            window.blit(self.ballSprite, (self.x, self.y))