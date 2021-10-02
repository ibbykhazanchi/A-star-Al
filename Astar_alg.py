import pygame as pg
import random
import math
import sys
from os import path
from queue import PriorityQueue

#Define Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#Settings
WIDTH = 606
HEIGHT = 606
FPS = 60
TITLE = 'A* Visual Test'
BGCOLOR = WHITE

TILESIZE = 6
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = WIDTH / TILESIZE

#blocked path object
class Wall(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Game:
    def __init__(self):
        #initialize game window
        #initialize Pygame and create window
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        #location of folder in OS
        alg_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(alg_folder, 'onegraph.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)


    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == 'X':
                    Wall(self,col,row)


    def run(self):
        #Game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, BLACK, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, BLACK, (0, y), (WIDTH, y))

    def draw(self):
        #Game loop - Draw/Render
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        #draw grid to screen
        self.draw_grid()
        #***after*** drawing everything, flip the display
        pg.display.flip()

    def events(self):
        #Game loop - Process Input/Events
        for event in pg.event.get():
            #check for closing window
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

g = Game()
while True:
    g.new()
    g.run()

pg.quit()
