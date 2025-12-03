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

# *********** Level 1 *************
level_1_objects = [  
    pygame.Rect(0 , 620 , 800 , 180)  # floor at pxl hight 620
]
level_1_start_pos = [200 , 621]
level_1_goal_pos = [600 , 540]

# *********** Level 2 *************
level_2_objects = [  
    pygame.Rect(0   , 620 , 800 , 180),     # floor at pxl hight 620
    pygame.Rect(240 , 520 , 560 , 100),     # first jump
    pygame.Rect(400 , 420 , 400 , 100)      # last jump
]
level_2_start_pos = [200 , 621]
level_2_goal_pos = [600 , 340]

# *********** Level 3 *************
level_3_objects = [  
    pygame.Rect(0   , 620 , 300 , 180),   # floor at pxl hight 620 untill mid point
    pygame.Rect(400 , 620 , 450 , 180)     # floor at pxl hight 620 after mid ponit
]
level_3_start_pos = [200 , 621]
level_3_goal_pos = [600 , 540]

# *********** Level 4 *************
level_4_objects = [  
    pygame.Rect(0   , 620 , 300 , 180),    # floor at pxl hight 620 untill mid point
    pygame.Rect(400 , 400 , 450 , 480),    # elevated floor at px hight after mid point
    pygame.Rect(150 , 470 , 150 , 50),     # floating wall jump point
]
level_4_start_pos = [200 , 621]
level_4_goal_pos = [600 , 320]

# *********** Level 5 *************
level_5_objects = [  
    pygame.Rect(50  , 400 , 200 , 25 ),  # platform 1
    pygame.Rect(350 , 350 , 300 , 25 ),  # platform 2
    pygame.Rect(200 , 200 , 200 , 25 ),  # platform 3
    pygame.Rect(0   , 120 , 160 , 25 ),  # platform 4
]
level_5_start_pos = [80 , 300]
level_5_goal_pos = [0 , 0]

# *********** Level 6 *************
level_6_objects = [ # hole at 340-440
    pygame.Rect(0   , 720 , 240 , 80 ),  # floor pxl hight 720
    pygame.Rect(240 , 620 , 100 , 180),  # elevated floor pre  jump
    pygame.Rect(440 , 620 , 360 , 180),  # elevated floor post jump
    pygame.Rect(700 , 240 , 100 , 560),  # right wall
    pygame.Rect(440 , 420 , 200 , 25 ),  # platform 1 pre  jump
    pygame.Rect(140 , 420 , 200 , 25 ),  # platform 1 post jump
    pygame.Rect(115 , 0   , 25  , 380),  # left wall
    pygame.Rect(240 , 240 , 100 , 25 ),  # platform 2 pre  jump
    pygame.Rect(440 , 240 , 360 , 25 )   # platform 2 post jump
]
level_6_start_pos = [80  , 620]
level_6_goal_pos  = [600 , 160]

# FIX ME :: contains all the objects in all levels


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

