"""
    This holds the pygame.rect objects to be used during levels
"""
import sys
import pygame

sys.path.append('/Game')
from button import button

WHITE   = (255 , 255 , 255)
BLACK   = (0   , 0   , 0)
GRAY    = (112 , 112 , 112)

RED     = (255 , 0   , 0)
BLUE    = (0   , 0   , 255)
GREEN   = (0   , 255 , 0)


# pygame.Rect(left, top, width, height)
level_1_objects = [  # FIX ME :: contains all the objects in level one
    pygame.Rect(0, 10, 800, 15)  # creates a floor at pxl hight 10
]
level_1_start_pos = [400 , 400]
level_1_goal_pos = [200 , 200]

level_select_rects = [  # contains the rects of the level slect buttons
    pygame.Rect(81, 161, 160, 160),  # level 1
    pygame.Rect(321, 161, 160, 160),  # level 2
    pygame.Rect(561, 161, 160, 160),  # level 3
    
    pygame.Rect(81, 401, 160, 160),  # level 4
    pygame.Rect(321, 401, 160, 160),  # level 5
    pygame.Rect(561, 401, 160, 160),  # level 6

    pygame.Rect(681, 42 , 80, 80)  # exit button    
]

level_select_buttons = [
    button(level_select_rects[0] , "1" , BLACK , GRAY , 36), 
    button(level_select_rects[1] , "2" , BLACK , GRAY , 36),
    button(level_select_rects[2] , "3" , BLACK , GRAY , 36),
    
    button(level_select_rects[3] , "4" , BLACK , GRAY , 36),
    button(level_select_rects[4] , "5" , BLACK , GRAY , 36),
    button(level_select_rects[5] , "6" , BLACK , GRAY , 36),
    
    button(level_select_rects[6] , "X" , BLACK , RED , 36)
]

