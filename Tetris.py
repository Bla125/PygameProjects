from pdb import Restart
from turtle import clear, window_width
import pygame
import sys
import time
import random
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Tetris')
WIN_WIDTH, WIN_HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
BOARD_SURFACE = pygame.Surface((250, 500))

BLACK = (0, 0, 0)
SILVER = (192, 192, 192)
GRAY = (128, 128, 128)
DARK_GRAY = (99, 102, 106)
WHITE = (255, 255, 255)
LIGHT_BLUE = (0, 255, 255) # I
DARK_BLUE = (0, 0, 255) # J
ORANGE = (255, 165, 0) # L
PURPLE = (255, 0, 255) # T
YELLOW = (255, 255, 0) # Square
GREEN = (0, 255, 0) # S
RED = (255, 0, 0) # Z

BLOCK_WIDTH = 25
BLOCK_HEIGHT = 25

START_POS_X = (125)
START_POS_Y = (0)
ONE_BLOCK = 25

GAMEOVER_FONT = pygame.font.SysFont('comicsans', 20)
GAMEOVER_TEXT = GAMEOVER_FONT.render('GAME OVER', 1, WHITE)


def main():

    class Shapes():
        def __init__(self, shape_type, color):
            self.location = [START_POS_X, START_POS_Y]
            self.shape_type = shape_type
            self.color = color
            self.velocity = 1

        def get_rect(self):
            if self.shape_type == '1': # L
                rect1 = pygame.Rect(self.location[0], self.location[1], BLOCK_WIDTH, BLOCK_HEIGHT)
                rect2 = pygame.Rect(self.location[0], self.location[1] + ONE_BLOCK, BLOCK_WIDTH, BLOCK_HEIGHT)
                rect3 = pygame.Rect(self.location[0], self.location[1] + ONE_BLOCK * 2, BLOCK_WIDTH, BLOCK_HEIGHT)
                rect4 = pygame.Rect(self.location[0] + ONE_BLOCK, self.location[1] + ONE_BLOCK * 2, BLOCK_WIDTH, BLOCK_HEIGHT)
                return [rect1, rect2, rect3, rect4]

            elif self.shape_type == '2': # J
                rect1 = pygame.Rect(self.location[0], self.location[1], BLOCK_WIDTH, BLOCK_HEIGHT)
                rect2 = pygame.Rect(self.location[0], self.location[1] + ONE_BLOCK, BLOCK_WIDTH, BLOCK_HEIGHT)
                rect3 = pygame.Rect(self.location[0], self.location[1] + ONE_BLOCK * 2, BLOCK_WIDTH, BLOCK_HEIGHT)
                rect4 = pygame.Rect(self.location[0] - ONE_BLOCK, self.location[1] + ONE_BLOCK * 2, BLOCK_WIDTH, BLOCK_HEIGHT)
                return [rect1, rect2, rect3, rect4]

            elif self.shape_type == '3': # T
                rect1 = pygame.Rect(self.location[0], self.location[1], BLOCK_WIDTH, BLOCK_HEIGHT)
                rect2 = pygame.Rect(self.location[0], self.location[1] + ONE_BLOCK, BLOCK_WIDTH, BLOCK_HEIGHT)
                rect3 = pygame.Rect(self.location[0] - ONE_BLOCK, self.location[1] + ONE_BLOCK, BLOCK_WIDTH, BLOCK_HEIGHT)
                rect4 = pygame.Rect(self.location[0] + ONE_BLOCK, self.location[1] + ONE_BLOCK, BLOCK_WIDTH, BLOCK_HEIGHT)
                return [rect1, rect2, rect3, rect4]

            elif self.shape_type == '4': # S
                rect1 = pygame.Rect(self.location[0], self.location[1], BLOCK_WIDTH, BLOCK_HEIGHT)
                rect2 = pygame.Rect(self.location[0], self.location[1] + ONE_BLOCK, BLOCK_WIDTH, BLOCK_HEIGHT)
                rect3 = pygame.Rect(self.location[0] + ONE_BLOCK, self.location[1], BLOCK_WIDTH, BLOCK_HEIGHT)
                rect4 = pygame.Rect(self.location[0] - ONE_BLOCK, self.location[1] + ONE_BLOCK, BLOCK_WIDTH, BLOCK_HEIGHT)
                return [rect1, rect2, rect3, rect4]

            elif self.shape_type == '5': # Z
                rect1 = pygame.Rect(self.location[0], self.location[1], BLOCK_WIDTH, BLOCK_HEIGHT)
                rect2 = pygame.Rect(self.location[0], self.location[1] + ONE_BLOCK, BLOCK_WIDTH, BLOCK_HEIGHT)
                rect3 = pygame.Rect(self.location[0] - ONE_BLOCK, self.location[1], BLOCK_WIDTH, BLOCK_HEIGHT)
                rect4 = pygame.Rect(self.location[0] + ONE_BLOCK, self.location[1] + ONE_BLOCK, BLOCK_WIDTH, BLOCK_HEIGHT)
                return [rect1, rect2, rect3, rect4]

            elif self.shape_type == '6': # Line
                rect1 = pygame.Rect(self.location[0], self.location[1], BLOCK_WIDTH, BLOCK_HEIGHT)
                rect2 = pygame.Rect(self.location[0], self.location[1] + ONE_BLOCK, BLOCK_WIDTH, BLOCK_HEIGHT)
                rect3 = pygame.Rect(self.location[0], self.location[1] + ONE_BLOCK * 2, BLOCK_WIDTH, BLOCK_HEIGHT)
                rect4 = pygame.Rect(self.location[0], self.location[1] + ONE_BLOCK * 3, BLOCK_WIDTH, BLOCK_HEIGHT)
                return [rect1, rect2, rect3, rect4]

            elif self.shape_type == '7': # Square
                rect1 = pygame.Rect(self.location[0], self.location[1], BLOCK_WIDTH, BLOCK_HEIGHT)
                rect2 = pygame.Rect(self.location[0] - ONE_BLOCK, self.location[1], BLOCK_WIDTH, BLOCK_HEIGHT)
                rect3 = pygame.Rect(self.location[0], self.location[1] + ONE_BLOCK, BLOCK_WIDTH, BLOCK_HEIGHT)
                rect4 = pygame.Rect(self.location[0] - ONE_BLOCK, self.location[1] + ONE_BLOCK, BLOCK_WIDTH, BLOCK_HEIGHT)
                return [rect1, rect2, rect3, rect4]


        def block_adjust(self, rect, amount):
            for i in range(4):
                rect[i].y -= amount

        def gravity(self, rect):
            rect.y += self.velocity

        def move(self, rect, direction):
            if direction == 'down':
                rect.y += 5
            if direction == 'left':  
                rect.x -= 25
            if direction == 'right':
                rect.x += 25

# do a screen collision left and right
        def screen_collision(self, rect, direction):
            if direction == 'left':
                if rect.x <= 0:
                    return True
            elif direction == 'right':
                if rect.x + 25 >= 250:
                    return True

        def bottom_collision(self, rect):
            for i in range(4):
                if rect[i].y + BLOCK_HEIGHT >= 500:
                    return True

        def top_collision(self, rect):
            for i in range(4):
                if rect[i].y == 1:
                    return True

            
        def rotate(self, rect):
            for i in range(4):
                x = rect[i].x
                y = rect[i].y
                if i == 1: # 1 is the center the shape, does not rotate
                    continue
                if rect[i].y < rect[1].y:
                    y += (rect[1].y - rect[i].y) + (rect[i].x - rect[1].x)
                    x += (rect[1].x - rect[i].x) + (rect[1].y - rect[i].y)

                elif rect[i].y == rect[1].y and rect[i].x > rect[1].x:
                    y += (rect[i].x - rect[1].x)
                    x -= (rect[i].x - rect[1].x)

                elif rect[i].y > rect[1].y:
                    y -= (rect[i].y - rect[1].y) + (rect[1].x - rect[i].x)
                    x -= (rect[i].x - rect[1].x) + (rect[i].y - rect[1].y)

                elif rect[i].y == rect[1].y and rect[i].x < rect[1].x:
                    y -= (rect[1].x - rect[i].x)
                    x += (rect[1].x - rect[i].x)
                rect[i].x = x
                rect[i].y = y

        def draw(self,rect):
            pygame.draw.rect(BOARD_SURFACE, self.color, rect)
            

    new_shape = True
    current_shape = {}
    board_dict = {}
    block_rect_list = []
    collide_delay = 0

    clear_line = False
    restart = False

    # delta time
    dt = 0
    prev_time = time.time()

    while True:
        clock.tick(60)
        dt = time.time() - prev_time
        dt *= 60
        prev_time = time.time()

########################################################
#                       Draw                           #
########################################################        
        WIN.fill(BLACK)
        BOARD_SURFACE.fill(DARK_GRAY)

        if new_shape == True:
            new_shape = False
            new_type = str(random.randint(1,7)) # create random int and cast as string
            match new_type:
                # color for the shapes rect
                case '1': color = ORANGE
                case '2': color = DARK_BLUE
                case '3': color = PURPLE
                case '4': color = GREEN
                case '5': color = RED
                case '6': color = LIGHT_BLUE
                case '7': color = YELLOW
            shape = Shapes(new_type, color)
            current_shape[shape] = shape.get_rect()
      
#       Draw the block controlled by the player
        for block in current_shape:
            for rect in current_shape[block]:
                block.draw(rect)
                block.gravity(rect)

#       Draw blocks on the board that were placed by the player
        for block in board_dict:
            for rect in board_dict[block]:
                block.draw(rect)
                    
#       Event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    collide = False
                    for block in current_shape:
                        for rect in current_shape[block]:
                            check = block.screen_collision(rect, 'left')
                            if check == True:
                                collide = True
                            for i in range(0,len(block_rect_list)):
                                board_rect = block_rect_list[i]
                                if (board_rect.y == rect.y - 1 or (board_rect.y > rect.y - 1 and board_rect.y < rect.y - 1 + 25) or (rect.y - 1 > board_rect.y and rect.y - 1 < board_rect.y + 25)) and board_rect.x == rect.x - 25:
                                    collide = True
                    if collide == False:
                        for block in current_shape:
                            for rect in current_shape[block]:
                                block.move(rect, 'left')
                if event.key == K_RIGHT:
                    collide = False
                    for block in current_shape:
                        for rect in current_shape[block]:
                            check = block.screen_collision(rect, 'right')
                            if check == True:
                                collide = True
                            for i in range(0,len(block_rect_list)):
                                board_rect = block_rect_list[i]
                                if (board_rect.y == rect.y - 1 or (board_rect.y > rect.y - 1 and board_rect.y < rect.y - 1 + 25) or (rect.y - 1 > board_rect.y and rect.y - 1 < board_rect.y + 25)) and board_rect.x == rect.x + 25:
                                    collide = True
                    if collide == False:                    
                        for block in current_shape:
                            for rect in current_shape[block]:
                                block.move(rect, 'right')
                if event.key == K_UP:
                    check_left = []             
                    check_right = []             
                    block.rotate(current_shape[shape])
                    for block in current_shape:
                        for rect in current_shape[block]:
                            check_left.append(block.screen_collision(rect, 'left'))
                            check_right.append(block.screen_collision(rect, 'right'))
                    collide_left = check_left.count(True)
                    collide_right = check_right.count(True)
                    if collide_left > 0:
                        for block in current_shape:
                            for rect in current_shape[block]:
                                for i in range(collide_left):
                                    block.move(rect, 'right')
                    elif collide_right > 0:
                        for block in current_shape:
                            for rect in current_shape[block]:
                                for i in range(collide_right):
                                    block.move(rect, 'left')

        key = pygame.key.get_pressed()
        if key[K_DOWN]:
            for block in current_shape:
                for rect in current_shape[block]:
                    block.move(rect, 'down')

#       add y coords of blocks to y list
        y_list = []
        for i in range(0,len(block_rect_list)):
            board_rect = block_rect_list[i]
            y_list.append(board_rect.y)

#       count number of occurences of y values in y_list
        y_totals_dict = {val: y_list.count(val) for val in set(y_list)}

#       check if 10 y coords are the same
        for y_val, total in y_totals_dict.items():
            if total == 10:
                clear_line = True
                clear_line_pos = y_val
        
        if clear_line == True:
            clear_line = False
#           remove blocks on the full line from rect list
            for i in reversed(range(0,len(block_rect_list))):
                board_rect = block_rect_list[i]
                if board_rect.y == clear_line_pos:
                    block_rect_list.pop(i)
#           remove blocks on the full line from board dict
            for block, rect in board_dict.items():
                for i in reversed(range(0,len(rect))):
                    if rect[i].y == clear_line_pos:
                        rect.pop(i)
#          move blocks down after line is cleared
            for i in range(0,len(block_rect_list)):
                board_rect = block_rect_list[i]
                if board_rect.y < clear_line_pos:
                    board_rect.y += 25
#          move blocks down after line is cleared
            for block, rect in board_dict.items():
                for i in range(0,len(rect)):
                    if rect[i].y < clear_line_pos:
                        rect[i].y += 25


#       Check collision with bottom of the board
        if block.bottom_collision(current_shape[shape]) == True:
            collide_delay += 1
            for block in current_shape:
                for rect in current_shape[block]: 
                    if rect.y - 475 > 0:
                        y_dif = rect.y % 475                
                        block.block_adjust(current_shape[block], y_dif)
            if collide_delay > 30:
                collide_delay = 0
                new_shape = True
                for block, rect in current_shape.items():
                    block.velocity = 0
                    block_rect_list.extend(rect)
                    board_dict[block] = rect
                for block, rect in list(current_shape.items()):
                    current_shape.pop(block)
                    

#       Check collision with other blocks
        i = 0
        collide = False
        for block in current_shape:
            for rect in current_shape[block]:
                for i in range(0,len(block_rect_list)):
                    if rect.colliderect(block_rect_list[i]):
                        collide_delay += 1
                        if rect.y + 25 > block_rect_list[i].y:
                            y_dif = rect.y + 25 - block_rect_list[i].y
                        else:
                            y_dif = 0
                        block.block_adjust(current_shape[block], y_dif)
                        if collide_delay > 30:
                            collide_delay = 0
                            collide = True
                            new_shape = True
                            if block.top_collision(current_shape[shape]) == True:
                                WIN.blit(GAMEOVER_TEXT, (WIN_WIDTH / 2 - GAMEOVER_TEXT.get_width() / 2,
                                                        WIN_HEIGHT / 2 - GAMEOVER_TEXT.get_height() / 2))
                                pygame.display.update()
                                pygame.time.delay(3000)
                                restart = True
                            for block, rect in current_shape.items():
                                block.velocity = 0
                                block_rect_list.extend(rect)
                                board_dict[block] = rect
                            for block, rect in list(current_shape.items()):
                                current_shape.pop(block)
                    if collide == True:
                        break
                if collide == True:
                    break
            if collide == True:
                break


        if restart == True:
            restart = False
            break
        

        WIN.blit(BOARD_SURFACE, (50, 50))
        pygame.display.update()

    main()

if __name__ == '__main__':
    main()