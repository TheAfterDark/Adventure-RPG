import enum
import pygame
from sprites import *
from config import *
from pygame.locals import *
from pygame import mixer
import sys

mixer.init()
mixer.music.load("background.wav")
mixer.music.play(-1)

class Game:
    def __init__(self):
        pygame.init
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = spritesheet('img/character.png')
        self.terrain_spritesheet = spritesheet('img/terrain.png')
        self.enemy_spritesheet = spritesheet('img/enemy.png')


    def create_tilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == 'E':
                    Enemy(self, j, i)
                if column == "P":
                    Player(self, j, i)
                


    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_tilemap()





    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        self.clock.tick(fps)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass


g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()