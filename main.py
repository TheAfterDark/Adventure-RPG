import enum
import pygame
from sprites import *
from config import *
from pygame.locals import *
from pygame import mixer
import sys

mixer.init()
mixer.music.load("background01.wav")
mixer.music.set_volume(0.3)
mixer.music.play(-1)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont('arial', 32)

        self.character_spritesheet = spritesheet('img/character.png')
        self.terrain_spritesheet = spritesheet('img/terrain.png')
        self.enemy_spritesheet = spritesheet('img/enemy.png')
        self.intro_background = pygame.image.load('img/introbackground.png')


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

    def healthy(self):
        health_bar = health(50, 50, 50, 200, 50)
        healthy = True
        while healthy:
            self.screen.blit(health_bar.image, health_bar.rect)
            pygame.display.update()

    def game_over(self):
        pass

    def intro_screen(self):
        intro = True

        title = self.font.render('Sword Art Offline', True, black)
        title_rect = title.get_rect(x=210, y=50)

        play_button = Button(260, 170, 100, 50, 'Play', white, black, 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False


            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(fps)
            pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
    g.healthy()
pygame.quit()
sys.exit()