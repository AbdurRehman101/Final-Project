import pygame,sys,random,math,time

pygame.init()

ShootSound = pygame.mixer.Sound('shooting.WAV')
ShipSound = pygame.mixer.Sound('thrust.ogg')
ExplosionSound = pygame.mixer.Sound('explod.WAV')
pygame.mixer.music.load('trektheme.ogg')
