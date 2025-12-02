"""movement_strategy.py

Class that uses strategy design pattern to handle player movement. At the moment
it handles normal movement and no movement, but later on we could add different
kinds of movement strategies such as faster movement, slower movement, slippery
movement, etc... 
"""

from __future__ import annotations

from abc import ABC, abstractclassmethod
import pygame

class MovementStrategy(ABC):
    """Abstract class that acts as a base for movement strategies
    """

    @abstractclassmethod
    def get_horizontal_velocity(self, move_speed: int, keys: pygame.key.ScancodeWrapper) -> int:
        """Returns horizontal velocity
        """


class NormalMovement(MovementStrategy):
    """Movement strategy that does normal movement for the player
    """

    def get_horizontal_velocity(self, move_speed: int, keys: pygame.key.ScancodeWrapper) -> int:
        """Returns horizontal velocity based on keyboard input
        
        Args
            move_speed (int): Player's movement speed
            keys (pygame.key.ScancodeWrapper): Input keys from keyboard    
        """
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            return -move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            return move_speed
        return 0
    
class NoMovement(MovementStrategy):
    """Movement strategy that ignores input from keyboard so player doesn't move
    """

    def get_horizontal_velocity(self, move_speed: int, keys: pygame.key.ScancodeWrapper) -> int:
        """Returns horizontal velocity, which in this case is 0 since this is no movement strategy
        """
        return 0
    
