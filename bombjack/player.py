import bombjack.sprites as sprites
import bombjack.settings as settings
import controls.controls as controls

import pygame
import numpy as np

sWidth = settings.sWidth
sHeight = settings.sHeight


class Player:
    def __init__(self, playerName):
        self.position = np.array([0, 0])
        self.movement = np.array([0, 0])

        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

        self.constGravity = 0.5

        self.gravity = 0.5
        self.speed = 0.5

        self.maxJumpPower = 800
        self.jumpPower = 30

        self.isGrounded = False

        self.sprite = pygame.transform.scale(sprites.player_spr, (self.width, self.height))

        self.score = 0

        self.levelPlatforms = []

        self.lives = 10

        self.invincible = False

        self.name = str(playerName).lower()

        self.controller = controls.XboxController()

    def update(self, levelPlatforms):
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

        self.levelPlatforms = levelPlatforms

    def check_grounded(self):
        if (self.position[1] + self.height) >= settings.GAME_FLOOR:
            return True

        for platform in self.levelPlatforms:
            if pygame.Rect(self.position[0], self.position[1], self.width, self.height + 1).colliderect(platform.rect):
                return True

        return False

    def drawLives(self, window):
        for i in range(self.lives):
            window.blit(self.sprite, (i * self.width, sHeight - self.height))

    def checkCollision(self, platforms):
        # Check floor
        if self.position[1] + self.height > settings.GAME_FLOOR:
            self.position[1] = settings.GAME_FLOOR - self.height

        # Check ceiling
        if self.position[1] < settings.GAME_CEILING:
            self.position[1] = settings.GAME_CEILING

        # Check left wall
        if self.position[0] < 0:
            self.position[0] = 0

        # Check right wall
        if self.position[0] + self.width > sWidth:
            self.position[0] = sWidth - self.width

        # Check platforms
        for platform in platforms:

            if self.position[1] + self.height > platform.y and self.position[1] < platform.y + platform.height:
                if self.position[0] > platform.x and self.position[0] < platform.x + platform.width:

                    if self.position[1] < platform.y:
                        self.position[1] = platform.y - self.height
                    else:
                        self.position[1] = platform.y + platform.height

                elif self.position[0] + self.width > platform.x and self.position[0] < platform.x + platform.width:
                    if self.position[1] < platform.y:
                        self.position[1] = platform.y - self.height
                    else:
                        self.position[1] = platform.y + platform.height

    def draw(self, window):
        if self.invincible == True:
            self.sprite.set_alpha(100)
            window.blit(self.sprite, (self.position[0], self.position[1]))
        else:
            self.sprite.set_alpha(250)
            window.blit(self.sprite, (self.position[0], self.position[1]))

    def addVelocity(self, xVel, yVel):
        self.movement[0] += xVel
        self.movement[1] += yVel

    def move(self, dt):

        userInput = pygame.key.get_pressed()
        controllerInput = self.controller.get_directions()

        if userInput[pygame.K_w] or userInput[pygame.K_UP] or 1 in controllerInput:
            if self.jumpPower > 0:
                self.addVelocity(0, (-self.speed - self.gravity) * dt)
                self.jumpPower -= 1 * dt

        if userInput[pygame.K_a] or userInput[pygame.K_LEFT] or 2 in controllerInput:
            self.addVelocity(-self.speed * dt, 0)

        if userInput[pygame.K_s] or userInput[pygame.K_DOWN] or 3 in controllerInput:
            self.addVelocity(0, self.speed * dt)

        if userInput[pygame.K_d] or userInput[pygame.K_RIGHT] or 4 in controllerInput:
            self.addVelocity(self.speed * dt, 0)

        if userInput[pygame.K_SPACE] or 5 in controllerInput:
            self.gravity = self.constGravity / 2.4
        else:
            self.gravity = self.constGravity

        if self.check_grounded():
            self.jumpPower = self.maxJumpPower

        # Gravity
        if self.check_grounded() is False:
            self.movement[1] += self.gravity * dt

        # Add movement
        self.position += self.movement

        # Clear movement
        self.movement = np.array([0, 0])
