from os import kill
from re import M, T
from tkinter import W
from turtle import _Screen, Screen
from pip import main
import pygame
from config import *
import math
import random

screen = pygame.display.set_mode((win_height, win_width))
player_health = 50
max_health = 50
health_bar_length = 300
health_ratio = max_health / health_bar_length

class spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        return sprite

class Crown(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites, self.game.Crown
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.crown_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(black)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Banana(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = enemy_layer
        self.groups = self.game.all_sprites, self.game.Banana
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.banana_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(black)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Player(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = player_layer
        self.groups = self.game.all_sprites

        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*23
        self.y = y*33
        self.width = 23
        self.height = 33

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.kirito_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(white)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def get_damage(self,amount):
        global player_health
        if player_health > 0:
            player_health -= amount
        if player_health <= 0:
            self.kill()
            self.game.playing = False
            player_health = max_health

    def get_health(self,amount):
        global player_health
        if  player_health < max_health:
            player_health += amount
        if player_health >= max_health:
            player_health = max_health

    def collide_banana(self):
        hits = pygame.sprite.spritecollide(self, self.game.Banana, False)
        if hits:
            Player.get_health(self, 1)

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            Player.get_damage(self,2)

    def collide_crown(self):
        hits = pygame.sprite.spritecollide(self, self.game.Crown, False)
        if hits:
            self.game.playing = False

    def health_bar(self):
        pygame.draw.rect(screen,(255,0,0),(10,10,player_health/health_ratio,25))
        pygame.draw.rect(screen,(255,255,255),(10,10,health_bar_length,25),4)
        pygame.display.update()

    def update(self):
        self.movement()
        self.anime()
        self.collide_banana()
        self.collide_enemy()
        self.health_bar()
        self.collide_crown()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += player_speed
            self.x_change -= player_speed
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= player_speed
            self.x_change += player_speed
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += player_speed
            self.y_change -= player_speed
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= player_speed
            self.y_change += player_speed
            self.facing = 'down'

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += player_speed
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= player_speed
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += player_speed
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= player_speed
                    self.rect.y = hits[0].rect.bottom

    def anime(self):
        down_animations = [self.game.kirito_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.kirito_spritesheet.get_sprite(23, 0, self.width, self.height),
                           self.game.kirito_spritesheet.get_sprite(46, 0, self.width, self.height)]

        up_animations = [self.game.kirito_spritesheet.get_sprite(161, 0, self.width, self.height),
                         self.game.kirito_spritesheet.get_sprite(184, 0, self.width, self.height),
                         self.game.kirito_spritesheet.get_sprite(207, 0, self.width, self.height)]

        left_animations = [self.game.kirito_spritesheet.get_sprite(69, 0, self.width, self.height),
                            self.game.kirito_spritesheet.get_sprite(69, 0, self.width, self.height),
                           self.game.kirito_spritesheet.get_sprite(138, 0, self.width, self.height)]

        right_animations = [self.game.kirito_spritesheet.get_sprite(92, 0, self.width, self.height),
                            self.game.kirito_spritesheet.get_sprite(92, 0, self.width, self.height),
                            self.game.kirito_spritesheet.get_sprite(115, 0, self.width, self.height)]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.kirito_spritesheet.get_sprite(0, 0, self.width, self.height)
                self.image.set_colorkey(white)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.image.set_colorkey(white)
                self.animation_loop += 0.1
                if self.animation_loop > 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.kirito_spritesheet.get_sprite(161, 0, self.width, self.height)
                self.image.set_colorkey(white)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.image.set_colorkey(white)
                self.animation_loop += 0.1
                if self.animation_loop > 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.kirito_spritesheet.get_sprite(69, 0, self.width, self.height)
                self.image.set_colorkey(white)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.image.set_colorkey(white)
                self.animation_loop += 0.1
                if self.animation_loop > 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.kirito_spritesheet.get_sprite(115, 0, self.width, self.height)
                self.image.set_colorkey(white)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.image.set_colorkey(white)
                self.animation_loop += 0.1
                if self.animation_loop > 3:
                    self.animation_loop = 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = enemy_layer
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize
        
        self.facing = random.choice(['left', 'right', 'up'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(15, 45)

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(black)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.movement()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= enemy_speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['left', 'right', 'up', 'down'])

        if self.facing == 'right':
            self.x_change += enemy_speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['left', 'right', 'up', 'down'])

        if self.facing == 'up':
            self.y_change -= enemy_speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['left', 'right', 'up', 'down'])

        if self.facing == 'down':
            self.y_change += enemy_speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['left', 'right', 'up', 'down'])

    def animate(self):

        down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height)]

        up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]

        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
                self.image.set_colorkey(black)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop > 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height)
                self.image.set_colorkey(black)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop > 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height)
                self.image.set_colorkey(black)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop > 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height)
                self.image.set_colorkey(black)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop > 3:
                    self.animation_loop = 1

    def collide_blocks(self, direction):
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    self.facing = random.choice(['left'])
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    self.facing = random.choice(['right'])

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    self.facing = "up"
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    self.facing = "down"

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = block_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x*tilesize
        self.y = y*tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(320, 68, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ground_layer
        self.groups =  self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.terrain_spritesheet.get_sprite(300, 300, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    def __init__(self, x, y, width, height, content, fg, bg, fontsize):
        self.font = pygame.font.SysFont('arial', 32)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
               return True
            return False
        return False

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._Layer = player_layer
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = tilesize
        self.height = tilesize

        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.anime()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def anime(self):

        direction = self.game.player.facing
        
        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()



