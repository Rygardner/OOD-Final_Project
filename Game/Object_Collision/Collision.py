"""
    contains the Object_Collision class
    this is ment to handel interactions between the player and the level
"""
import pygame
from player import Player

class Object_Collision:
    """ 
        This class handels all of the Object collisions 
        between the player and 
            walls
            ground
            ceiling
            possibly
                coins , stars , or keys
    """

    def __init__(self , player_class):
        self.player_object = player_class
    
    def collision_detected(self) -> None:
        """
            This function communicates with the player class when collison occures
        """
        pass
    
    def collision_detector(self) -> bool:
        """
            This function returns true if a collision occures
        """
        pass
    
# these 3 classes are to identify when a platform collision happens
# imagin this       |
#               -- [ ] --
#                   |
class touch_ground(Object_Collision):
    """ 
        checks if the player object touches the ground
        this should start to be called when the player is not on the ground
    """
    # somthing like get player X then look down the Y to find the next ground point
    def __init__(self , player_class : Player ,floors : tuple):
        super().__init__(self)
        self.floors = floors

    def collision_detector(self)
        """
            This function returns true if the player is touching a floor object
        """
        if self.player_object.collidelist(floors):
            self.player_object.on_ground(True)


class touch_wall_left(Object_Collision):
    """
        checks if the player object is touching a wall 
        this should run always
    """
    # should be somthing like checks were the closest wall 
    #   is to the left when Y level changes
    def __init__(self , player_class : Player , left_walls : tuple):
        super().__init__(self)
        self.left_walls = left_walls

    def collision_detector(self)
        """
            This function returns true if the player is touching a left_wall object
        """
        if self.player_object.collidelist(left_walls):
            self.player_object.touching_left_wall(True)
            self.player_object.can_wall_jump(True)

class touch_wall_right(Object_Collision):
    """
        checks if the player object is touching a wall 
        this should run always
    """
    # should be somthing like checks were the closest wall 
    #   is to the left when Y level changes
    def __init__(self , player_class : Player , right_walls : tuple):
        super().__init__(self)
        self.right_walls = right_walls

    def collision_detector(self)
        """
            This function returns true if the player is touching a left_wall object
        """
        if self.player_object.collidelist(right_walls):
            self.player_object.touching_right_wall(True)
            self.player_object.can_wall_jump(True)


    
class touch_ceiling(Object_Collision):
    """ 
        checks if the player object is touching a ceiling
        this should run when the player begins to move up
    """
    # somthing like get player X then look up the Y to find the next ceiling point 

# non platform collision 
class touch_collectable(Object_Collision):
    """
        checks if the player object is touching a collectable object
        should only run on levels where there is a collectable
    """
    # somthing like if player pos is ~= collecable pos


class touch_spike(Object_Collision):
    """
        checks if the player touches a spike
            this kills the player
        should run on levels with spikes
    """
    # somthing like if player touch ground && gound==spike
    # also should work if player touches the side 


class touch_goal(Object_Collision):
    """
        checks if the player touches the boarders of the screen
            this is a win condition
        should run on all levels
    """
    # somthing like if player pos >= screen -> win
    # or if player pos ~= goal pos -> win