import time
import pygame
import random
import sqlite3
import os



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
need_input=False
input_text=''
display = pygame.display.set_mode((display_width, display_height)) #создание экрана
pygame.display.set_caption("Runner Boy")
clock = pygame.time.Clock()
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
make_jump=False
music=pygame.mixer.music.load("music.mp3")
img_counter=0
hero_img_counter=0
jump_counter=40
jump_img_counter=0


bg = pygame.image.load('bg1.png')
orc_walk = [pygame.image.load('enemy/ORK_01_WALK_000.png'),pygame.image.load('enemy/ORK_01_WALK_002.png'),
       pygame.image.load('enemy/ORK_01_WALK_004.png'),pygame.image.load('enemy/ORK_01_WALK_006.png'),
        pygame.image.load('enemy/ORK_01_WALK_008.png')]
orc_walk2=[pygame.image.load('enemy/orc2/ORK_03_WALK_000.png'),pygame.image.load('enemy/orc2/ORK_03_WALK_002.png'),
           pygame.image.load('enemy/orc2/ORK_03_WALK_004.png'),pygame.image.load('enemy/orc2/ORK_03_WALK_006.png'),
           pygame.image.load('enemy/orc2/ORK_03_WALK_008.png')]
hero_run = [pygame.image.load('hero/run01.png'),pygame.image.load('hero/run02.png'),pygame.image.load('hero/run03.png'),
            pygame.image.load('hero/run04.png'),pygame.image.load('hero/run05.png'),pygame.image.load('hero/run06.png')]
hero_jump = [pygame.image.load('hero/jump/jump01.png'),pygame.image.load('hero/jump/jump02.png'),
             pygame.image.load('hero/jump/jump03.png'),pygame.image.load('hero/jump/jump04.png'),
             pygame.image.load('hero/jump/jump05.png'),pygame.image.load('hero/jump/jump06.png')]



def game(x):
    global make_jump, jump_img_counter,score
    game=True

    pygame.mixer.music.play(-1)
    while game:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
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
            pygame.mixer.music.pause()
            pause()
        if make_jump:
            hero.jump()
            if keys[pygame.K_RIGHT]:
                hero.rect.x+=3
            if keys[pygame.K_LEFT]:
                hero.rect.x-=3
        if keys[pygame.K_h]:
            help()

        display.blit(bg,(x,bg_y))

        hero.move()
        orc.move()
        orc2.move()
        if (hero.rect.colliderect(orc.rect1)or(hero.rect.colliderect(orc2.rect1))):
            hero.hit()
            score-=2
            if score<0:
                score=0
        if hero.health<=0:
            pygame.mixer.music.stop()
            death()

        score_game()
        difficul()

        pygame.display.update()
        clock.tick(fps)

    if game==False:
        menu_game()
pygame.display.update()
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_enemy,num):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.speed_enemy = speed_enemy+speed
        self.rect1=pygame.Rect((self.x,self.y,90,120))
        #self.rect2=pygame.Rect((self.x,self.y,50,100))
        self.num=num


    def move(self):

        if self.rect1.x < -50:
            self.rect1.x = display_width+50

        else:
            self.rect1.x-=self.speed_enemy+speed
            #self.rect2.x-=self.speed_enemy+speed

            global img_counter
            if img_counter == 40:
                img_counter = 0
            if (self.num==1):
                display.blit(orc_walk[img_counter//8], (self.rect1.x, self.rect1.y))
                img_counter += 1
            else:
                display.blit(orc_walk2[img_counter//8], (self.rect1.x, self.rect1.y))
                img_counter += 1



class Hero(pygame.sprite.Sprite):
    def __init__(self, hero_x, hero_y):
        pygame.sprite.Sprite.__init__(self)
        self.hero_x=hero_x
        self.hero_y=hero_y
        self.rect=pygame.Rect((self.hero_x,self.hero_y,47,100))
        self.health=100
        #self.hp=pygame.transform.scale(hero_hp, (self.health,30))
        self.hero_speed=0.1
    def hit(self):


        self.health-=1
        #print(self.health)

    def move(self):
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
                exit()
        print_text('Paused. \nPress Enter to continued', display_width / 3-130, display_height / 2-230,font_color='black')
        print_text('Paused. \nPress Enter to continued', display_width / 3-130, display_height / 2-233,font_color='brown')
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            pygame.mixer.music.unpause()
            pause = False

        pygame.display.update()
        clock.tick(15)
def print_text(message, x, y, font_color=(255, 255, 255), font_type='Boncegro FF 4F.otf', font_size=40):  # вывод текста
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message,True,font_color)
    display.blit(text, (x, y))

def menu_game():
    global menu, keys
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        display.blit(pygame.image.load('bg1.png'), (0, 0))
        print_text('Runner BOY', display_width // 3-30, display_height / 2 - 200, font_color=(0, 0, 0), font_size=80)
        print_text('Runner BOY', display_width // 3-30, display_height / 2 - 205, font_color=(255, 255, 255), font_size=80)
        print_text('Press SPACE Start Game', display_width / 3-10, display_height / 2 + 50, font_color='black')
        print_text('Press SPACE Start Game', display_width / 3-10, display_height / 2 + 48, font_color='brown')
        print_text('Hold R Records table', display_width / 3-10, display_height / 2 + 100, font_color='black')
        print_text('Hold R Records table', display_width / 3-10, display_height / 2 + 98, font_color='yellow')
        print_text('Hold H Read manual', display_width / 3-10, display_height / 2 + 150, font_color='black')
        print_text('Hold H Read manual', display_width / 3-10, display_height / 2 + 148, font_color='white')
        display.blit(pygame.image.load('hero.png'),(display_height-600,display_width-600))
        print_text('Press I for help documentation', 500, 550, font_size=14, font_color='white')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            menu = False
            game(bg_x)

        if keys[pygame.K_h]:
            help()
        if keys[pygame.K_r]:
            show_records()
        if keys[pygame.K_i]:
            help_doc()


        pygame.display.update()
        clock.tick(15)

def difficul():
    global difficul_counter,speed
    if difficul_counter==1000:
        speed+=1

        difficul_counter=0
    difficul_counter+=1


def death():
    global menu, game, score, speed, hero_start_x,hero_start_y,orc_start_x,orc_start_y,difficul_counter
    game_over = True
    update_bd(score,input_text)
    orc.kill()
    hero.kill()
    orc_start_x = display_width - 150
    orc_start_y = display_height - 200
    hero_start_x = display_width - 750
    hero_start_y = display_height - 200
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        print_text('Game over', display_width-480, display_height -350,font_color='black')
        print_text('Game over', display_width-480, display_height -355,font_color='white')
        print_text('Press Enter to exit menu', display_width - 580, display_height - 250, font_color='black')
        print_text('Press Enter to exit menu', display_width - 580, display_height - 255, font_color='white')
        print_text('Health: ',display_width-200,display_height-580,font_color='black')
        print_text('Health: ',display_width-200,display_height-582,font_color='white')
        print_text(str(hero.health) ,display_width-70,display_height-580,font_color='black')
        print_text(str(hero.health) ,display_width-70,display_height-582,font_color='white')
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            game_over = False


            pygame.quit()
            exit()
        if keys[pygame.K_RETURN]:
            score=0
            hero.health=100
            speed=1
            difficul_counter = 0


            menu_game()

        pygame.display.update()
        clock.tick(15)

def score_game():
    global score,sdb
    print_text('Score: ',display_width-780,display_height-580,font_color='black')
    print_text('Score: ',display_width-780,display_height-582,font_color='white')
    print_text('Health: ',display_width-200,display_height-580,font_color='black')
    print_text('Health: ',display_width-200,display_height-582,font_color='white')
    print_text(str(hero.health) ,display_width-70,display_height-580,font_color='black')
    print_text(str(hero.health) ,display_width-70,display_height-582,font_color='white')

    print_text(str(score),display_width-650,display_height-580,font_color='black')
    print_text(str(score),display_width-652,display_height-582,font_color='white')


    if ((hero.rect.right>orc.rect1.left and
        hero.rect.bottom<orc.rect1.bottom and hero.rect.left<orc.rect1.left)or\
        (hero.rect.right>orc2.rect1.left and
        hero.rect.bottom<orc2.rect1.bottom and hero.rect.left<orc2.rect1.left)):
            score+=1

def help_doc():
    os.startfile('help\Help.chm')


def collide():
    global score
    score-=1

def help():
    pygame.display.set_mode((display_width, display_height))
    display.blit(bg,(0,0))
    print_text('Control set', display_width / 3-130, display_height / 2-230,font_color='black')
    print_text('Control set', display_width / 3-130, display_height / 2-233,font_color='brown')
    print_text('Moving forward', display_width-600, display_height -425,font_color='black')
    print_text('Moving forward', display_width-600, display_height -427,font_color='white')
    print_text('Moving backwards', display_width-600, display_height -325,font_color='black')
    print_text('Moving backwards', display_width-600, display_height -327,font_color='white')
    print_text('Jump', display_width-500, display_height -225,font_color='black')
    print_text('Jump', display_width-500, display_height -227,font_color='white')
    print_text('Pause game', display_width-600, display_height -125,font_color='black')
    print_text('Pause game', display_width-600, display_height -127,font_color='white')
    space=pygame.image.load('space.png')
    arrow1=pygame.image.load('arrow_back.png')
    arrow2=pygame.image.load('arrow_walk.png')
    esc=pygame.image.load('ESC.png')
    display.blit(arrow2,(display_width-680, display_height-430))
    display.blit(arrow1,(display_width-680, display_height-330))
    display.blit(space,(display_width-680, display_height-230))
    display.blit(esc,(display_width-680, display_height-140))
    keys = pygame.key.get_pressed()

    pygame.display.update()
    clock.tick(15)

def show_records():

    pygame.display.set_mode((display_width, display_height))
    display.blit(bg, (0, 0))
    sql.execute("""SELECT name, max(score) from users 
                            group by name""")
    print_text('Records: ',display_height/2,display_width/9, font_color='black')
    print_text('Records: ',display_height/2,display_width/9-2, font_color='white')
    #print_text(str(database.leaders),display_width-680,display_height-300,font_color='white')
    leaders_user=leaders
    lead1=lead
    h = display_height / 2
    w = display_width / 6
    for i in lead1:
        print(i)
        print_text(str(i), h-20, w, font_color='black')
        print_text(str(i), h-20, w-2, font_color='white')
        w += 40
    pygame.display.update()



def enter_name():
    global menu, input_text,name,users_name
    need_input=True
    while need_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                name = input_text
                need_input = False
                add_user()
                menu_game()

            if need_input and event.type==pygame.KEYDOWN:
                if event.type==pygame.K_SPACE:
                    users_name=input_text
                    need_input=False

                    input_text=''
                if event.type==pygame.K_BACKSPACE:
                    input_text=input_text[:-1]

                else:
                    input_text+=event.unicode


        frame=pygame.image.load('enter_name.png')
        display.blit(pygame.image.load('bg1.png'), (0, 0))
        display.blit(frame, (display_width -550, display_height -325))

        print_text('Runner BOY', display_width // 3 - 30, display_height / 2 - 200, font_color=(0, 0, 0),
                       font_size=80)
        print_text('Runner BOY', display_width // 3 - 30, display_height / 2 - 205, font_color=(255, 255, 255),
                       font_size=80)
        print_text('Enter your name', display_width // 3 - 10, display_height - 400, font_color=(0, 0, 0),
                   font_size=40)
        print_text('Enter your name', display_width // 3 - 10, display_height - 405, font_color=(255, 255, 255),
                   font_size=40)
        print_text(str(input_text), display_width -500, display_height -300, font_color=(255, 255, 255),
                   font_size=40)
        print_text('Press SPACE to continue', display_width // 3 - 10, display_height - 105, font_color=(255, 255, 255),
                   font_size=40)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            menu_game()

        pygame.display.update()

orc_start_x=display_width-150
orc_start_y=display_height-200
hero_start_x=display_width-750
hero_start_y=display_height-200
orc = Enemy(orc_start_x, orc_start_y, random.randrange(3,4)+speed, 1)
orc2=Enemy(display_width-150,display_height-200,random.randrange(1,4)/2,2)
hero=Hero(hero_start_x,hero_start_y)

#bd

db = sqlite3.connect('RunnerBoy.db')

sql = db.cursor()
global leaders
global lead
global users_score
global users_name
global complete
global group
sql.execute("""CREATE TABLE if not exists users(name TEXT, score BIGINT)""")

db.commit()
users_name = ''
users_score=score
complete=False


leaders=sql.execute("""SELECT name, score FROM users
                        ORDER by score DESC
                        LIMIT 10""")


lead=sql.fetchall()

def add_user():
    if (sql.fetchone() is None) :
        sql.execute('INSERT INTO users VALUES(?,?)', (input_text,users_score))
        db.commit()
        print ('User complete')
        #sql.close()
    else:
        print("error")
    # sql.close()



def update_bd(s,n):
    try:
        sqlite_connection = sqlite3.connect('RunnerBoy.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_update_query = """UPDATE users SET score = ? WHERE name = ?"""
        data = (s, n)
        cursor.execute(sql_update_query, data)
        sqlite_connection.commit()
        print("Запись успешно обновлена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")




enter_name()

pygame.display.update()
