import pygame
import math
import random
from pygame import mixer

# initialise the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('/home/pragya/space invaders/background.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)


#title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('/home/pragya/space invaders/spaceship.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('/home/pragya/space invaders/space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(
        '/home/pragya/space invaders/monsters.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# enemy
ghostImg = []
ghostX = []
ghostY = []
ghostX_change = []
ghostY_change = []
num_of_ghost = 5

for i in range(num_of_ghost):
    ghostImg.append(pygame.image.load(
        '/home/pragya/space invaders/player.png'))
    ghostX.append(random.randint(0, 735))
    ghostY.append(random.randint(50, 150))
    ghostX_change.append(4)
    ghostY_change.append(40)

#bullet
bulletImg = pygame.image.load('/home/pragya/space invaders/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 25)

textX = 10
textY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 32)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("Remember kids:", True, (255, 255, 255))
    screen.blit(over_text, (220, 150))

    over_text = over_font.render("Life has always planned something better for you!", True, (255, 255, 255))
    screen.blit(over_text, (3, 200))

    over_text = over_font.render("NEVER LOOSE HOPES!!", True, (255, 255, 255))
    screen.blit(over_text, (220, 250))


    over_text = over_font.render("And yes, always choose green monsters :) ", True, (255, 255, 255))
    screen.blit(over_text, (50, 300))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def ghost(x, y, i):
    screen.blit(ghostImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, playerX, playerY):
    #print("tyui")
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                         (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def isCollision1(ghostX, ghostY, playerX, playerY):
    distance = math.sqrt((math.pow(ghostX-bulletX, 2)) +
                         (math.pow(ghostY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


hold = True
# start screen
while hold:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            hold = False
        text1 = font.render("Here's a question for you guysss!!!!", True, (255, 255, 255))
        screen.blit(text1, (200, 100))
        text2 = font.render("What will you do if you fail in a task that matters the most to you?", True, (255, 255, 255))
        screen.blit(text2, (3, 200))
        text3 = font.render("1. Suicide - RED MONSTER", True, (255, 255, 255))
        screen.blit(text3, (7, 250))
        text4 = font.render("2. Work harder for the next time - GREEN MONSTER", True, (255, 255, 255))
        screen.blit(text4, (7, 300))
        text = font.render("Come on in and choose your options!!", True, (255, 255, 255))
        screen.blit(text, (180, 400))
        text = font.render("PRESS ANY KEY TO START" ,True, (255, 255, 255))
        screen.blit(text, (220, 450))
        if event.type == pygame.KEYDOWN:
            running = True
            hold = False

    pygame.display.update()


# game loop
running = True
while running:

    screen.fill((0, 0, 0))
    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # key movements
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_UP:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                ghostY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value -= 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    for i in range(num_of_ghost):

        # game over
        if ghostY[i] > 440:
            for j in range(num_of_ghost):
                ghostY[j] = 2000
                enemyY[j] = 2000
            game_over_text()
            break

        ghostX[i] += ghostX_change[i]

        if ghostX[i] <= 0:
            ghostX_change[i] = 2
            ghostY[i] += ghostY_change[i]
        elif ghostX[i] >= 736:
            ghostX_change[i] = -2
            ghostY[i] += ghostY_change[i]

        # collision

        collision1 = isCollision1(ghostX[i], ghostY[i], playerX, playerY)
        if collision1:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            ghostX[i] = random.randint(0, 735)
            ghostY[i] = random.randint(50, 150)

        ghost(ghostX[i], ghostY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
