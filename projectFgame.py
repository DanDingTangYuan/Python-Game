import pygame
import random

from pygame import key


# 初始化
pygame.init()
time = pygame.time.Clock()
updating = True

FPS = 60

WHITE = (255,255,255)
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
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT - 70)
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(255,0,0)
        self.rect = self.image.get_rect()
        self.center

    def update(self):
        self.rect

# sprite 群組
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
# 主迴圈

while updating:
    time.tick(FPS)
    # 輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            updating = False
    # 畫面更新
    all_sprites.update()

    # 畫面刷新
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.update()
