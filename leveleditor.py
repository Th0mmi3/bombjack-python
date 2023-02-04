from re import template
import sys
import json
import pygame
from pygame.locals import *
import bombjack
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

width = bombjack.sWidth
height = bombjack.sHeight 

screen = pygame.display.set_mode((width, height))

background = bombjack.sprites.background_spr1

bombLocs = []
bombs = []

walkerLocs = []
walkers = []

platLocs = []
plats = []
tempPlat = []

level = {}

platPoint = 0

# Game loop.
while True:
  screen.fill((0, 0, 0))
  
  for event in pygame.event.get():
    if event.type == QUIT:
        pygame.quit()
        sys.exit()

    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        bombLocs.append(list((list(pos)[0] - 32/2, list(pos)[1] - 32/2)))
        bombs.append(bombjack.Bomb(list(pos)[0] - 32/2, list(pos)[1] - 32/2))
        print(bombLocs)
    """

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            level["bombs"] = bombLocs
            level["platforms"] = platLocs
            level["walkers"] = walkerLocs

            with open("level.json", "w") as outfile:
                json.dump(level, outfile, indent=4)

        if event.key == pygame.K_b:
            pos = pygame.mouse.get_pos()
            bombLocs.append(list((list(pos)[0] - 32/2, list(pos)[1] - 32/2)))
            bombs.append(bombjack.Bomb(list(pos)[0] - 32/2, list(pos)[1] - 32/2))

        if event.key == pygame.K_w:
            pos = pygame.mouse.get_pos()
            walkerLocs.append(list((list(pos)[0] - 32/2, list(pos)[1] - 32/2)))
            walkers.append(bombjack.Walker(list(pos)[0] - 32/2, list(pos)[1] - 32/2, 0, 1))

            print(walkers)


        if event.key == pygame.K_p:
            pos = pygame.mouse.get_pos()

            if platPoint == 0:
                tempPlat.append(pos[0])
                tempPlat.append(pos[1])
                platPoint = 1
            else:
                tempPlat.append(pos[0])
                tempPlat.append(pos[1])
                platLocs.append(tempPlat)

                platPoint = 0

                plats.append(bombjack.Platform(tempPlat[0], tempPlat[1], tempPlat[2], tempPlat[3]))


                tempPlat = []


    if event.type == QUIT:
        pygame.quit()
        sys.exit()
  
  # Update.
  
  # Draw.

  screen.blit(background, (0, bombjack.settings.GAME_CEILING))

  for bomb in bombs:
      bomb.draw(screen)

  for plat in plats:
      plat.draw(screen)

  for walker in walkers:
      walker.draw(screen)

  pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(0, 60, 880, 15))
  pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(0, height - 60 - 20, 800, 15))

  

  pygame.display.flip()
  fpsClock.tick(fps)