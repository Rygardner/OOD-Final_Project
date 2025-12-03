"""player.py

Player class that the user interacts with to move around the level
"""

from __future__ import annotations
import pygame


class Player:
    """Player object that handles input, moves, applies gravity, handle collision for player
    object, and draw on pygame screen
    """
    
    __slots__ = (
        "__move_speed", 
        "__jump_speed", 
        "__fall_speed", 
        "__wall_jump_speed", 
        "__jump_velocity", 
        "__color", 
        "__size", 
        "__on_ground", 
        "__can_wall_jump", 
        "__touching_left_wall", 
        "__touching_right_wall",
        "rect"
    )

    def __init__(self, x: int = 0, y: int = 0, 
                 chosen_color: tuple[int] = (0, 128, 255),
                 rec_size: tuple[int] = (40, 40), 
                 movement_speed: int = 5,
                 jump_speed: float = 15.0, 
                 fall_speed: float = 0.7,
                 wall_bounce_speed: float = 13.0
                 ) -> None:
        """Initializes player's attributes. 

        Args:
            x (int): Player's x position
            y (int): Player's y position
            chosen_color (tuple[int, int, int]): Player's color
            rec_size (tuple[int]): Player's rect size
            movement_speed (int): Player's movement speed
            jump_speed (float): = Player's jump speed
            fall_speed (float): = Player's fall speed
            wall_bounce_speed (float): = Player's wall bounce speed


        """

        # Player's coords, size, and color
        self.rect: pygame.Rect = pygame.Rect(x, y, *rec_size)
        self.color = chosen_color

        # Player's speeds
        self.move_speed: int = movement_speed
        self.jump_speed: float = jump_speed
        self.fall_speed: float = fall_speed
        self.wall_jump_speed: float = wall_bounce_speed

        # Player's velocity (set to 0 initially) rect handles horizontal velocity
        self.jump_velocity: float = 0.0

        # Players flags
        self.on_ground: bool = False
        self.can_wall_jump: bool = True
        self.touching_left_wall: bool = False
        self.touching_right_wall: bool = False

# ********* Setters/Getters **************

    @property
    def x(self) -> int:
        return self.rect.x

    @x.setter
    def x(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("x must be an int")
        self.rect.x = value

    @property
    def y(self) -> int:
        return self.rect.y

    @y.setter
    def y(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("y must be an int")
        self.rect.y = value

    @property
    def size(self) -> tuple[int, int]:
        return self.rect.size
    
    @size.setter
    def size(self, value: tuple[int, int]) -> None:
        if (
            not isinstance(value, tuple)
            or len(value) != 2
            or not all(isinstance(v, int) and v > 0 for v in value)
        ):
            raise TypeError("size must be a tuple of two positive ints (width, height)")

        self.rect.size = value
    
    @property
    def color(self) -> tuple[int]:
        """Getter for player's color
        """
        return self.__color
    
    @color.setter
    def color(self, chosen_color: tuple[int] | str) -> None:
        """Setter for player's color. Supports either a tuple with 3 ints
        that represent RGB or a string with a generic colors: red, green, blue,
        white, black, or yellow.
        """
        color_dict = {
            "red":   (255, 0, 0),
            "green": (0, 255, 0),
            "blue":  (0, 0, 255),
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "yellow": (255, 255, 0),
        }

        if isinstance(chosen_color, str):
            if chosen_color.lower() not in self.color_dict:
                raise ValueError("chosen_color name is unknown")
            self.__color = color_dict[chosen_color.lower()]

        elif not isinstance(chosen_color, tuple) or len(chosen_color) != 3:
            raise TypeError("chosen_color must be a tuple with three ints that represent RGB")
        self.__color = chosen_color

    @property
    def move_speed(self) -> int:
        """Getter for player's move speed
        """
        return self.__move_speed
    
    @move_speed.setter
    def move_speed(self, speed: int) -> None:
        """Setter for player's move speed
        """
        if not isinstance(speed, int):
            raise TypeError("Player's move_speed must be an int")
        
        self.__move_speed = speed
        
    @property
    def jump_speed(self) -> float:
        """Getter for player's jump speed
        """
        return self.__jump_speed
    
    @jump_speed.setter
    def jump_speed(self, speed: float) -> None:
        """Setter for player's jump speed
        """
        if not isinstance(speed, float):
            raise TypeError("Player's jump_speeed must be a float")
        self.__jump_speed = speed
        
    @property
    def fall_speed(self) -> float:
        """Getter for player's fall speed
        """
        return self.__fall_speed
    
    @fall_speed.setter
    def fall_speed(self, gravity: float) -> None:
        """Setter for player's fall speed
        """
        if not isinstance(gravity, float):
            raise TypeError("Player's fall_speed must be a float")
        
        self.__fall_speed = gravity

    @property
    def wall_jump_speed(self) -> float:
        """Getter for player's wall jump speed
        """
        return self.__wall_jump_speed
    
    @wall_jump_speed.setter
    def wall_jump_speed(self, speed: float) -> None:
        """Setter for player's wall jump speed
        """
        if not isinstance(speed, float):
            raise TypeError("Player's wall_jump_speed must be a float")
        
        self.__wall_jump_speed = speed

    @property 
    def jump_velocity(self) -> float:
        """Getter for player's jump velocity
        """
        return self.__jump_velocity
    
    @jump_velocity.setter
    def jump_velocity(self, velocity: float) -> None:
        """Setter for player's jump velocity
        """
        if not isinstance(velocity, float):
            raise TypeError("Player's jump_velocity must be a float")
        
        self.__jump_velocity = velocity

    @property
    def on_ground(self) -> bool:
        """Getter for on ground flag
        """
        return self.__on_ground
    
    @on_ground.setter
    def on_ground(self, is_on_ground: bool) -> None:
        """Setter for on ground flag
        """
        if not isinstance(is_on_ground, bool):
            raise TypeError("Player's is on ground flag must be a bool")
        self.__on_ground = is_on_ground
        
    @property
    def can_wall_jump(self) -> bool:
        """Getter for player's can wall jump flag
        """
        return self.__can_wall_jump
    
    @can_wall_jump.setter
    def can_wall_jump(self, flag: bool) -> None:
        """Setter for player's can wall jump flag
        """
        if not isinstance(flag, bool):
            raise TypeError("Player's can wall jump flag must be a bool")
        self.__can_wall_jump = flag
        
    @property
    def touching_left_wall(self) -> bool:
        """Getter for player's touching left wall flag
        """
        return self.__touching_left_wall
    
    @touching_left_wall.setter
    def touching_left_wall(self, flag: bool) -> None:
        """Setter for player's touching left wall flag
        """
        if not isinstance(flag, bool):
            raise TypeError("Player's touching_left_wall flag must be a bool")
        self.__touching_left_wall = flag
        
    @property
    def touching_right_wall(self) -> bool:
        """Getter for player's touching right wall flag
        """
        return self.__touching_right_wall
    
    @touching_right_wall.setter
    def touching_right_wall(self, flag: bool) -> None:
        """Setter for player's touching right wall flag
        """
        if not isinstance(flag, bool):
            raise TypeError("Player's touching_right_wall flag must be a bool")
        self.__touching_right_wall = flag

#************** Movement / Physics ******************

    def horizontal_movement(self, keys: pygame.key.ScancodeWrapper) -> int:
        """Handles Horizontal movement input
        """
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            return -self.move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            return self.move_speed
        
        return 0
        
    def handle_horizontal_collisions(self, colliders: list[pygame.Rect], horizontal_velocity: int,) -> None:
        """Handles horzontal collisions
        """
        self.touching_left_wall = False
        self.touching_right_wall = False
        
        for collider in colliders:
            if self.rect.colliderect(collider):
                if horizontal_velocity > 0:
                    self.rect.right = collider.left
                    self.touching_right_wall = True
                elif horizontal_velocity < 0:
                    self.rect.left = collider.right
                    self.touching_left_wall = True
        
    def jump(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Handles jump logic
        """
        if keys[pygame.K_SPACE]:
            if self.on_ground:
                self.jump_velocity = -self.jump_speed
                self.on_ground = False
                self.can_wall_jump = True
            elif self.can_wall_jump and (self.touching_left_wall or self.touching_right_wall):
                self.jump_velocity = -self.wall_jump_speed
                self.can_wall_jump = False

    def apply_gravity(self) -> None:
        """Applies gravity to player
        """
        self.jump_velocity += self.fall_speed
        self.y += int(self.jump_velocity)

    def handle_vertical_collision(self, colliders: list[pygame.Rect]) -> None:
        """Handles vertical collision. So capable of landing on a floor/platform. Also
        handles collision for when the player jumps and collides with a platform from
        underneath.
        """
        self.on_ground = False

        for collider in colliders:
            if self.rect.colliderect(collider):
                if self.jump_velocity > 0:
                    self.rect.bottom = collider.top
                    self.jump_velocity = 0.0
                    self.on_ground = True
                    self.can_wall_jump = True
                elif self.jump_velocity < 0:
                    self.rect.top = collider.bottom
                    self.jump_velocity = 0.0

    def reposition(self, x: int, y: int) -> None:
        """Move the player to a new (x, y) area. Could use for spawning/respawning
        or teleport the player to set location. Resets jump_velocity and flags
        """
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("spawn coordinates must be ints")

        self.rect.x = x
        self.rect.y = y

        self.jump_velocity = 0.0
        self.on_ground = False
        self.touching_left_wall = False
        self.touching_right_wall = False
        self.can_wall_jump = True

    def update(self, keys: pygame.key.ScancodeWrapper, colliders: list[pygame.Rect]) -> None:
        """Updates player's loop in game 
        """
        horizontal_velocity = self.horizontal_movement(keys)
        self.x += horizontal_velocity

        self.handle_horizontal_collisions(colliders, horizontal_velocity)

        self.jump(keys)

        self.apply_gravity()

        self.handle_vertical_collision(colliders)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw player onto pygame screen/surface
        """
        pygame.draw.rect(surface, self.color, self.rect)


if __name__ == "__main__":
    pass