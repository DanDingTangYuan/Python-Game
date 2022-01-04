import pygame
import random

#from pygame import key
#from pygame.constants import KEYDOWN


# 初始化
pygame.init()
time = pygame.time.Clock()

updating = True

FPS = 60
enemy_wait = 0
EnemyNum = random.randrange(2,6,2)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WIDTH = 600
HEIGHT = 800


# 定義視窗
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("StarWar")


# 角色
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 60))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 70
        self.speed = 5  

    def update(self):
        # 按鍵捕捉及移動
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LSHIFT]:
            self.speed = 10
        else :
            self.speed = 5
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
        # 邊界移動限制
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def fire(self):
        bullet = F_bullet(self.rect.centerx, self.rect.bottom)
        player_sprite.add(bullet)


class Enemy_L(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40,40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = -50
        self.rect.y = -50
        self.speedx = 2
        self.speedy = 1
        self.time = 0

    def update(self):
        if self.rect.x >= 230 and self.speedx > 0:
            self.speedx = -2
            self.time = 120
        elif self.rect.x <= 30 and self.speedx < 0:
            self.speedx = 2
            self.time = 120
        if self.time == 0:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        else:
            self.time -= 1

class F_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,20))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# sprite 群組
player_sprite = pygame.sprite.Group()
enemy_sprite = pygame.sprite.Group()

player = Player()
player_sprite.add(player)
enemy_L = Enemy_L()
enemy_sprite.add(enemy_L)
# 主迴圈

while updating:
    time.tick(FPS)
    # 輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            updating = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()
    

    # 畫面更新
    enemy_sprite.update()
    player_sprite.update()

    # 畫面刷新
    screen.fill(WHITE)
    player_sprite.draw(screen)
    enemy_sprite.draw(screen)
    pygame.display.update()
