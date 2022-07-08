import datetime
import time
import pygame
import random
import sys

pygame.init() #иициализация библиотеки
display_height = 600
display_width = 800 #параметры экрана
bg_x=0
bg_y=0
fps = 60
speed = 1
score = 0
timeLast=time.time()
difficul_counter=0

display = pygame.display.set_mode((display_width, display_height)) #создание экрана
pygame.display.set_caption("Runner Boy")
clock = pygame.time.Clock()

make_jump=False

bg = pygame.image.load('bg1.png')
orc_walk = [pygame.image.load('enemy/ORK_01_WALK_000.png'),pygame.image.load('enemy/ORK_01_WALK_002.png'),
       pygame.image.load('enemy/ORK_01_WALK_004.png'),pygame.image.load('enemy/ORK_01_WALK_006.png'),
        pygame.image.load('enemy/ORK_01_WALK_008.png')]
#orc_rect=orc_walk[0].get_rect(topleft=(0,0))
orc_walk2=[pygame.image.load('enemy/orc2/ORK_03_WALK_000.png'),pygame.image.load('enemy/orc2/ORK_03_WALK_002.png'),
           pygame.image.load('enemy/orc2/ORK_03_WALK_004.png'),pygame.image.load('enemy/orc2/ORK_03_WALK_006.png'),
           pygame.image.load('enemy/orc2/ORK_03_WALK_008.png')]
hero_run = [pygame.image.load('hero/run01.png'),pygame.image.load('hero/run02.png'),pygame.image.load('hero/run03.png'),
            pygame.image.load('hero/run04.png'),pygame.image.load('hero/run05.png'),pygame.image.load('hero/run06.png')]
#hero_rect=hero_run[0].get_rect(topleft=(0,0))
hero_jump = [pygame.image.load('hero/jump/jump01.png'),pygame.image.load('hero/jump/jump02.png'),
             pygame.image.load('hero/jump/jump03.png'),pygame.image.load('hero/jump/jump04.png'),
             pygame.image.load('hero/jump/jump05.png'),pygame.image.load('hero/jump/jump06.png')]
img_counter=0
hero_img_counter=0
jump_counter=40
jump_img_counter=0







def game(x):
    global make_jump, jump_img_counter
    game=True

    while game:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            hero.rect.x+=2
        if keys[pygame.K_LEFT]:
            hero.rect.x-=3
        if game:
            x-=speed
            if x<=-900:
                x=50
        if keys[pygame.K_SPACE]:
            make_jump=True
            jump_img_counter=0
        if keys[pygame.K_ESCAPE]:
            pause()
        if make_jump:
            hero.jump()
            if keys[pygame.K_RIGHT]:
                hero.rect.x+=3
            if keys[pygame.K_LEFT]:
                hero.rect.x-=3
        display.blit(bg,(x,bg_y))

        score_game(score)
        hero.move()
        orc.move()
        #orc2.move()
        #if hero_rect.colliderect(orc_rect):
         #   collide()
        if hero.rect.colliderect(orc.rect1):
            collide()
        #time_game(speed,timeLast)
        difficul()

        #pygame.display.update(rect_update)
        #pygame.display.update(rect1_update)
        pygame.display.update()
        clock.tick(fps)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_enemy):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.speed_enemy = speed_enemy+speed
        self.rect1=pygame.Rect((self.x,self.y,100,100))
        #display.blit(self.orcus)
        #self.orcus=pygame.Surface((100,120))
        #display.blit(self.orcus,(self.x,self.y))
        #self.rect1=self.orcus.get_rect(topleft=(self.x,self.y))


    #self.enemy=pygame.Surface((40,120))
        #self.rect1= pygame.Rect((0,0,160,125))

        #self.rect1.move(self.x,self.y)

    def move(self):
        #display.blit(self.orcus,(self.x,self.y),self.rect1)

        if self.rect1.x < -50:
            self.rect1.x = display_width+50
            #self.kill()
        else:
            #display.blit(self.orcus,(self.x,self.y),self.rect))
            self.rect1.x-=self.speed_enemy+speed
            global img_counter
            if img_counter == 40:
                img_counter = 0
            else:
                display.blit(orc_walk[img_counter//8], (self.rect1.x, self.rect1.y))
                #self.rect1.move_ip(800-speed,60)
                img_counter += 1
               # else:
                    #display.blit(orc_walk2[img_counter//8], (self.x, self.y))
                   # img_counter += 1



class Hero(pygame.sprite.Sprite):
    def __init__(self, hero_x, hero_y):
        pygame.sprite.Sprite.__init__(self)
        self.hero_x=hero_x
        self.hero_y=hero_y
        #self.hero=pygame.Surface((40,120))
        self.rect=pygame.Rect((self.hero_x,self.hero_y,47,120))
        #display.blit(self.hero,(self.hero_x,self.hero_y))
        #self.hero_rect=self.hero.get_rect(topleft=(1,1))
        self.hero_hp=3
        self.hero_speed=0.1
        #self.hero=pygame.Surface((40,120))
        #self.rect=pygame.Rect((0,0,93,121))
    def move(self):
        #display.blit(self.hero,(self.hero_x,self.hero_y),self.hero_rect)
        #pygame.Rect(100,100,100,100)

        if self.hero_x == display_width:
            self.hero_x-=self.hero_speed-4

        elif self.hero_x<5:
            self.hero_x+=self.hero_speed+4
        else:
            self.hero_x+=self.hero_speed
            global hero_img_counter
            if hero_img_counter == 40:
               hero_img_counter = 0
            else:
                #self.hero_rect.move(self.hero_x,self.hero_y)
                #self.rect.move_ip(self.hero_x,self.hero_y)

                display.blit(hero_run[hero_img_counter//8], (self.rect.x, self.rect.y))
                hero_img_counter += 1
    def jump(self):
        global make_jump, jump_img_counter, jump_counter

        if make_jump:
            if jump_counter >= -40:
                self.rect.y -= jump_counter/2
                jump_counter -= 2
            else:
                jump_counter = 40
                make_jump = False
            if jump_img_counter==36:
                jump_img_counter = 0
            display.blit(hero_jump[jump_img_counter // 12], (self.rect.x, self.rect.y))
            jump_img_counter += 1


def pause():  # функия паузы в игре
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text('Paused. \nPress Enter to continued', display_width / 3-130, display_height / 2-230,font_color='black')
        print_text('Paused. \nPress Enter to continued', display_width / 3-130, display_height / 2-233,font_color='brown')
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            pause = False

        pygame.display.update()
        clock.tick(15)
def print_text(message, x, y, font_color=(255, 255, 255), font_type='Boncegro FF 4F.otf', font_size=40):  # вывод текста
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message,True,font_color)
    display.blit(text, (x, y))

def menu():
    global menu, keys
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.blit(pygame.image.load('bg1.png'), (0, 0))
        print_text('Runner BOY', display_width // 3-30, display_height / 2 - 200, font_color=(0, 0, 0), font_size=80)
        print_text('Runner BOY', display_width // 3-30, display_height / 2 - 205, font_color=(255, 255, 255), font_size=80)
        print_text('Press Enter to START', display_width / 3-10, display_height / 2 + 50, font_color='black')
        print_text('Press Enter to START', display_width / 3-10, display_height / 2 + 48, font_color='brown')
        print_text('Press H to read manual', display_width / 3-30, display_height / 2 + 110, font_color='black')
        print_text('Press H to read manual', display_width / 3-30, display_height / 2 + 108, font_color='grey')
        display.blit(pygame.image.load('hero.png'),(display_height-600,display_width-600))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            menu = False
            game(bg_x)
        pygame.display.update()
        clock.tick(15)

def difficul():
    global difficul_counter,speed
    if difficul_counter==1000:
        speed+=1
        #print(speed)
        difficul_counter=0
    difficul_counter+=1
    #print(difficul_counter)




def death():
    global menu, game
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text('Game over', display_width-480, display_height -350,font_color='black')
        print_text('Game over', display_width-480, display_height -355,font_color='white')
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            pause = False
            game=False
            pygame.quit()
            exit()
        pygame.display.update()
        clock.tick(15)

def score_game(score):

    print_text('Score: ',display_width-780,display_height-580,font_color='black')
    print_text('Score: ',display_width-780,display_height-582,font_color='white')
    print_text(str(score),display_width-650,display_height-580,font_color='black')
    print_text(str(score),display_width-652,display_height-582,font_color='white')



def collide():
    global score
    print('qwert')
    score=score+1







orc=Enemy(display_width-150,display_height-200,random.randrange(3,4)+speed)
#orc2=Enemy(display_width-150,display_height-200,random.randrange(1,4)/2,2)
hero=Hero(display_width-750,display_height-200)

#orc_surf=pygame.Surface((70,120))
#orc_rect=orc_surf.get_rect(topleft=(orc.x,orc.y))
#rect1_update=pygame.Rect(orc.x,orc.y,70,120)

#hero_surf=pygame.Surface((47,120))
#hero_rect=hero_surf.get_rect(topleft=(hero.hero_x,hero.hero_y))
#rect_update=pygame.Rect(hero_rect.x,hero_rect.y,47,120)
#pygame.draw.rect(display,(255,255,255),(hero.hero_x,hero.hero_y,40,120))
#print(hero.rect)
#game(bg_x)
menu()
pygame.display.update()
