from asyncio import events
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
        global screen
        screen = pygame.display.set_mode((win_width,win_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont('arial', 32)

        self.crown_spritesheet = spritesheet('img/crown.png')
        self.gameover_background = pygame.image.load('img/gameover.png')
        self.character_spritesheet = spritesheet('img/character.png')
        self.terrain_spritesheet = spritesheet('img/terrain.png')
        self.attack_spritesheet = spritesheet('img/attack.png')
        self.enemy_spritesheet = spritesheet('img/enemy.png')
        self.intro_background = pygame.image.load('img/introbackground.png')
        self.banana_spritesheet = spritesheet('img/Banana.png')


    def create_tilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == 'E':
                    Enemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "F":
                    Banana(self, j, i)
                if column == "C":
                    Crown(self, j, i)


    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.Banana = pygame.sprite.LayeredUpdates()
        self.Crown = pygame.sprite.LayeredUpdates()

        self.create_tilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - tilesize)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + tilesize)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - tilesize, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + tilesize, self.player.rect.y)


    def update(self):
        self.all_sprites.update()

    def draw(self):
        screen.fill(black)
        self.all_sprites.draw(screen)
        self.clock.tick(fps)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text = self.font.render('Git Gud', True, white)
        text_rect = text.get_rect(center=(win_width/2, win_height/2 - 50))

        restart_button = Button(260, win_height/2 + 10, 120, 50,'Try Again', white, black, 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            screen.blit(self.gameover_background, (0,0))
            screen.blit(text, text_rect)
            screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(fps)
            pygame.display.update()

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


            screen.blit(self.intro_background, (0,0))
            screen.blit(title, title_rect)
            screen.blit(play_button.image, play_button.rect)
            self.clock.tick(fps)
            pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()