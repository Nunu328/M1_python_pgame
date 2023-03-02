# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 14:11:19 2022

@author: white
"""
import pygame
from pygame.locals import *
import os
import random
import sys

WIDTH = 900
HEIGHT = int(WIDTH * 0.7)
SCR_RECT = Rect(0, 0, WIDTH, HEIGHT)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Invader final")
    
    # la musique
    Alien.hit_sound = load_sound("hit.wav")
    Player.shoot_sound = load_sound("shoot.wav")
    Player.explosion_sound = load_sound("explosion.wav")
    
    BGM = load_sound('background.wav')
    BGM.set_volume(0.2)
    BGM.play(-1)
    
    # Groupes
    all = pygame.sprite.RenderUpdates()
    aliens = pygame.sprite.Group()  # Aliens
    shots = pygame.sprite.Group()   # bullet
    beams = pygame.sprite.Group()   # beams
    Player.containers = all
    Shot.containers = all, shots
    Alien.containers = all, aliens
    Beam.containers = all, beams
    
    # image
    Back_image = load_image("BG.png")
    back_rect = Back_image.get_rect()
    Player.image = load_image("Player.png")
    Player.image = pygame.transform.scale(Player.image,(95,75))
    
    Shot.image = load_image("bullet.png")
    Alien.images = split_image(load_image("alien.png"), 0.5)

    Beam.image = load_image("ball.png")
    Beam.image = pygame.transform.scale(Beam.image,(35,15))
    

    # Player
    player = Player()
    # Aliens
    for i in range(0, 50):
        x = 20 + (i % 10) * 40
        y = 20 + (i - 25) * (i - 25) / 3
        Alien((x,y))
    
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        all.update()
        # bullet et alien touchent 
        collision_detection(player, aliens, shots, beams)
        all.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        screen.blit(Back_image, back_rect)

def collision_detection(player, aliens, shots, beams):
    # alien et bullet
    alien_collided = pygame.sprite.groupcollide(aliens, shots, True, True)
    for alien in list(alien_collided.keys()):
        Alien.hit_sound.play()
    # player et beams
    beam_collided = pygame.sprite.spritecollide(player, beams, True)
    if beam_collided:  
        Player.explosion_sound.play()

    # beams et bullet
    beam_collided = pygame.sprite.groupcollide(beams, shots, True, True)
    for beam in list(alien_collided.keys()):
        beam.hit_sound.play()


class Player(pygame.sprite.Sprite):

    speed = 5  # rapide
    reload_time = 15  
    def __init__(self):

        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCR_RECT.bottom
        self.reload_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        #Player bouge
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        elif keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        elif keys[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed)
        elif keys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed)
        self.rect.clamp_ip(SCR_RECT)
        # bullet
        if keys[pygame.K_SPACE]:
            if self.reload_timer > 0:
                self.reload_timer -= 1
            else:
                Player.shoot_sound.play()
                Shot(self.rect.center)  
                self.reload_timer = self.reload_time

class Alien(pygame.sprite.Sprite):
    speed = 2  
    animcycle = 18  
    frame = 0
    move_width = WIDTH - 250  
    prob_beam = 0.005
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.left = pos[0]
        self.right = self.left + self.move_width  
    def update(self):
        # BOUGER VERS WIGTH
        self.rect.move_ip(self.speed, 0)
        if self.rect.center[0] < self.left or self.rect.center[0] > self.right:
            self.speed = -self.speed
        # BEAM
        if random.random() < self.prob_beam:
            Beam(self.rect.center)
        # Animation
        self.frame += 1
        self.image = self.images[self.frame//self.animcycle%2]       

class Shot(pygame.sprite.Sprite):
    speed = 9  
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:  
            self.kill()

class Beam(pygame.sprite.Sprite):
    speed = 5  
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > SCR_RECT.height:
            self.kill()

def load_image(filename, colorkey=None):
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image:", filename)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image

def split_image(image, n):
    image_list = []
    w = image.get_width()
    h = image.get_height()
    w1 = w / n
    for i in range(0, w, 22):        
        surface = pygame.Surface((w1,h))
        surface.blit(image, (0,0), (i,0,w1,h))
        surface.set_colorkey(surface.get_at((0,0)), pygame.RLEACCEL)
        surface.convert()
        image_list.append(surface)
    return image_list

def load_sound(filename):
    filename = os.path.join("data", filename)
    return pygame.mixer.Sound(filename)

if __name__ == "__main__":

    main()