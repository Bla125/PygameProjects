import pygame
import sys
import os
import time
import math
import random
from pygame.locals import *


pygame.init() # initialize pygame
clock = pygame.time.Clock() # initialize clock
pygame.display.set_caption('Roguelike') # set window name

#########################################
#              Constants                #
#########################################
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600 # resolution
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # window width and height

BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)
ASSETS_PATH = 'RoguelikeAssets'


def main():

#########################################
#         Map images / functions        #
#########################################

    def load_image(image):
        image = pygame.image.load(os.path.join(ASSETS_PATH, image)).convert()
        image.set_colorkey((255, 255, 255)) # make white transparent
        return image

    green_background_img = pygame.image.load(os.path.join(ASSETS_PATH, 'green_background.png')).convert()
    brown_background_img = pygame.image.load(os.path.join(ASSETS_PATH, 'brown_background.png')).convert()
    blue_background_img = pygame.image.load(os.path.join(ASSETS_PATH, 'blue_background.png')).convert()

    def change_map(map_level):
        match map_level:
            case 1: return green_background_img
            case 2: return brown_background_img
            case 3: return blue_background_img
            case 4: return blue_background_img


#########################################
#        Menu images / functions        #
#########################################

    main_menu_img = pygame.image.load(os.path.join(ASSETS_PATH, 'main_menu.png')).convert()
    main_menu_location = (0, 0)
    play_button_location = (300, 100)
    main_menu_1_rect = pygame.Rect(play_button_location[0], play_button_location[1], 200, 65)
    main_menu_2_rect = pygame.Rect(play_button_location[0], play_button_location[1] + 70, 200, 65)
    main_menu_3_rect = pygame.Rect(play_button_location[0], play_button_location[1] + 140, 200, 65)


    weapon_menu_img = pygame.image.load(os.path.join(ASSETS_PATH, 'weapon_menu.png')).convert()
    weapon_menu_location = (WINDOW_WIDTH / 2 - weapon_menu_img.get_width() / 2,
                             WINDOW_HEIGHT / 2 - weapon_menu_img.get_height() / 2)
    weapon_menu_rect = pygame.Rect(weapon_menu_location[0], weapon_menu_location[1], weapon_menu_img.get_width(), weapon_menu_img.get_height())
    weapon_menu_1_rect = pygame.Rect(weapon_menu_location[0], weapon_menu_location[1], 100, 200)
    weapon_menu_2_rect = pygame.Rect(weapon_menu_location[0] + 100, weapon_menu_location[1], 100, 200)
    weapon_menu_3_rect = pygame.Rect(weapon_menu_location[0] + 200, weapon_menu_location[1], 100, 200)
    weapon_menu_4_rect = pygame.Rect(weapon_menu_location[0] + 300, weapon_menu_location[1], 100, 200)

    level_up_menu_img = pygame.image.load(os.path.join(ASSETS_PATH, 'level_up_menu.png')).convert()
    level_up_menu_location = (WINDOW_WIDTH / 2 - weapon_menu_img.get_width() / 2,
                               WINDOW_HEIGHT / 2 - weapon_menu_img.get_height() / 2)
    level_up_menu_1_rect = pygame.Rect(level_up_menu_location[0], level_up_menu_location[1], 100, 200)
    level_up_menu_2_rect = pygame.Rect(level_up_menu_location[0] + 100, level_up_menu_location[1], 100, 200)


#########################################
# Weapon variable / images / animations #
#########################################


    ############################
    #         Weapons          #
    ############################
    weapon_staff_img = pygame.image.load(os.path.join(ASSETS_PATH, 'weapon_staff.png')).convert()
    weapon_staff_img.set_colorkey((255, 255, 255)) # make white transparent

    weapon_revolver_img = pygame.image.load(os.path.join(ASSETS_PATH, 'weapon_revolver.png')).convert()
    weapon_revolver_img.set_colorkey((255, 255, 255)) # make white transparent
    weapon_revolver_img = pygame.transform.flip(weapon_revolver_img, True, False) # make revolver face left

    weapon_shuriken_img = pygame.image.load(os.path.join(ASSETS_PATH, 'weapon_shuriken.png')).convert()
    weapon_shuriken_img.set_colorkey((255, 255, 255)) # make white transparent

    weapon_poison_img = pygame.image.load(os.path.join(ASSETS_PATH, 'weapon_poison.png')).convert()
    weapon_poison_img.set_colorkey((255, 255, 255)) # make white transparent

    ############################
    #       Projectiles        #
    ############################
    projectile_frost_img = pygame.image.load(os.path.join(ASSETS_PATH, 'projectile_frost.png')).convert()
    projectile_frost_img.set_colorkey((255, 255, 255)) # make white transparent

    projectile_bullet_img = pygame.image.load(os.path.join(ASSETS_PATH, 'projectile_bullet.png')).convert()
    projectile_bullet_img.set_colorkey((255, 255, 255)) # make white transparent

    projectile_shuriken_img = pygame.image.load(os.path.join(ASSETS_PATH, 'projectile_shuriken.png')).convert()
    projectile_shuriken_img.set_colorkey((255, 255, 255)) # make white transparent

    projectile_poison_img = pygame.image.load(os.path.join(ASSETS_PATH, 'projectile_poison.png')).convert()
    projectile_poison_img.set_colorkey((255, 255, 255)) # make white transparent


#########################################
# Enemy variables / images / animations #
#########################################

    enemy_goblin_img = pygame.image.load(os.path.join(ASSETS_PATH, 'enemy_goblin.png')).convert()
    enemy_goblin_img.set_colorkey((255, 255, 255)) # make white transparent

    enemy_slime_img = pygame.image.load(os.path.join(ASSETS_PATH, 'enemy_slime.png')).convert()
    enemy_slime_img.set_colorkey((255, 255, 255)) # make white transparent

    enemy_golem_img = pygame.image.load(os.path.join(ASSETS_PATH, 'enemy_golem.png')).convert()
    enemy_golem_img.set_colorkey((255, 255, 255)) # make white transparent


#########################################
# Player variable / images / animations #
#########################################

    player_img = pygame.image.load(os.path.join(ASSETS_PATH, 'player_cat.png')).convert()
    player_img.set_colorkey((255, 255, 255)) # make white transparent
    player_location = [400, 300]
    player_rect = pygame.Rect(player_location[0], player_location[1], player_img.get_width(), player_img.get_height())

    player_speed = 2

    player_idle0 = pygame.image.load(os.path.join(ASSETS_PATH, 'player_cat_idle0.png')).convert()
    player_idle0.set_colorkey((255, 255, 255)) # make white transparent
    player_idle1 = pygame.image.load(os.path.join(ASSETS_PATH, 'player_cat_idle1.png')).convert()
    player_idle1.set_colorkey((255, 255, 255)) # make white transparent

    player_run0 = pygame.image.load(os.path.join(ASSETS_PATH, 'player_cat_run0.png')).convert()
    player_run0.set_colorkey((255, 255, 255)) # make white transparent
    player_run1 = pygame.image.load(os.path.join(ASSETS_PATH, 'player_cat_run1.png')).convert()
    player_run1.set_colorkey((255, 255, 255)) # make white transparent
    

    player_idle_animations = {0: player_idle0,
                              1: player_idle1}

    player_run_animations = {0: player_run0,
                             1: player_run1}




#########################################
#             Player class              #
#########################################

    class Player():
        def __init__(self, image, location, move_speed):
            self.location = location
            self.image = image
            self.death_count = 0
            self.move_speed = move_speed
            self.max_health = 10
            self.health = 10
            self.player_health_bar = [[20, 20], [120, 20]]
            self.level = 1
            self.experience = 0
            self.animation_timer = 0
            self.moving = False
            self.attack_cooldown = 0
            self.weapon_damage = 0
            self.weapon_speed = 0
            self.attack_speed_skill = 0
            self.attack_damage_skill = 0
            self.weapon = weapon_staff_img
            self.projectile = projectile_frost_img
            self.projectile_list = []
            self.projectile_speed = 0
            self.rect = player_rect
            self.hands_revolver = (15, 20) # position of hands relative to 0,0 of player image for revolver
            self.hands_shuriken = (7, 14) # position of hands relative to 0,0 of player image for shuriken
            self.hands_poison = (7, 14) # position of hands relative to 0,0 of player image for shuriken
            self.weapon_location_adjust = (0, 0) # weapon location adjust changes based on weapon used to make the weapon position properly
            self.chain_lightning_level = 1
            
        @property
        def attack_speed(self):
            return self.weapon_speed - self.attack_speed_skill

        @property
        def attack_damage(self):
            return self.weapon_damage + self.attack_damage_skill

        def move(self, direction):
            if direction == 'up' and self.rect.top >=0:
                self.location[1] -= self.move_speed * dt
            if direction == 'down' and self.rect.bottom <=600:
                self.location[1] += self.move_speed * dt
            if direction == 'left' and self.rect.left >=0:
                self.location[0] -= self.move_speed * dt
            if direction == 'right' and self.rect.right <=800:
                self.location[0] += self.move_speed * dt

        def draw(self):
            player.player_health_bar[1][0] = (player.health * 10) # update player health bar
            pygame.draw.lines(WINDOW, RED, False, self.player_health_bar, 10)
            WINDOW.blit(self.image, self.location)
            self.rect.x = self.location[0]
            self.rect.y = self.location[1]
            WINDOW.blit(self.weapon, (self.location[0] - self.weapon_location_adjust[0], self.location[1] + self.weapon_location_adjust[1]))
#           projectile[0] = image, projectile[1] = rect, [2] = speed_x, [3] = speed_y, [4] = pos_x, [5] = pos_y
            for projectile in self.projectile_list: # update projectile rect position
                # rects only work in ints, update floats pos_x and pos_y to get more accurate positions
                projectile[4] += projectile[2] * dt
                projectile[5] += projectile[3] * dt
                projectile[1].center = round(projectile[4]), round(projectile[5]) # round positions to become int for rect
                WINDOW.blit(projectile[0], (projectile[4], projectile[5]))

        def idle(self, idle_animation_dict):
            self.animation_timer += 1
            if self.animation_timer <= 29:
                self.image = idle_animation_dict[0]
            elif self.animation_timer >= 30:
                self.image = idle_animation_dict[1]
            if self.animation_timer > 59:
                self.animation_timer = 0

        def run(self, run_animation_dict):
            self.animation_timer += 1
            if self.animation_timer <= 6:
                self.image = run_animation_dict[0]
            elif self.animation_timer >= 7:
                self.image = run_animation_dict[1]
            if self.animation_timer > 14:
                self.animation_timer = 0          

        def shoot_projectile(self, speed_x, speed_y, proj_img_angle):
            projectile_rect = pygame.Rect(self.location[0] - self.weapon_location_adjust[0], self.location[1] + self.weapon_location_adjust[1], self.projectile.get_width(), self.projectile.get_height())
            pos_x = projectile_rect.x
            pos_y = projectile_rect.y
            rotated_image = pygame.transform.rotate(self.projectile, proj_img_angle) # rotate the projectile image towards location being shot
            self.projectile_list.append([rotated_image, projectile_rect, speed_x, speed_y, pos_x, pos_y])

        def projectile_wall_collision(self):
#           projectile[0] = image, projectile[1] = rect, [2] = speed_x, [3] = speed_y
            for projectile in self.projectile_list:
                if projectile[1].top <= 0:
                    self.projectile_list.remove(projectile)
                elif projectile[1].bottom >= 600:
                    self.projectile_list.remove(projectile)
                elif projectile[1].left <= 0:
                    self.projectile_list.remove(projectile)
                elif projectile[1].right >= 800:
                    self.projectile_list.remove(projectile)
    

#########################################
#             Enemy class               #
#########################################
    
    class Enemy():
        def __init__(self, type, health, movement_speed, attack_damage, image, location):
            self.type = type
            self.health = health
            self.image = image
            self.location = location
            self.movement_speed = movement_speed
            self.rect = pygame.Rect(self.location[0], self.location[1], self.image.get_width(), self.image.get_height())
            self.attack_damage = attack_damage
            self.poisoned = False
            self.poisoned_timer = 0
            self.slowed = False

        def draw(self):
            self.movement()
            WINDOW.blit(self.image, self.location)
            self.rect.x = self.location[0]
            self.rect.y = self.location[1]

        def animation(self):
            raise NotImplementedError('need to create animations')
        
        def create_new(type):
            if type == 'goblin':
                return Enemy('goblin', 2, 1, 1, enemy_goblin_img, [random.randint(20, 600), random.randint(20, 100)])
            elif type == 'slime':
                return Enemy('slime', 2, 1, 1, enemy_slime_img, [random.randint(20, 600), random.randint(20, 100)])
            if type == 'golem':
                return Enemy('golem', 50, 1, 3, enemy_golem_img, [random.randint(20, 600), random.randint(20, 100)])

        def movement(self):
            # function to make enemy move towards the player
            player_x, player_y = player.location[0], player.location[1]
            distance_x = player_x - self.location[0]
            distance_y = player_y - self.location[1]
            angle = math.atan2(distance_y, distance_x)
            speed_x = self.movement_speed * math.cos(angle)
            speed_y = self.movement_speed * math.sin(angle)
            self.location[0] += speed_x * dt
            self.location[1] += speed_y * dt


#########################################
#          Debuff/DOT Function          #
#########################################

    def debuff_dot():
        raise NotImplementedError('need to move code from projectile collision into function')


#########################################
#        Closest Enemies Function       #
#########################################
#       takes in enemy hit and a number for how many chains
    def closest_enemies(current_enemy, num_chains):
        enemies_to_hit = []
        enemy_coords = []
        for i in range(num_chains):
            close_enemies = [enemy for enemy in enemy_list if enemy is not current_enemy] # make list of enemies, NOT including the enemy hit
            closest_enemy = min([enemy for enemy in close_enemies if enemy not in enemies_to_hit], key=lambda enemy: pow(enemy.rect.centerx - current_enemy.rect.centerx, 2) 
                                                                                    + pow(enemy.rect.centery - current_enemy.rect.centery, 2)) # find the closest enemy to the enemy hit
            enemies_to_hit.append(closest_enemy)
            enemy_coords.append((closest_enemy.rect.centerx, closest_enemy.rect.centery))
        return enemies_to_hit, enemy_coords


#########################################
#         Display Text Function         #
#########################################

    def draw_text(msg, color, location_x, location_y):
        font = pygame.font.SysFont(None, 25)
        text = font.render(msg, True, color)

        if location_x == 'center':
            location_x = WINDOW_WIDTH / 2 - text.get_width() / 2

        if location_y == 'center':
            location_y = WINDOW_HEIGHT / 2 - text.get_height() / 2
        elif location_y == 'center_top':
            location_y = WINDOW_HEIGHT / 2 - text.get_height() / 2 - 200
            
        WINDOW.blit(text, (location_x, location_y))


#########################################
#            Declarations               #
#########################################
#   initialize player
    player = Player(player_img, player_location, player_speed)
    player.weapon = weapon_staff_img
    player.projectile = projectile_frost_img

#   list containing all spawned enemies
    enemy_list = []

    map_level = 0
    new_map = True
    end_of_level = False

    main_menu = True
    weapon_menu = True
    level_up_menu = False

    poison_clock = time.time()

    chain_lightning = False
    lightning_timer = 0

    restart = False

    dt = 0
    prev_time = time.time()

#########################################
#              Game Loop                #
#########################################
    while True:
        # compute delta time
        dt = time.time() - prev_time
        dt *= 60
        prev_time = time.time()


#########################################
#              Main Menu                #
#########################################

        if main_menu == True:
            WINDOW.blit(main_menu_img, main_menu_location) # draw menu on screen
            pygame.display.update() # update display
            while main_menu == True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit() # stop pygame
                        sys.exit() # stop program
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse_pos = pygame.mouse.get_pos()
                            if pygame.Rect.collidepoint(main_menu_1_rect, mouse_pos):
                                main_menu = False
                            elif pygame.Rect.collidepoint(main_menu_2_rect, mouse_pos):
                                print('Need to implement settings menu')
                                pass
                            elif pygame.Rect.collidepoint(main_menu_3_rect, mouse_pos):
                                pygame.quit()
                                sys.exit()


#########################################
#              Change Map               #
#########################################

#       Check if enemy list is empty
        if not enemy_list and map_level > 0:
            end_of_level = True         

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE] and end_of_level == True:
            end_of_level = False
            new_map = True

        if new_map == True:
            player.location = [400,300]
            new_map = False
            map_level += 1
            if map_level % 4 == 0:
                level_up_menu = True
                player.level += 1
            map = change_map(map_level)
            match map_level:
                case 1:
                    for i in range(4):
                        enemy_list.append(Enemy.create_new('goblin'))
                case 2:
                    for i in range(6):
                        enemy_list.append(Enemy.create_new('slime'))
                case 3:
                    enemy_list.append(Enemy.create_new('golem'))
                case 4:
                    for i in range(6):
                        enemy_list.append(Enemy.create_new('goblin'))
                        enemy_list.append(Enemy.create_new('slime'))

#########################################
#                Draw                   #
#########################################  

        WINDOW.blit(map, (0, 0))

        player.draw()

        for enemy in enemy_list:
            enemy.draw()

        if end_of_level == True:
            draw_text('Press ESC to continue to next level', WHITE, 'center', 'center_top')


#########################################
#           Main Event Loop             #
#########################################

        for event in pygame.event.get():
            if event.type == QUIT: # check for window exit
                pygame.quit() # stop pygame
                sys.exit() # stop program
# KEYUP used to stop the movement animations of the player
            if event.type == KEYDOWN:
                if event.key == K_c:
                    player.attack_damage_skill += 10
            if event.type == KEYUP:
                if event.key == K_w:
                    player.moving = False
                if event.key == K_s:
                    player.moving = False
                if event.key == K_a:
                    player.moving = False
                if event.key == K_d:
                    player.moving = False
# MOUSEBUTTONUP used to set attack cooldown back to zero, so the next attack won't have a delay
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    player.attack_cooldown = 0
# trigger attack cooldown timer after mouse up to trigger cooldown timer after mouse button up


#########################################
#     Weapon Select Menu Event Loop     #
#########################################
        
        if weapon_menu == True:
            WINDOW.blit(weapon_menu_img, weapon_menu_location) # draw menu on screen
            pygame.display.update() # update display
            while weapon_menu == True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse_pos = pygame.mouse.get_pos()
                            if pygame.Rect.collidepoint(weapon_menu_1_rect, mouse_pos):
                                player.weapon = weapon_staff_img
                                player.projectile = projectile_frost_img
                                player.projectile_speed = 5
                                player.weapon_speed = 10
                                player.weapon_damage = 1
                                weapon_menu = False
                            elif pygame.Rect.collidepoint(weapon_menu_2_rect, mouse_pos):
                                player.weapon = weapon_revolver_img
                                player.projectile = projectile_bullet_img
                                player.projectile_speed = 5
                                player.weapon_location_adjust = player.hands_revolver
                                player.weapon_speed = 10
                                player.weapon_damage = 1
                                weapon_menu = False
                            elif pygame.Rect.collidepoint(weapon_menu_3_rect, mouse_pos):
                                player.weapon = weapon_shuriken_img
                                player.projectile = projectile_shuriken_img
                                player.projectile_speed = 5
                                player.weapon_location_adjust = player.hands_shuriken
                                player.weapon_speed = 10
                                player.weapon_damage = 1
                                weapon_menu = False
                            elif pygame.Rect.collidepoint(weapon_menu_4_rect, mouse_pos):
                                player.weapon = weapon_poison_img
                                player.projectile = projectile_poison_img
                                player.projectile_speed = 5
                                player.weapon_location_adjust = player.hands_poison
                                player.weapon_speed = 10
                                player.weapon_damage = .5
                                weapon_menu = False
                prev_time = time.time() # update delta time, don't add time passed while in the menu


#########################################
#        Level Up Menu Event Loop       #
#########################################

        if level_up_menu == True:
            draw_text('LEVEL UP!!!', WHITE, 'center', 'center_top') # draw 'LEVEL UP!!!' on the screen
            WINDOW.blit(level_up_menu_img, weapon_menu_location) # draw menu on screen
            pygame.display.update() # update display
            while level_up_menu == True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse_pos = pygame.mouse.get_pos()
                            if pygame.Rect.collidepoint(level_up_menu_1_rect, mouse_pos):
                                player.attack_damage_skill +=1
                                level_up_menu = False
                            elif pygame.Rect.collidepoint(level_up_menu_2_rect, mouse_pos):
                                player.attack_speed_skill += 2
                                level_up_menu = False
                prev_time = time.time() # update delta time, don't add time passed while in the menu


#########################################
#    Level Transition Menu Event Loop   #
#########################################
                


#########################################
#           Player Attack               #
#########################################


        if pygame.mouse.get_pressed()[0]:
            ##### code to shoot towards the mouse cursor
            mouse_x, mouse_y = pygame.mouse.get_pos()
            distance_x = mouse_x - player.location[0]
            distance_y = mouse_y - player.location[1] - player.weapon_location_adjust[1] # adjust the location based on where the weapon is on the player
            angle = math.atan2(distance_y, distance_x)
            proj_img_angle = 270-math.atan2(distance_y, distance_x)*180/math.pi
            speed_x = player.projectile_speed * math.cos(angle)
            speed_y = player.projectile_speed * math.sin(angle)
            player.attack_cooldown += 1
            if player.attack_cooldown == player.attack_speed:
                player.shoot_projectile(speed_x, speed_y, proj_img_angle)
                player.attack_cooldown = 0


#########################################
#           Player Movement             #
#########################################

        keys = pygame.key.get_pressed()
        if keys[K_w]:
            player.move('up')
            player.moving = True
        if keys[K_s]:
            player.move('down')
            player.moving = True
        if keys[K_a]:
            player.move('left')
            player.moving = True
        if keys[K_d]:
            player.move('right')
            player.moving = True

#       Change player 
        if player.moving == True:
            player.run(player_run_animations)
        elif player.moving == False:
            player.idle(player_idle_animations)


#########################################
#           Player Collision            #
#########################################

        for enemy in enemy_list:
            if pygame.Rect.colliderect(enemy.rect, player.rect):
                player.health -= enemy.attack_damage * dt
                print(player.health)
                if player.health <= 0:
                    player.death_count += 1
                    restart = True # triggers restart of game on death


#########################################
#          Projectile Collision         #
#########################################

#       Check for projectile collision with walls
        player.projectile_wall_collision()

#       Check for projectile collision with enemies
        for projectile in player.projectile_list:
            for enemy in enemy_list:
                if pygame.Rect.colliderect(enemy.rect, projectile[1]):
                    player.projectile_list.remove(projectile)
                    enemy.health -= player.attack_damage
                    current_enemy = enemy

                    if player.weapon == weapon_shuriken_img: # apply chain lightning damage and get enemies hit by chain lightning
                        try:
                            chain_coords_list = []
                            chain_hit_list, chain_coords = closest_enemies(current_enemy, player.chain_lightning_level) # returns list of enemies hit by chain lightning
                            chain_coords_list.append([(current_enemy.rect.centerx, current_enemy.rect.centery), chain_coords[0]]) # add first pair of coords for chain lightning

                            for enemy in chain_hit_list: # apply chain lightning damage
                                enemy.health -= player.attack_damage

                            for i in range(len(chain_coords)-1): # make paired coords for enemies hit
                                chain_coords_list.append([chain_coords[i], chain_coords[i + 1]])
                            chain_lightning = True
                        except: pass

                    elif player.weapon == weapon_poison_img: # apply poisoned debuff
                        enemy.poisoned = True
                        enemy.poisoned_timer = 10
                        
                    if enemy.health <= 0:
                        enemy_list.remove(enemy)
                    break


#       Draw the chain lightning
        if chain_lightning == True:
            if lightning_timer <= 4:
                for i in range(len(chain_coords_list)):
                    pygame.draw.aalines(WINDOW, YELLOW, False, chain_coords_list[i], 2)
                lightning_timer += 1
            else: 
                chain_lightning = False
                lightning_timer = 0


#       Apply poison damage
        for enemy in enemy_list:        
            if enemy.poisoned == True:
                if time.time() - poison_clock > .1: # calculate how much time has passed since last poison damage tick
                    enemy.health -= .2
                    enemy.poisoned_timer -= 1
                    poison_clock = time.time()
            if enemy.poisoned_timer <= 0:
                enemy.poisoned = False
            if enemy.health <= 0:
                enemy_list.remove(enemy)


#       start from beginning, but with all skills and stats gained so far
        if restart == True:
            if player.death_count > 3: # if player dies more than 3 times, start over without skills and stats gained
                main()
            restart = False
            new_map = True # trigger map change
            map_level = 0 # set map level to 0, will increase to 1 on map change
            enemy_list = [] # reset enemy list
            player.health = player.max_health # reset player health
            

        pygame.display.update() # update display
        clock.tick(60) # fps

if __name__ == '__main__':
    main()