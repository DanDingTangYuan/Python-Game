from sys import path
import pygame
import random
import os
from pygame.constants import MOUSEBUTTONDOWN

from pygame.sprite import groupcollide, spritecollideany
from pygame.time import delay



# 初始化
pygame.init()
pygame.mixer.init()
time = pygame.time.Clock()
updating = True

f = open(os.path.join("Grade", "H_Grade.txt"), mode='r')
hscore = f.read()
f.close()



FPS = 60
enemy_wait = 0
E_Health = 1000
player_heart = 3
Score = 0
Music_On = True


GAMESTEP = 0
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
Enemy_IMG =  pygame.image.load(os.path.join("img", "Patchouli.png")).convert()
Player_IMG = pygame.image.load(os.path.join("img", "player.png")).convert()
F_Bullet_IMG = pygame.image.load(os.path.join("img", "F_Bullet.png")).convert()
E_Bullet_IMG = pygame.image.load(os.path.join("img", "E_Bullet.png")).convert()
P_Heart_IMG = pygame.image.load(os.path.join("img", "Heart.jpg")).convert()
P_Heart_IMG.set_colorkey(WHITE)
E_Health_H_IMG = pygame.image.load(os.path.join("img", "life_H.png")).convert()
E_Health_M_IMG = pygame.image.load(os.path.join("img", "life_M.png")).convert()
E_Health_E_IMG = pygame.image.load(os.path.join("img", "life_E.png")).convert()
E_Health_H_IMG.set_colorkey(WHITE)
E_Health_M_IMG.set_colorkey(WHITE)
E_Health_E_IMG.set_colorkey(WHITE)
Title_IMG = pygame.image.load(os.path.join("img", "title.png")).convert()
StartButtom_IMG = pygame.image.load(os.path.join("img", "startbuttom.jpg")).convert()
MusicOn_IMG = pygame.image.load(os.path.join("img", "music_on.jpg")).convert()
MusicOFF_IMG = pygame.image.load(os.path.join("img", "music_off.jpg")).convert()
GoodEnd_IMG = pygame.image.load(os.path.join("img", "GE.png")).convert()
BadEnd_IMG = pygame.image.load(os.path.join("img", "BE.png")).convert()
ReStartButtom_IMG = pygame.image.load(os.path.join("img", "re.jpg")).convert()


#音效
Menu_Bgm = pygame.mixer.Sound(os.path.join("sound", "start_bgm.mp3"))
Game_Bgm = pygame.mixer.Sound(os.path.join("sound", "game_bgm.mp3"))




font_name = pygame.font.match_font('arial')


def score_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLUE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def BS_text(surf, text, size, x, y):
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
        #self.image = pygame.Surface((40, 40))
        self.image = Player_IMG
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 10
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
        self.image = pygame.transform.scale(Enemy_IMG, (70,70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 30
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
        self.bulletSpeed = 2

    def update(self):
        if self.settingPlace == False:
            self.movein()
        if self.settingPlace == True:
            if self.EnemyFireMode == 1 and self.time == 0 and self.fireTime < 600:
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
                self.time = 40
            if self.EnemyFireMode == 2 and self.time == 0 and self.fireTime < 600:
                for i in range(5):
                    self.time = 30
                    if i % 5 == 0:
                        self.x = self.rect.centerx - 120
                        self.y = self.rect.centery
                        self.fire()
                    elif i % 5 == 1:
                        self.x = self.rect.centerx - 60
                        self.y = self.rect.centery + 30
                        self.fire()
                    elif i % 5 == 2:
                        self.x = self.rect.centerx
                        self.y = self.rect.centery + 50
                        self.fire()
                    elif i % 5 == 3:
                        self.x = self.rect.centerx + 60
                        self.y = self.rect.centery + 30
                        self.fire()
                    elif i % 5 == 4:
                        self.x = self.rect.centerx + 120
                        self.y = self.rect.centery
                        self.fire()
                self.time = 40
            self.fireTime += 1
            if self.time > 0:
                self.time -= 1
            if self.fireTime == 600:
                self.EnemyFireMode == 0
            elif self.fireTime > 720:
                self.fireTime = 0
                self.bulletSpeed += 1
            
                
    def movein(self):
        if self.rect.centery < 50:
            self.rect.y += 1
        else:
            self.settingPlace = True


    def fire(self):
        bullet = E_bullet(self.x, self.y, self.bulletSpeed)
        all_sprite.add(bullet)
        enemy_bullets.add(bullet)

class F_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,35))
        self.image = F_Bullet_IMG
        self.image.set_colorkey(WHITE)
        #self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -15

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class E_bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, z):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((18,18))
        self.image = pygame.transform.scale(E_Bullet_IMG, (18,18))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 9
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = random.randrange(-1, 2)
        self.speedy = z

    def update(self):
        if Enemy().EnemyFireMode == 1:
            self.move()
        if self.rect.top > HEIGHT or self.rect.right > P_WIDTH or self.rect.left < 0:
            self.kill()

    def move(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

class StartButtom(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = StartButtom_IMG
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 400

    def update(self, Mx, My):
        if 700 >= Mx >= 500 and 480 >= My >= 400:
            self.rect.x = 490
            self.rect.y = 380
        else:
            self.rect.x = 500
            self.rect.y = 400

class MusicButtom(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = MusicOn_IMG
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 500

    def update(self, Mx, My):
        if 700 >= Mx >= 500 and 580 >= My >= 500:
            self.rect.x = 490
            self.rect.y = 480
        else:
            self.rect.x = 500
            self.rect.y = 500
        if Music_On == True:
            self.image = MusicOn_IMG
        elif Music_On == False:
            self.image = MusicOFF_IMG

class RestartButtom(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ReStartButtom_IMG
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 600

    def update(self, Mx, My):
        if 600 >= Mx >= 400 and 680 >= My >= 600:
            self.rect.x = 390
            self.rect.y = 580
        else:
            self.rect.x = 400
            self.rect.y = 600

# sprite 群組
all_sprite = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_sprite = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
buttom_sprite = pygame.sprite.Group()
ED_sprite = pygame.sprite.Group()

player = Player()
all_sprite.add(player)
player_sprite.add(player)
enemy = Enemy()
all_sprite.add(enemy)
enemy_sprite.add(enemy)

sb = StartButtom()
buttom_sprite.add(sb)
mb = MusicButtom()
buttom_sprite.add(mb)
rb = RestartButtom()
ED_sprite.add(rb)
# 主迴圈

while updating:
    time.tick(FPS)

    if GAMESTEP == 0:
        screen.blit(Title_IMG, (0, 0))
        if pygame.mixer.music.get_busy() == 0:
            if Music_On == True:
                Menu_Bgm.play()
                Menu_Bgm.set_volume(0.1)
        Mx, My = pygame.mouse.get_pos()
        buttom_sprite.update(Mx, My)
        if 700 >= Mx >= 500 and 480 >= My >= 400:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Menu_Bgm.stop()
                    GAMESTEP = 1
        if 700 >= Mx >= 500 and 580 >= My >= 500:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Music_On == True:
                        Music_On = False
                        Menu_Bgm.stop()
                    else:
                        Music_On = True
        buttom_sprite.draw(screen)
    elif GAMESTEP == 1: #主階段
        if pygame.mixer.music.get_busy() == 0:
            if Music_On == True:
                Game_Bgm.play()
                Game_Bgm.set_volume(0.1)
        screen.blit(frame_IMG, (0, 0))
        if player_heart == 3:
            screen.blit(pygame.transform.scale(P_Heart_IMG, (40, 40)), (760, 255))
            screen.blit(pygame.transform.scale(P_Heart_IMG, (40, 40)), (810, 255))
            screen.blit(pygame.transform.scale(P_Heart_IMG, (40, 40)), (860, 255))
        elif player_heart == 2:
            screen.blit(pygame.transform.scale(P_Heart_IMG, (40, 40)), (760, 255))
            screen.blit(pygame.transform.scale(P_Heart_IMG, (40, 40)), (810, 255))
        elif player_heart == 1:
            screen.blit(pygame.transform.scale(P_Heart_IMG, (40, 40)), (760, 255))
        elif player_heart == 0:
            Game_Bgm.stop()
            GAMESTEP = 2

        all_sprite.update()
        hit = pygame.sprite.groupcollide(enemy_sprite, bullets, False, True, pygame.sprite.collide_circle)
        if hit:
            E_Health -= 1
            Score += 10
        getfire = pygame.sprite.spritecollide(player, enemy_bullets, True, pygame.sprite.collide_circle)
        if getfire :
            player_heart -= 1
        
        if E_Health == 0:
            Game_Bgm.stop()
            GAMESTEP = 2
        all_sprite.draw(screen)
        score_text(screen, str(Score), 36, 840, 114)
        if Score > int(hscore):
            BS_text(screen, str(Score), 36, 900, 74)
        else:
            BS_text(screen, str(hscore), 36, 900, 74)


    elif GAMESTEP == 2: #勝利
        if Score > int(hscore):
            f.write(Score)
            f.close()
            screen.blit(GoodEnd_IMG,(0,0))
            win = True
            GAMESTEP = 3
        else:
            screen.blit(BadEnd_IMG,(0,0))
            win = False
            GAMESTEP = 3
            
    elif GAMESTEP == 3:
        if win == True:
            screen.blit(GoodEnd_IMG,(0,0))
        else:
            screen.blit(BadEnd_IMG,(0,0))
        Mx, My = pygame.mouse.get_pos()
        ED_sprite.update(Mx, My)
        if 600 >= Mx >= 400 and 680 >= My >= 600:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    GAMESTEP = 0
        ED_sprite.draw(screen)


        

    # 輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            updating = False
    pygame.display.update()
