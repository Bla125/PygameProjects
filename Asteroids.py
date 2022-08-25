import random
import pygame
import sys
import os
import time
import math
from pygame.locals import *

pygame.init() # initiate pygame
clock = pygame.time.Clock() # setup the clock
pygame.display.set_caption('Asteroids') # setup the window name
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BLACK = (0,0,0)
WHITE = (255,255,255)

#########################################
#               Images                  #
#########################################

def main():  
    
    background_img = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space_background.png')).convert(), (WINDOW_WIDTH, WINDOW_HEIGHT))

    ship_img = pygame.image.load(os.path.join('Assets', 'spaceship.png')).convert()
    ship_img.set_colorkey((255, 255, 255))
    ship_location = [400, 300]

    big_asteroid_img = pygame.image.load(os.path.join('Assets', 'big_asteroid.png')).convert()
    big_asteroid_img.set_colorkey((255, 255, 255))

    small_asteroid_img = pygame.image.load(os.path.join('Assets', 'small_asteroid.png')).convert()
    small_asteroid_img.set_colorkey((255, 255, 255))

    asteroid_images = [big_asteroid_img, small_asteroid_img]

    ship_rect = pygame.Rect(ship_location[0], ship_location[1], ship_img.get_width()-15, ship_img.get_height()-17)

    GAMEOVER_FONT = pygame.font.SysFont('comicsans', 100)
    GAMEOVER_TEXT = GAMEOVER_FONT.render('GAME OVER', 1, WHITE)

    #########################################
    #              Asteroids                #
    #########################################

    class Asteroid():
        def __init__(self, image, location):
            self.location = location
            self.image = image
            self.x_velocity = 1
            self.y_velocity = 1

        def get_rect(self):
            if self.image == big_asteroid_img:
                rect = pygame.Rect(self.location[0], self.location[1],self.image.get_width()-22,self.image.get_height()-25)
            else:
                rect = pygame.Rect(self.location[0], self.location[1],self.image.get_width()-15,self.image.get_height()-10)
            return rect

        def screen_collision(self):
            if self.location[0] > WINDOW_WIDTH - self.image.get_width():
                self.x_velocity = -2
            elif self.location[0] < 0:
                self.x_velocity = 2

            if self.location[1] > WINDOW_HEIGHT - self.image.get_height():
                self.y_velocity = -2
            elif self.location[1] < 0:
                self.y_velocity = 2

        def move(self, rect):
            if self.image == big_asteroid_img:
                # Make rect follow image
                self.screen_collision()
                self.location[0] += round(self.x_velocity)
                self.location[1] += round(self.y_velocity)
                rect.x = self.location[0] +10
                rect.y = self.location[1] +10
            else:
                # Make rect follow image
                self.screen_collision()
                self.location[0] += self.x_velocity
                self.location[1] += self.y_velocity
                rect.x = self.location[0] +7
                rect.y = self.location[1] +7

        def draw(self):
                WINDOW.blit(self.image, self.location)


    asteroid_dict = {}


    def generate_asteroid_list(level):
        for i in range(level):
            asteroid_type = random.randint(0, 1)
            rand_location = random.randint(1, 4)
            if asteroid_type == 1: 
                if rand_location == 1:           
                    asteroid = Asteroid(big_asteroid_img,[-50, random.randint(-50, 650)])
                elif rand_location == 2:
                    asteroid = Asteroid(big_asteroid_img,[random.randint(-50, 850), -50])
                elif rand_location == 3:
                    asteroid = Asteroid(big_asteroid_img,[850, random.randint(-50, 650)])
                elif rand_location == 4:
                    asteroid = Asteroid(big_asteroid_img,[random.randint(-50, 850), 650])
            else:
                if rand_location == 1:
                    asteroid = Asteroid(small_asteroid_img,[-50, random.randint(-50, 650)])
                elif rand_location ==2:
                    asteroid = Asteroid(small_asteroid_img,[random.randint(-50, 850), -50])
                elif rand_location == 3:
                    asteroid = Asteroid(small_asteroid_img,[850, random.randint(-50, 650)])
                elif rand_location == 4:
                    asteroid = Asteroid(small_asteroid_img,[random.randint(-50, 850), 650])
            asteroid_dict[asteroid] = asteroid.get_rect()


    #########################################
    #               Bullets                 #
    #########################################

    bullet_list = []
    max_bullets = 10
    bullet_velocity = 10

    def handle_bullets(bullet_list, asteroid_dict):
        bullet_removed = False
        for bullet in bullet_list:
    #       bullet = bullet, speed_x, speed_y
            bullet[0].x += bullet[1] * dt
            bullet[0].y += bullet[2] * dt
            for asteroid, ast_rect in list(asteroid_dict.items()):
                if bullet[0].colliderect(asteroid_dict[asteroid]): 
                    bullet_list.remove(bullet)
                    asteroid_dict.pop(asteroid)
                    bullet_removed = True
                    break
            if bullet_removed == True:
                bullet_removed = False
                continue
            if bullet[0].x < 0 or bullet[0].x > WINDOW_WIDTH:
                bullet_list.remove(bullet)
            elif bullet[0].y < 0 or bullet[0].y > WINDOW_HEIGHT:
                bullet_list.remove(bullet)


    up_velocity = 1
    down_velocity = 1
    left_velocity = 1
    right_velocity = 1
    up_accel = 0
    down_accel = 0
    left_accel = 0
    right_accel = 0
    moving_up = False
    moving_down = False
    moving_left = False
    moving_right = False

    new_level = True
    level = 0

    GAMEOVER = pygame.USEREVENT + 1
    restart = False

    dt = 0
    prev_time = time.time()

    while True:
        clock.tick(60) # 60 fps
        # compute delta time
        dt = time.time() - prev_time
        dt *= 60
        prev_time = time.time()  

    # Make ship rect follow the ship
        ship_rect.x = ship_location[0] - (ship_img.get_width()/2) + 7
        ship_rect.y = ship_location[1] - (ship_img.get_height()/2) + 10

    #########################################
    #                Draw                   #
    #########################################   
        WINDOW.blit(background_img, (0, 0))

        handle_bullets(bullet_list, asteroid_dict)
        for bullet in bullet_list:
                pygame.draw.rect(WINDOW, WHITE, bullet[0])

    #########################################
    #         Asteroid Draw/Movement        #
    ######################################### 
    # Generate and spawn new enemies at start of new level
        if len(asteroid_dict) == 0:
            new_level = True
            level += 1

        if new_level == True:
            generate_asteroid_list(level)
        new_level = False

    # Track enemy movement
        for asteroid in asteroid_dict:
            current_img = asteroid
            current_rect = asteroid_dict[asteroid]
            current_img.move(current_rect)
            current_img.draw()

    #########################################
    #            Player Movement            #
    #########################################
    # Ship movement and acceleration
        if moving_up:
            ship_location[1] -= up_velocity + up_accel * dt
            up_accel += .17
        if moving_down:
            ship_location[1] += down_velocity + down_accel * dt
            down_accel += .17
        if moving_left:
            ship_location[0] -= left_velocity + left_accel * dt
            left_accel += .17
        if moving_right:
            ship_location[0] += right_velocity + right_accel * dt
            right_accel += .17

    # Ship drag
        if up_accel > 0:
            ship_location[1] -= up_accel
            up_accel -= .1
        if down_accel > 0:
            ship_location[1] += down_accel
            down_accel -= .1
        if left_accel > 0:
            ship_location[0] -= left_accel
            left_accel -= .1    
        if right_accel > 0:
            ship_location[0] += right_accel
            right_accel -= .1

    # Make ship point at mouse cursor        
        pos = pygame.mouse.get_pos()
        angle = 270-math.atan2(pos[1]-ship_location[1],pos[0]-ship_location[0])*180/math.pi
        rotimage = pygame.transform.rotate(ship_img,angle)
        rect = rotimage.get_rect(center=(ship_location))
        WINDOW.blit(rotimage,rect)

    #########################################
    #            Player Collision           #
    #########################################
    # Ship collision and bounch with border
        if ship_location[1] < 0:
            ship_location[1] = 0 + 5       
            down_accel = 5
            up_accel = 0
        if ship_location[1] + ship_img.get_height() > WINDOW_HEIGHT:
            ship_location[1] = WINDOW_HEIGHT - ship_img.get_height() - 5       
            down_accel = 0
            up_accel = 5
        if ship_location[0] < 0:
            ship_location[0] = 0 + 5       
            left_accel = 0
            right_accel = 5
        if ship_location[0] + ship_img.get_width() > WINDOW_WIDTH:
            ship_location[0] = WINDOW_WIDTH - ship_img.get_width() - 5       
            left_accel = 5
            right_accel = 0

        for asteroid in asteroid_dict:
            if ship_rect.colliderect(asteroid_dict[asteroid]):
                pygame.event.post(pygame.event.Event(GAMEOVER))

    #########################################
    #             Event Loop                #
    #########################################
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                pygame.quit() # stop pygame
                sys.exit() # stop script
            if event.type == KEYDOWN: # Movement keys
                if event.key == K_w:
                    moving_up = True
                if event.key == K_s:
                    moving_down = True
                if event.key == K_a:
                    moving_left = True
                if event.key == K_d:
                    moving_right = True
            if event.type == KEYUP:
                if event.key == K_w:
                    moving_up = False
                if event.key == K_s:
                    moving_down = False
                if event.key == K_a:
                    moving_left = False
                if event.key == K_d:
                    moving_right = False
            if event.type == MOUSEBUTTONDOWN: # Fire bullet 
                if event.button == 1 and len(bullet_list) < max_bullets:
                    bullet = pygame.Rect(ship_location[0], ship_location[1], 5, 5)
                    mouse_x, mouse_y = pygame.mouse.get_pos() 
                    distance_x = mouse_x - ship_location[0]
                    distance_y = mouse_y - ship_location[1]
                    angle = math.atan2(distance_y, distance_x)
                    speed_x = bullet_velocity * math.cos(angle)
                    speed_y = bullet_velocity * math.sin(angle)              
                    bullet_list.append([bullet, speed_x, speed_y])
            if event.type == GAMEOVER:
                WINDOW.blit(GAMEOVER_TEXT, (WINDOW_WIDTH / 2 - GAMEOVER_TEXT.get_width() / 2,
                                             WINDOW_HEIGHT / 2 - GAMEOVER_TEXT.get_height() / 2))
                pygame.display.update()                
                pygame.time.delay(3000)
                restart = True

        if restart == True:            
            restart == False
            break

        pygame.display.update() # update display

    main()

if __name__ == "__main__":
    main()