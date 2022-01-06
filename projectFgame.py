import pygame
import random
import os

from pygame import font

#from pygame.sprite import collide_circle
#from pygame import key
#from pygame.constants import KEYDOWN


# 初始化
pygame.init()
time = pygame.time.Clock()

updating = True



FPS = 60
enemy_wait = 0
Health = 1000
gamestep = 0


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

#圖片讀取
frame_IMG =  pygame.image.load(os.path.join("img", "TESTBG.jpg")).convert()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLUE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


# 角色
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.radius = 18
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
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
        bullet = F_bullet(self.rect.centerx, self.rect.bottom - 60)
        all_sprite.add(bullet)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80,80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.radius = 30
        pygame.draw.circle(self.image, GREEN, self.rect.center, self.radius)
        self.rect.centerx = P_WIDTH/2
        self.rect.centery = -50
        self.speedx = 1
        self.speedy = 1
        self.time = 0
        self.fireTime = 0
        self.settingPlace = False
        self.EnemyFireMode = 1
        self.x = 0
        self.y = 0

    def update(self):
        if self.settingPlace == False:
            self.movein()
        if self.settingPlace == True:
            if self.EnemyFireMode == 1 and self.time == 0:
                for i in range(9):
                    self.time = 40
                    if i % 9 == 0:
                        self.x = self.rect.centerx - 120
                        self.y = self.rect.centery - 10
                        self.fire()
                    elif i % 9 == 1:
                        self.x = self.rect.centerx - 80
                        self.y = self.rect.centery + 20
                        self.fire()
                    elif i % 9 == 2:
                        self.x = self.rect.centerx - 40
                        self.y = self.rect.centery + 40
                        self.fire()
                    elif i % 9 == 3:
                        self.x = self.rect.centerx 
                        self.y = self.rect.centery + 50
                        self.fire()
                    elif i % 9 == 4:
                        self.x = self.rect.centerx + 40
                        self.y = self.rect.centery + 40
                        self.fire()
                    elif i % 9 == 5:
                        self.x = self.rect.centerx + 80
                        self.y = self.rect.centery + 20
                        self.fire()
                    elif i % 9 == 6:
                        self.x = self.rect.centerx + 120
                        self.y = self.rect.centery - 10
                        self.fire()
                    elif i % 9 == 7:
                        self.x = self.rect.centerx - 180
                        self.y = self.rect.centery - 15
                        self.fire()
                    elif i % 9 == 8:
                        self.x = self.rect.centerx + 180
                        self.y = self.rect.centery - 15
                        self.fire()
                    self.fireTime += 1
                self.time = 40
            
            
            
            #if self.EnemyFireMode == 2 and self.time == 0:


            if self.time > 0:
                self.time -= 1
        #    if self.fireTime >= 80:
         #       self.firemode()

    def movein(self):
        if self.rect.centery < 50:
            self.rect.y += 1
        else:
            self.settingPlace = True
            
    def firemode(self):
        self.EnemyFireMode = random.randrange(1,2)

    def fire(self):
        bullet = E_bullet(self.x, self.y)
        all_sprite.add(bullet)
        enemy_bullets.add(bullet)

        
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

class E_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((18,18))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.radius = 9
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = 1
        self.speedy = 3

    def update(self):
        if Enemy().EnemyFireMode == 1:
            self.move_1()
        if self.rect.top > HEIGHT or self.rect.right > P_WIDTH or self.rect.left < 0:
            self.kill()

    def move_1(self):
        self.speedx = random.randrange(-3, 4)
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy


# sprite 群組
all_sprite = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_sprite = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

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
    hit = pygame.sprite.groupcollide(enemy_sprite, bullets, False, True, pygame.sprite.collide_circle)
    if hit:
        Health -= 1


    
    # 畫面刷新
    screen.fill(WHITE)
    screen.blit(frame_IMG, (0, 0))
    all_sprite.draw(screen)
    draw_text(screen, str(Health), 24, P_WIDTH/2, 10)
    pygame.display.update()
