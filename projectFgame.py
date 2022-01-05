import pygame
import random
import os


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
WIDTH = 1000
HEIGHT = 800
P_WIDTH = 600


# 定義視窗
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("東方Project")

BGIMG =  pygame.image.load(os.path.join("img", "TESTBG.jpg")).convert()


# 角色
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 60))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = P_WIDTH/2
        self.rect.bottom = HEIGHT - 70
        self.speed = 5  
        self.FireTime = 0

    def update(self):
        # 按鍵捕捉及移動
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE] and self.FireTime == 0:
            self.fire()
            self.FireTime = 3
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
        if self.rect.right > P_WIDTH:
            self.rect.right = P_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.FireTime > 0:
            self.FireTime -= 1
        

    def fire(self):
        bullet = F_bullet(self.rect.centerx, self.rect.bottom)
        all_sprite.add(bullet)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70,70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = P_WIDTH/2
        self.rect.y = -80
        self.speedx = 1
        self.speedy = 1
        self.time = 0

    def update(self):
        if self.rect.y < 10:
            self.rect.y += 1
        


class F_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,20))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -15

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# sprite 群組
all_sprite = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_sprite = pygame.sprite.Group()

player = Player()
all_sprite.add(player)
enemy = Enemy()
all_sprite.add(enemy)
enemy_sprite.add(enemy)
# 主迴圈

while updating:
    time.tick(FPS)
    # 輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            updating = False
        


    # 畫面更新
    all_sprite.update()
    pygame.sprite.groupcollide(enemy_sprite, bullets, False, True)


    # 畫面刷新
    screen.fill(WHITE)
    screen.blit(BGIMG, (0, 0))
    all_sprite.draw(screen)
    pygame.display.update()
