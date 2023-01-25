import random
import pygame
import math
from pygame import mixer
from pygame.examples.eventlist import font

c = 12
pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
mixer.music.load('background music.mp3')
mixer.music.play(-1)
pygame.display.set_caption('MARPHY')


# background
background = pygame.image.load('the Fruit Kingdom2.png')
# our chef
chef_img = pygame.image.load('chef (2).png')
playerX = 370
playerY = 520
playerX_change = 0
# our enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6
num_of_items = 109
j = 1

for x in range(num_of_items):
    picture = pygame.image.load(f'({j}).png')
    picture = pygame.transform.scale(picture, (50, 50))
    enemy_img.append(picture)
    j += 1

for i in range(num_of_enemies):

    enemyX.append(random.randint(0, 900))
    enemyY.append(random.randint(10,50))
    enemyX_change.append(0)
    enemyY_change.append(1.25)

# our knife , ready = you cannot see the knife on the screen, fire = the knife is currently moving
knife_img = pygame.image.load('knifer.png')
knifeX = 370
knifeY = 390
knifeX_change = 0
knifeY_change = 15
knife_state = "ready"
score = 0
font1 = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    game_over = game_over_font.render("Game Over",True, (255, 255, 255))
    screen.blit(game_over, (330, 270))


def show_score(x, y):
    score_value = font1.render("Score :"+str(score),True,(255,255,255))
    screen.blit(score_value, (x, y))


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


def chef(x, y):
    screen.blit(chef_img, (x, y))


def enemy(x, y):
    screen.blit(enemy_img[i], (x, y))


def knife(x, y):
    global knife_state
    knife_state = "fire"
    screen.blit(knife_img, (x - 15, y - 40))


def collision(enemy_x, enemy_y, knife_x, knife_y, counter):
    distance = math.sqrt(math.pow(enemy_x[counter] - knife_x, 2) + math.pow(enemy_y[counter] - knife_y, 2))
    if distance < 35:
        return True
    else:
        return False


run = True
while run:

    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # checking if keyboard keys are pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -9.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 9.5
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                if knife_state == "ready":
                    knifeX = playerX
                    knife(knifeX, knifeY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    clock.tick(60)
    # player movements
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1068:
        playerX = 1068

    # knife movement
    if knifeY <= 0:
        knifeY = 480
        knife_state = "ready"

    if knife_state == "fire":
        knife(knifeX, knifeY)
        knifeY -= knifeY_change

    playerX += playerX_change

    # enemy movements
    for i in range(num_of_enemies):
        if enemyY[i] > 490:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyY[i] += enemyY_change[i]
        if enemyY[i] <= 0:
            enemyY[i] = 0
        # elif enemyY[i] >= 480:
        #     enemyY[i] = 480

        # Collision
        Collision = collision(enemyX, enemyY, knifeX, knifeY, i)
        if Collision:
            knife_sound = mixer.Sound('hit sound.wav')
            knife_sound.play()
            knifeY = 480
            knife_state = "ready"
            score += 1

            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(10, 50)
            c = random.randint(0, 108)
            enemy_img[i] = enemy_img[c]

        enemy(enemyX[i], enemyY[i])
    show_score(textX, textY)
    chef(playerX, playerY)
    pygame.display.update()






