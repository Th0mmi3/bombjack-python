import bombjack.sprites as sprites
import bombjack.settings as settings
import pygame
import pathlib

package_path = pathlib.Path(__file__).parent

player_spr = pygame.image.load(package_path / 'img' / 'player.png')
player_invincible_spr = player_spr

bomb_spr = pygame.image.load(package_path / 'img' / 'bomb.png')
bomb_special_spr = pygame.image.load(package_path / 'img' / 'special_bomb.png')

platform_spr = pygame.image.load(package_path / 'img' / 'platform.png')

walker_spr = pygame.image.load(package_path / 'img' / 'walker.png')
ball_walker_spr = pygame.image.load(package_path / 'img' / 'walker_ball.png')

background_spr1 = pygame.image.load(package_path / 'img' / 'backgrounds' / 'bg_1.png')
background_spr2 = pygame.image.load(package_path / 'img' / 'backgrounds' / 'bg_2.png')
background_spr3 = pygame.image.load(package_path / 'img' / 'backgrounds' / 'bg_3.png')
background_spr4 = pygame.image.load(package_path / 'img' / 'backgrounds' / 'bg_4.png')
background_spr5 = pygame.image.load(package_path / 'img' / 'backgrounds' / 'bg_5.png')