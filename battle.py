import pygame
import random, os.path
from pygame.locals import *

import time
import random

pygame.init()


MAX_SHOTS      = 2      #most player bullets onscreen
ROCK_ODDS     = 22     #chances a new alien appears
BOMB_ODDS      = 60    #chances a new bomb will drop
ROCK_RELOAD   = 12     #frames between new aliens
SCREENRECT     = Rect(0, 0, 1280, 720)
SCORE          = 0



pygame.display.set_caption('Battle in Air')
clock = pygame.time.Clock()



black=(0,0,0)
DARKGREEN=(0,50,0)

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

class Player(pygame.sprite.Sprite):
    speed = 10
    bounce = 24
    gun_offset = -11
    images = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1
        self.movey = 0
        self.frame = 0

    def move(self, direction):
        if direction: self.facing = direction
        self.rect.move_ip(direction*self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
        self.rect.top = self.origtop - (self.rect.left//self.bounce%2)

    def movev(self, y):
        self.movey += y

    def update(self):
        self.rect.y = self.rect.y + self.movey

class Rock(pygame.sprite.Sprite):
    speed = 1
    animcycle = 2
    images = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.facing = random.choice((-1,1)) * Rock.speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = SCREENRECT.right

    def update(self):
        self.rect.move_ip(self.facing, 10)
        if not SCREENRECT.contains(self.rect):
            self.facing = -self.facing;
            #self.rect.top = self.rect.bottom + 1
            #self.rect = self.rect.clamp(SCREENRECT)
        # self.frame = self.frame + 1
        # self.image = self.images[self.frame//self.animcycle%3]





class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('white')
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, 450)

    def update(self):
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, 0, self.color)


def crash():
    pass#message_display('You Crashed')


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



        mouse= pygame.mouse.get_pos()

        #print(mouse)


        pygame.display.update()
        clock.tick(15)
        intro = False


def game_loop():
    # Set the display mode
    background = pygame.Surface(SCREENRECT.size)
    background.fill(DARKGREEN)
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    rocks = pygame.sprite.Group()
    x_change = 0
    img = load_image('plane.png')
    Player.images = [img, pygame.transform.flip(img, 1, 0)]
    img = load_image('blockade image.png')  
    Rock.images= [img, pygame.transform.flip(img, 1, 0)]
    all = pygame.sprite.RenderUpdates()
    Player.containers = all
    Rock.containers = rocks, all
    Score.containers = all

    global score
    rockreload = ROCK_RELOAD
    kills = 0
    clock = pygame.time.Clock()
    global SCORE
    player = Player()

    gameExit = False


    while player.alive():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_UP:
                    player.movev(-20)
                if event.key == pygame.K_DOWN:
                    player.movev(20)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        keystate = pygame.key.get_pressed()
        # clear/erase the last drawn sprites
        screen.fill(DARKGREEN)
        all.clear(screen, background)

        # update all the sprites
        all.update()

        # handle player input
        direction = keystate[K_RIGHT] - keystate[K_LEFT]
        player.move(direction)

        #directionv = keystate[K_UP] - keystate[K_DOWN]
        #player.movev(directionv)
        player.update()


        # Create new rocks
        if rockreload:
            rockreload = rockreload - 1
        elif not int(random.random() * ROCK_ODDS):
            Rock()
            rockreload = ROCK_RELOAD
            #drav the scene
        dirty = all.draw(screen)
        pygame.display.update(dirty)




#game_intro()
game_loop()
pygame.quit()
quit()