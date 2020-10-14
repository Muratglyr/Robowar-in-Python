import pygame
import random
import math


WIDTH =200
HEIGHT =300
FPS = 20 



#COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
GREY = (128,128,128)
#Create Robots
class Robot1(pygame.sprite.Sprite):
    #sprite for the Robot1
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image= pygame.image.load("robot.png") 
        self.rect = self.image.get_rect()
        self.rect.center = (25,275)
        self.energy = 100
        self.speed = 5
        self.attack = 2
        self.defence = 2
        self.enerji_tuketimi = float(self.speed*0.5/self.speed)*5
        

    def update(self):
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_d]:
            self.rect.x += float(self.speed*0.5)# ( 0.5 = Mesafe Katsayısı)
            collisions = pygame.sprite.groupcollide(robot1_groups,robot2_groups,False,False)
            for i in collisions:
                self.rect.x -= float(self.speed*0.5) # ( 0.5 = Mesafe Katsayısı)
            self.energy -= self.enerji_tuketimi

        if keys[pygame.K_a]:
            self.rect.x -=float(self.speed*0.5) # ( 0.5 = Mesafe Katsayısı)
            collisions = pygame.sprite.groupcollide(robot2_groups,robot1_groups,False,False)
            for i in collisions:
                self.rect.x +=float(self.speed*0.5) # ( 0.5 = Mesafe Katsayısı)
            self.energy -= self.enerji_tuketimi
            print(int(self.enerji_tuketimi))
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Fuze1(self.rect.x+25,self.rect.y+25)
        all_sprites.add(bullets)
        bullets.add(bullet)


class Robot2(pygame.sprite.Sprite):
    #sprite for the Robot1
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image= pygame.image.load("robot.png") 
        self.rect = self.image.get_rect()
        self.rect.center = (175,275)
        self.moving_rect = pygame.Rect(self.rect.x,self.rect.y,60,60)
        self.energy = 100
        self.speed = 4
        self.attack = 4
        self.defence = 2
        self.enerji_tuketimi = float(self.speed*0.5/self.speed)*5

    def update(self):
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_LEFT]:
            self.rect.x -= float(self.speed*0.5) # ( 0.5 = Mesafe Katsayısı)
            collisions = pygame.sprite.groupcollide(robot2_groups,robot1_groups,False,False)
            for i in collisions:
                self.rect.x += float(self.speed*0.5) # ( 0.5 = Mesafe Katsayısı)
            self.energy -= self.enerji_tuketimi

        if keys[pygame.K_RIGHT]:
            self.rect.x += float(self.speed*0.5) # ( 0.5 = Mesafe Katsayısı)
            collisions = pygame.sprite.groupcollide(robot2_groups,robot1_groups,False,False)
            for i in collisions:
                self.rect.x -= float(self.speed*0.5) # ( 0.5 = Mesafe Katsayısı)
            self.energy -= self.enerji_tuketimi

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
    def shoot(self):
        bullet = Fuze2(self.rect.x+25,self.rect.y+25)
        all_sprites.add(bullets)
        bullets.add(bullet)


#Robot1'nin Füze 
class Fuze1(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((12,4))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = 5

    def update(self):
        self.rect.x +=self.speedy
        collisions = pygame.sprite.groupcollide(bullets,robot2_groups,False,False)
        for i in collisions:
            self.distance = math.hypot(robot1.rect.x - robot2.rect.x)
            self.damage = abs((random.randrange(10)*robot1.attack/self.distance)-((robot2.defence*self.distance)/10))
            robot2.energy -=self.damage/10
            i.kill()
            if robot2.energy <0:
                robot2.energy = 0
                game_over = True
        #kill if it moves off the top of the screen
        if self.rect.x <0:
            self.kill()
        if self.rect.x > WIDTH:
            self.kill

#Robot2'nin Füze    
class Fuze2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface((12,4))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = -5


    def update(self):
        self.rect.x +=self.speedy 
        collisions = pygame.sprite.groupcollide(bullets,robot1_groups,False,False)
        for i in collisions:
            self.distance = math.hypot(robot2.rect.x - robot1.rect.x)
            self.damage = abs((random.randrange(10)*robot2.attack/self.distance)-((robot1.defence*self.distance)/10))
            robot1.energy -=self.damage/10
            i.kill()
            if robot1.energy <0:
                robot1.energy = 0
                game_over = True
        #kill if it moves off the top of the screen
        if self.rect.x <0:
            self.kill()
        if self.rect.x > WIDTH:
            self.kill

#Create Text
font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

#GameOver Screen
def show_go_screen():
    draw_text(screen,"BAŞLA!",50,WIDTH /2,HEIGHT/4)
    draw_text(screen,"Hareket etmek için; ",14,WIDTH/2,HEIGHT/2)
    draw_text(screen,"Robot1:A-D-TAB   Robot2:Yön Tuşları-RSHIFT",12,WIDTH/2,HEIGHT*2/3)
    draw_text(screen,"Başlamak için bir tuşa basın!",10,WIDTH/2,HEIGHT*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

#Energy Bars Function
def energie_bars(robot1_energy,robot2_energy):
    if robot1_energy >75:
        robot1_energy_color = GREEN
    
    elif robot1_energy >50:
        robot1_energy_color = YELLOW
    
    else:
        robot1_energy_color = RED

    if robot2_energy >75:
        robot2_energy_color = GREEN
    
    elif robot2_energy >50:
        robot2_energy_color = YELLOW
    
    else:
        robot2_energy_color = RED
    
    if robot1_energy < 0:
        robot1_energy = 0

        
    elif robot2_energy <0:
        robot2_energy = 0
        
    pygame.draw.rect(screen,robot1_energy_color,(5,10,robot1_energy/2,10))
    pygame.draw.rect(screen,robot2_energy_color,(145,10,robot2_energy/2,10))


#PENCERE OLUŞTURMA

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("ROBOWAR")
clock = pygame.time.Clock()

#Groups
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
robot1 = Robot1()
robot2 = Robot2()
robot1_groups = pygame.sprite.GroupSingle(robot1)
robot2_groups = pygame.sprite.GroupSingle(robot2)
all_sprites.add(robot1)
all_sprites.add(robot2)



#OYUN DÖNGÜSÜ
game_over = True
running  = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        bullets = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        robot1 = Robot1()
        robot2 = Robot2()
        robot1_groups = pygame.sprite.GroupSingle(robot1)
        robot2_groups = pygame.sprite.GroupSingle(robot2)
        all_sprites.add(robot1)
        all_sprites.add(robot2)

    #keep loop running at the right speed
    clock.tick(FPS)
        
    #Energy Bars
    robot1_energy = robot1.energy
    robot2_energy = robot2.energy
    if robot1_energy == 0:
        game_over=True
    
    if robot2_energy == 0:
        game_over=True
    #Process Input
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_TAB]:
        robot1.shoot()
    
    if keys[pygame.K_RSHIFT]:
        robot2.shoot()

    all_sprites.update()

    #Draw/render
    screen.fill(GREY)
    energie_bars(robot1_energy,robot2_energy)
    all_sprites.draw(screen)
    #*after* drawing  everything, flip the display
    pygame.display.flip()

pygame.quit()
