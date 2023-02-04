import json
import os
import pathlib
import random
import sys
import time

import pygame
from pygame.locals import *

import bombjack

package_path = pathlib.Path(__file__).parent


class Game:
    def __init__(self, playerName):
        pygame.mixer.init()

        self.scene = 'game'
        self.died = False

        self.deathInit = True

        # Backgrounds
        self.backgrounds = [
            bombjack.sprites.background_spr1,
            bombjack.sprites.background_spr2,
            bombjack.sprites.background_spr3,
            bombjack.sprites.background_spr4,
            bombjack.sprites.background_spr5
        ]

        self.background = bombjack.sprites.background_spr1

        self.level = 1

        # Vars
        self.width = bombjack.sWidth
        self.height = bombjack.sHeight

        self.bombs = []
        self.platforms = []
        self.walkers = []
        self.entries = []

        self.playerName = playerName

        self.launch = True

        # Initialization
        self.player = bombjack.Player(playerName)
        self.scoreboard = bombjack.Scoreboard()

        # Temporary initialization
        self.start_ticks = 0

        pygame.font.init()
        self.font = pygame.font.Font(package_path / 'bombjack' / 'fonts' / 'bomb-jack.ttf', 16)

    def restartGame(self):
        ...

    def loadLevel(self, level):

        print(f"loading level: {level}")

        levelCount = len([entry for entry in os.listdir('levels') if os.path.isfile(os.path.join('levels', entry))])
        loadLevel = level % levelCount

        if loadLevel == 0:
            loadLevel = levelCount

        with open(f'levels\\{loadLevel}.json') as lvlFile:
            levelData = json.load(lvlFile)

        self.background = self.backgrounds[int(loadLevel) - 1]
        # print(int(levelCount) - 1)

        for bomb in levelData["bombs"]:
            self.bombs.append(bombjack.Bomb(bomb[0], bomb[1]))

        for platform in levelData["platforms"]:
            self.platforms.append(bombjack.Platform(platform[0], platform[1], platform[2], platform[3]))

        for walker in levelData["walkers"]:
            self.walkers.append(bombjack.Walker(walker[0], walker[1], self.platforms, level))

        specialBomb = random.choice(self.bombs)
        specialBomb.isSpecial = True

    def invincibleTimer(self, startTimer, time):

        if startTimer:
            self.player.invincible = True
            self.start_ticks = pygame.time.get_ticks()

        seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        if seconds > time:
            self.player.invincible = False

    def loseLive(self):
        if not self.player.invincible:
            for walker in self.walkers:
                if self.player.rect.colliderect(walker.rect):
                    self.player.lives -= 1

                    self.invincibleTimer(True, 2)

    def clearLevel(self):
        self.bombs = []
        self.platforms = []
        self.walkers = []

    def collision(self):
        # Check if player collides with bomb
        for bomb in self.bombs:
            if self.player.rect.colliderect(bomb.rect):
                self.bombs.remove(bomb)

                if bomb.isSpecial:
                    pygame.mixer.Channel(0).play(
                        pygame.mixer.Sound(package_path / 'bombjack' / 'sfx' / 'bomb_special.wav'))

                    self.player.score += 100

                    if len(self.bombs) > 0:
                        specialBomb = random.choice(self.bombs)
                        specialBomb.isSpecial = True

                else:
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound(package_path / 'bombjack' / 'sfx' / 'bomb.wav'))
                    # pygame.mixer.music.load(package_path / 'bombjack' / 'sfx' / 'bomb.wav')
                    # pygame.mixer.music.play()

                    self.player.score += 50

    def update(self, dt):
        self.invincibleTimer(False, 2)

        self.collision()

        self.player.move(dt)
        self.player.checkCollision(self.platforms)
        self.player.update(self.platforms)

        self.loseLive()

        for walker in self.walkers:
            walker.move(dt)
            walker.checkCollision()

        if self.player.lives <= 0 and self.died == False:  # Player died
            playerScore = {
                self.player.name: self.player.score
            }

            with open('leaderboard.json', 'r') as file:
                leaderboardData = json.load(file)

            if self.player.name in leaderboardData:
                if self.player.score > leaderboardData[self.player.name]:
                    leaderboardData[self.player.name] = self.player.score
            else:
                leaderboardData[self.player.name] = self.player.score

            with open('leaderboard.json', 'w') as file:
                json.dump(leaderboardData, file, indent=4)

            print(self.player.score)

            self.died = True
            self.clearLevel()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_r:
                    self.restartGame()

    def draw(self, screen):

        screen.fill((0, 0, 0))

        # Redrawing
        screen.blit(self.background, (0, bombjack.settings.GAME_CEILING))

        self.player.draw(screen)
        self.scoreboard.draw(screen, self.player.score)

        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(0, 60, 880, 15))
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(0, self.height - 60 - 20, 800, 15))

        for bomb in self.bombs:
            bomb.draw(screen)

        for platform in self.platforms:
            platform.draw(screen)

        for walker in self.walkers:
            walker.draw(screen)

        self.player.drawLives(screen)

        # Game over screen
        if self.died == True:
            screen.fill((0, 0, 0))

            if self.deathInit == True:
                with open('leaderboard.json', 'r') as file:
                    lbData = json.load(file)

                for count, item in enumerate(lbData.items()):
                    self.entries.append(bombjack.Entry(5, 5 + (count * 30), item[0], item[1], 200))

                self.deathInit = False

            for entry in self.entries:
                entry.draw(screen)

        pygame.display.flip()

    def run(self):
        # Initialise PyGame.
        pygame.init()

        fps = 165.0
        fpsClock = pygame.time.Clock()

        # Set up the window.
        screen = pygame.display.set_mode((self.width, self.height))

        if self.scene == 'game':
            self.loadLevel(self.level)

        # Main game loop.
        dt = 1 / fps  # dt is the time since last frame.

        while True:  # Loop forever!

            if self.scene == 'game':

                if self.launch is True:
                    self.launch = False
                    time.sleep(0.6)

                if len(self.bombs) == 0 and self.died is False:
                    self.level += 1
                    self.clearLevel()
                    self.loadLevel(self.level)
                    time.sleep(1)

                self.update(dt)  # You can update/draw here, I've just moved the code for neatness.
                self.draw(screen)

            dt = fpsClock.tick(fps)
