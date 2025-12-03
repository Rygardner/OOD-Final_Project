"""
    This module holds the game manager that works with pygame and the player class
    as well as the coordinator for all level aspects
"""
import sys
import pygame
from pygame.locals import *
from player.player import Player
from Levels import Level_Objects
from button import button

WHITE   = (255 , 255 , 255)
BLACK   = (0   , 0   , 0)
GRAY    = (112 , 112 , 112)

RED     = (255 , 0   , 0)
BLUE    = (0   , 0   , 255)
GREEN   = (0   , 255 , 0)


class game:
    """
        This class is the manager for all game play asspects
    """
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if game._initialized:
            return  # <-- PREVENTS double init safely
        game._initialized = True

        self.player = Player(200, 200)
        self.objects: list[pygame.Rect]

        self.level = 0
        self.start_pos = [0 , 0]
        self.goal_pos = [0 , 0]
        self.goal = pygame.Rect(self.goal_pos[0], self.goal_pos[1], 80, 80)

        self.floor = pygame.Rect(-800, 900, 2400, 80)  # floor object to prevent forever falling

        self.pygame_init()
    
    def pygame_init(self) -> None:
        """
            This function initializes the pygame window
        """
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        WIDTH, HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2D platformer")
        self.clock = pygame.time.Clock()

        self.screen.fill((50,50,50))
        pygame.display.flip()
        pygame.time.delay(200)

    def quit(self):
        """
            handles everyting needed to exit the program
        """
        pygame.quit()
        sys.exit()

    def level_setup(self , new_level_objects , new_start_pos , new_goal_pos) -> None:
        """
            Sets up the level for play
        """    
        self.objects = new_level_objects

        self.start_pos = new_start_pos
        self.player.x = self.start_pos[0]
        self.player.y = self.start_pos[1]

        self.goal_pos  = new_goal_pos
        self.goal.x = self.goal_pos[0]
        self.goal.y = self.goal_pos[1]

    def level_changer(self , new_level) -> bool:
        """
            This function is called when a new level is selected
            returns a True if level is selected, False if not
        """
        match new_level:
            case 1:
                new_level_objects = Level_Objects.level_1_objects
                new_start_pos = Level_Objects.level_1_start_pos
                new_goal_pos = Level_Objects.level_1_goal_pos
                self.level_setup(new_level_objects , new_start_pos , new_goal_pos)
            
            case 2:
                new_level_objects = Level_Objects.level_2_objects
                new_start_pos = Level_Objects.level_2_start_pos
                new_goal_pos = Level_Objects.level_2_goal_pos
                self.level_setup(new_level_objects , new_start_pos , new_goal_pos)

            case 3:
                new_level_objects = Level_Objects.level_3_objects
                new_start_pos = Level_Objects.level_3_start_pos
                new_goal_pos = Level_Objects.level_3_goal_pos
                self.level_setup(new_level_objects , new_start_pos , new_goal_pos)
                
            case 4:
                new_level_objects = Level_Objects.level_4_objects
                new_start_pos = Level_Objects.level_4_start_pos
                new_goal_pos = Level_Objects.level_4_goal_pos
                self.level_setup(new_level_objects , new_start_pos , new_goal_pos)
                
            case 5:
                new_level_objects = Level_Objects.level_5_objects
                new_start_pos = Level_Objects.level_5_start_pos
                new_goal_pos = Level_Objects.level_5_goal_pos
                self.level_setup(new_level_objects , new_start_pos , new_goal_pos)
                
            case 6:
                new_level_objects = Level_Objects.level_6_objects
                new_start_pos = Level_Objects.level_6_start_pos
                new_goal_pos = Level_Objects.level_6_goal_pos
                self.level_setup(new_level_objects , new_start_pos , new_goal_pos)


            case _:  # should only happen if exiting to main menu
                return False
        self.level = new_level
        self.player.jump_velocity = 0.0  # fixes error if player leaves map
        return True

    def level_select(self) -> bool:  
        """
            creates a Level selection menu
            returns true if level is selected
            returns false for exit to main menu
        """
        first_loop = True
        self.level = 0
        buttons = Level_Objects.level_select_buttons
        mouse_up_at_start = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                # makes sure the mouse is released before starting level slect
                if event.type == pygame.MOUSEBUTTONUP: 
                    if event.type == 1026:
                        mouse_up_at_start = True

            self.screen.fill(WHITE)

            if not first_loop and mouse_up_at_start:
                for index , button_object in enumerate(buttons):
                    button_object.draw_button(self.screen)
                    if button_object.button_clicked() :
                        if index == 6: # exit to main menu 
                            return False
                        return self.level_changer(index+1)
            else:
                first_loop = False
            pygame.display.flip()
            self.clock.tick(60)

    def post_game_menu(self , win) -> int:
        """
            displayed after game 
            one display for faild and 1 for win
            returns 0 = next level, 1 = level select, 2 = main menu, 3 = retry
        """
        option_1 = pygame.Rect(81,  241, 160, 160)  # option 1
        option_2 = pygame.Rect(321, 241, 160, 160)  # option 2
        option_3 = pygame.Rect(561, 241, 160, 160)  # option 3

        if win:  # creates button for next level
            button_1 = button(option_1, "Next Level", BLACK , GRAY , 36)
        else:  #creates button for retry level
            button_1 = button(option_1, "Retry Level", BLACK , GRAY , 36)

        button_2 = button(option_2, "Select Level", BLACK , GRAY , 36)
        button_3 = button(option_3, "Main Menu", BLACK , GRAY , 36)
        text_options = [button_1 , button_2 , button_3]
        first_loop = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
            self.screen.fill(WHITE)
            if not first_loop: 
                for index , buttons in enumerate(text_options):
                    buttons.draw_button(self.screen)
                    if buttons.button_clicked():
                        if not win and index == 0:
                            return 3 # retuns 3 for retry level
                        return index
            pygame.display.flip()
            self.clock.tick(60)
            first_loop = False

    def draw_platforms(self) -> None:
        """
            This function draws all objects of the current level
        """
        for platforms in self.objects :
            pygame.draw.rect(self.screen, BLACK, platforms)
        pygame.draw.rect(self.screen, (255, 246, 0), self.goal)

    def Game_play(self) -> int:
        """ 
            this function is the main game play loop 
            returns 0 = next level, 1 = level select, 2 = main menu, 3 = retry
        """
        win = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            if self.player.rect.colliderect(self.goal): # detects a win
                running = False
                win = True
            if self.player.rect.colliderect(self.floor):
                running = False
                win = False

            # get player input
            keys = pygame.key.get_pressed()
            self.player.update(keys, self.objects)

            self.screen.fill(WHITE)

            # draw rects
            self.draw_platforms()

            # draw player
            self.player.draw(self.screen)

            # update screen
            pygame.display.flip()
            self.clock.tick(60)
        return self.post_game_menu(win)
        
    def main_menu(self) -> int:
        """
            This Function is the first screen the player sees
            it has options for level select and quit

            it returns an int value according to the option selected
            0 = quit , 1 = level selct 
        """
        ls_rect   = pygame.Rect(161, 161, 480, 160)  # level select
        exit_rect = pygame.Rect(161, 401, 480, 160)  # exit

        button_ls   = button(ls_rect  , "Level Select", BLACK , GRAY , 36)
        button_exit = button(exit_rect, "Exit"        , BLACK , RED  , 36)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            self.screen.fill(WHITE)
    
            button_ls.draw_button(self.screen)
            button_exit.draw_button(self.screen)

            if button_ls.button_clicked():
                return 1
            elif button_exit.button_clicked():
                return 0

            pygame.display.flip()
            self.clock.tick(60)   

    def manager(self) -> None:
        """
            This function is the compleat manager for all other functions in this class
        """
        option = self.main_menu()
        while True: # loops untill player decieds to exit
            # exit
            if option == 0:  
                self.quit()

            # level select
            elif option == 1 or option == 3: 
                if self.level_select():
                    option = self.Game_play() + 2 
                    # 2 = next level, 3 = level select, 4 = main menu, 5 = retry
                else :
                    option = self.main_menu()
            
            # next level
            elif option == 2:
                self.level_changer(self.level+1)
                option = self.Game_play() + 2

            # main menu
            elif option == 4:
                option = self.main_menu()
            
            # retry
            elif option == 5:
                self.level_changer(self.level)
                option = self.Game_play() + 2

def main() -> None:
    try:
        game_manager = game()
        game_manager.manager()
    except Exception as e:
        print("CRASH:", e)
    

if __name__ == "__main__":
    main()