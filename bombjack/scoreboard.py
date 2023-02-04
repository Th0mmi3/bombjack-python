import pygame
import pathlib

package_path = pathlib.Path(__file__).parent

class Scoreboard:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font(package_path / 'fonts' / 'bomb-jack.ttf', 16)

    def draw(self, window, score):
        scoreNum = self.font.render(str(score), False, (255, 255, 255))
        scoreTxt = self.font.render('SCORE', False, (40, 40, 255))

        window.blit(scoreTxt, (0, 5))
        window.blit(scoreNum, (120, 5))

class Entry:
    def __init__(self, x, y, entryName, entryScore, wordDistance):
        self.x = x
        self.y = y

        self.wordDistance = wordDistance

        self.entryName = str(entryName).upper()
        self.entryScore = str(entryScore)

        pygame.font.init()
        self.font = pygame.font.Font(package_path / 'fonts' / 'bomb-jack.ttf', 16)

    def draw(self, window):

        name = self.font.render(self.entryName, False, (0, 255, 255))
        score = self.font.render(self.entryScore, False, (255, 255, 255))

        window.blit(name, (self.x, self.y))
        window.blit(score, (self.x + self.wordDistance, self.y))



        