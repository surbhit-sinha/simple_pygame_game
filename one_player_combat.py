'''
Simple 1 player combat game to understanding pygame fundamentals.
'''

import pygame
import random

# Rectangle Parameters
#[width,height]
size = (520,480)
done = False # Loop until the user clicks the close button.
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
score = 0

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5        # velocity of movement
        # For jumping
        self.isJumping = False
        self.jumpCount = 10
        self.left = True
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x+17, self.y+11, 29, 52)
        self.health = 10
        self.visible = True
        self. hitCount = 0

    def draw(self, win):
        if self.visible:
            if (self.walkCount + 1) >= 27:
                self.walkCount = 0
            if not(self.standing):
                if self.left:
                    win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
            else:
                if self.right:
                    win.blit(walkRight[0], (self.x, self.y))
                else:
                    win.blit(walkLeft[0], (self.x, self.y))
                self.walkCount = 0
            self.hitbox = (self.x+17, self.y+11, 29, 52)
            pygame.draw.rect(win, RED, (self.hitbox[0], self.hitbox[1]-20, 50, 10))
            pygame.draw.rect(win, GREEN, (self.hitbox[0], self.hitbox[1]-20, 50 - (5*(10-self.health)), 10))    
            #pygame.draw.rect(win, RED, self.hitbox, 2)

    def hit(self):
        self.health -= 2
        self.hitCount += 1
        self.isJumping = False
        self.jumpCount = 10
        i = 0
        if (self.hitCount < 6):
            font1 = pygame.font.SysFont('comicsans', 100)
            text = font1.render('Oops', 1, RED)
            win.blit(text, (250 - (text.get_width()/2), 200))
            self.x = 60
            self.y = 410
            pygame.display.update()
            while i < 300:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        i = 301
                        pygame.quit()
        else:
            self.visible = False
            font2 = pygame.font.SysFont('comicsans', 100)
            text2 = font2.render('YOU LOST!!', 1, RED)
            win.blit(text2, (250 - (text2.get_width()/2), 200))
            pygame.display.update()
            global done
            done = True
            while i < 300:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        i = 301
                        pygame.quit()

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8*facing
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('images/R1E.png'), pygame.image.load('images/R2E.png'), pygame.image.load('images/R3E.png'), pygame.image.load('images/R4E.png'), pygame.image.load('images/R5E.png'), pygame.image.load('images/R6E.png'), pygame.image.load('images/R7E.png'), pygame.image.load('images/R8E.png'), pygame.image.load('images/R9E.png'), pygame.image.load('images/R10E.png'), pygame.image.load('images/R11E.png')]
    walkLeft = [pygame.image.load('images/L1E.png'), pygame.image.load('images/L2E.png'), pygame.image.load('images/L3E.png'), pygame.image.load('images/L4E.png'), pygame.image.load('images/L5E.png'), pygame.image.load('images/L6E.png'), pygame.image.load('images/L7E.png'), pygame.image.load('images/L8E.png'), pygame.image.load('images/L9E.png'), pygame.image.load('images/L10E.png'), pygame.image.load('images/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x+17, self.y+2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if (self.walkCount + 1) >= 33:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x+17, self.y+2, 31, 57)
            pygame.draw.rect(win, RED, (self.hitbox[0], self.hitbox[1]-20, 50, 10))
            pygame.draw.rect(win, GREEN, (self.hitbox[0], self.hitbox[1]-20, 50 - (5*(10-self.health)), 10))

    def move(self):
        if (self.vel > 0):
            if (self.x + self.vel < self.path[1]):
                self.x += self.vel
            else:
                self.vel = self.vel * (-1)
                self.walkCount = 0
        else:
            if (self.x - self.vel > self.path[0]):
                self.x += self.vel
            else:
                self.vel = self.vel * (-1)
                self.walkCount = 0

    def hit(self):
        if (self.health > 0):
            self.health -= 0.5
        else:
            font2 = pygame.font.SysFont('comicsans', 100)
            text2 = font2.render('YOU WON!!', 1, RED)
            win.blit(text2, (250 - (text2.get_width()/2), 200))
            pygame.display.update()
            self.visible = False
            global done
            done = True
            i = 0
            while i < 100:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        i = 301
                        pygame.quit()

pygame.init()
win = pygame.display.set_mode(size)
pygame.display.set_caption("Basics")

walkRight = [pygame.image.load('images/R1.png'), pygame.image.load('images/R2.png'), pygame.image.load('images/R3.png'), pygame.image.load('images/R4.png'), pygame.image.load('images/R5.png'), pygame.image.load('images/R6.png'), pygame.image.load('images/R7.png'), pygame.image.load('images/R8.png'), pygame.image.load('images/R9.png')]
walkLeft = [pygame.image.load('images/L1.png'), pygame.image.load('images/L2.png'), pygame.image.load('images/L3.png'), pygame.image.load('images/L4.png'), pygame.image.load('images/L5.png'), pygame.image.load('images/L6.png'), pygame.image.load('images/L7.png'), pygame.image.load('images/L8.png'), pygame.image.load('images/L9.png')]
bg = pygame.image.load('images/bg.jpg')
char = pygame.image.load('images/standing.png')


# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def redrawGameWindow():
    win.blit(bg, (0,0))  # This will draw our background image at (0,0)
    #text = font.render('Score: ' + str(score), 1, BLACK)
    #win.blit(text,(390, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    for goblin_bullet in goblin_bullets:
        goblin_bullet.draw(win)
    pygame.display.update() 

# -------- Main Program Loop -----------#
man = player(300, 410, 64, 64)
goblin = enemy(60, 410, 64, 64, 450)
font = pygame.font.SysFont('comicsans', 30, True, False) # (font, size, Bold, Italics)
shootLoop = 0
bullets = []
goblin_bullets = []

while not done:
    # --- Main event loop

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            done = True

    if man.visible == True:
        for bullet in bullets:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
            if bullet.x < size[0] and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

    for goblin_bullet in goblin_bullets:
            if goblin_bullet.y - goblin_bullet.radius < man.hitbox[1] + man.hitbox[3] and goblin_bullet.y + goblin_bullet.radius > man.hitbox[1]:
                if goblin_bullet.x + goblin_bullet.radius > man.hitbox[0] and goblin_bullet.x - goblin_bullet.radius < man.hitbox[0] + man.hitbox[2]:
                    man.hit()
                    goblin_bullets = []
                    goblin.x = 440
                    goblin.y = 410
            if goblin_bullet.x < size[0] and goblin_bullet.x > 0:
                goblin_bullet.x += goblin_bullet.vel
            else:
                goblin_bullets.pop(goblin_bullets.index(goblin_bullet))

    keys = pygame.key.get_pressed()
    if man.visible == True:
        if keys[pygame.K_SPACE] and shootLoop == 0:
            if man.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 5:
                bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, BLACK, facing))
            shootLoop = 1

    x = random.randint(1,101)
    if shootLoop == 0:
        if goblin.vel < 0:
            goblin_facing = -1
        else:
            goblin_facing = 1
        if len(goblin_bullets) < 5:
            goblin_bullets.append(projectile(round(goblin.x + goblin.width//2), round(goblin.y + goblin.height//2), 6, BLACK, goblin_facing))
        shootLoop = 1

    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            man.hit()
            goblin_bullets = []
            goblin.x = 440
            goblin.y = 410
    # Move the rectangle using keys
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < size[0]-man.width:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if not(man.isJumping):
        if keys[pygame.K_UP]:
            man.isJumping = True
            man.walkCount = 0
    else:
        if (man.jumpCount >= -10):
            neg = +1
            if man.jumpCount < 0:
                neg = -1
            man.y -= man.jumpCount ** 2 * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.jumpCount = 10
            man.isJumping = False
    redrawGameWindow()
    # --- Limit to 60 frames per second
    clock.tick(27)

pygame.quit()