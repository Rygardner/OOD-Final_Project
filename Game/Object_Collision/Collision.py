"""
    contains the Object_Collision class
    this is ment to handel interactions between the player and the level
"""


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
    
    # these 3 functs are to identify when a platform collision happens
    # imagin this       |
    #               -- [ ] --
    #                   |
    def touch_ground() -> bool:
        """ 
            checks if the player object touches the ground
            this should start to be called when the player is not on the ground
        """
        # somthing like get player X then look down the Y to find the next ground point

    def touch_wall() -> bool:
        """
            checks if the player object is touching a wall 
            this should run always
        """
        # should be somthing like checks were the closest wall 
        #   is to the left and right when Y level changes
    
    def touch_ceiling() -> bool:
        """ 
            checks if the player object is touching a ceiling
            this should run when the player begins to move up
        """
        # somthing like get player X then look up the Y to find the next ceiling point 
    
    # non platform collision 
    def touch_collectable() -> bool:
        """
            checks if the player object is touching a collectable object
            should only run on levels where there is a collectable
        """
        # somthing like if player pos is ~= collecable pos

    def touch_spike() -> bool:
        """
            checks if the player touches a spike
                this kills the player
            should run on levels with spikes
        """
        # somthing like if player touch ground && gound==spike
        # also should work if player touches the side 

    def touch_goal() -> bool:
        """
            checks if the player touches the boarders of the screen
                this is a win condition
            should run on all levels
        """
        # somthing like if player pos >= screen -> win
        # or if player pos ~= goal pos -> win