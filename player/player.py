"""player.py
"""

from __future__ import annotations
import pygame


class Player:
    """Player object that handles input, moves, applies gravity, handle collision for player
    object, and draw on pygame screen
    """
    Player_SIZE: tuple[int, int] = (40, 40)
    PLAYER_COLOR: tuple[int, int, int] = (0, 128, 255)  # RGB colors
    MOVE_SPEED: int = 5
    JUMP_SPEED: int = 15
    GRAVITY: float = 0.7
    WALL_BOUNCE_VELOCITY: int = 20

    def __init__(self, x: int, y: int) -> None:
        """Initializes player position, size, y velocity, on ground flag,
        wall jump flag, and touching left/right wall flags.
        """
        self.rect: pygame.Rect = pygame.Rect(x, y, *self.Player_SIZE)
        self.jump_velocity: float = 0.0
        self.on_ground: bool = False
        self.can_wall_jump: bool = True

        # Track which side of player is touching the wall
        self.touching_left_wall: bool = False
        self.touching_right_wall: bool = False

    def handle_input(self, keys: pygame.key.ScancodeWrapper, walls: list[pygame.Rect]) -> None:
        """Handles input for moving left/right, jumping and wall bounce. """
        horizontal_velocity: int = 0

        # Check to move left or right based on key input
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            horizontal_velocity -= self.MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            horizontal_velocity += self.MOVE_SPEED

        # Move Left/Right
        self.rect.x += horizontal_velocity

        # Reset left/right wall flags
        self.touching_left_wall = False
        self.touching_right_wall = False

        # Wall Colision, checks if moving right or left when touching wall
        for wall in walls:
            if self.rect.colliderect(wall):
                if horizontal_velocity > 0:
                    self.rect.right = wall.left
                    self.touching_right_wall = True
                if horizontal_velocity < 0:
                    self.rect.left = wall.right
                    self.touching_left_wall = True

        # Jumping and wall jump if on wall
        if keys[pygame.K_SPACE]:
            if self.on_ground:
                self.jump_velocity = -self.JUMP_SPEED
                self.on_ground = False
                self.can_wall_jump = True
            elif self.can_wall_jump and (self.touching_left_wall or self.touching_right_wall):
                self.jump_velocity = -self.JUMP_SPEED
                #********* Need to figure out how to smoothly apply this ************
                # if self.touching_left_wall:
                #     self.rect.x += self.WALL_BOUNCE_VELOCITY
                # if self.touching_right_wall:
                #     self.rect.x -= self.WALL_BOUNCE_VELOCITY
                self.can_wall_jump = False

    # Will probably need to rework this to fit actual floors
    def apply_gravity(self, floor: int) -> None:
        """Applies gravity to player"""
        self.jump_velocity += self.GRAVITY
        self.rect.y += int(self.jump_velocity)

        self.on_ground = False

        # Floor colision
        if self.rect.bottom >= floor:
            self.rect.bottom = floor
            self.jump_velocity = 0
            self.on_ground = True
            self.can_wall_jump = True

    def update(self, keys: pygame.key.ScancodeWrapper, floor: int, walls: list[pygame.Rect]) -> None:
        """Wrapper function that calls both handle input and apply gravity to update player on pygame surface
        """
        self.handle_input(keys, walls)
        self.apply_gravity(floor)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw player onto pygame screen/surface
        """
        pygame.draw.rect(surface, self.PLAYER_COLOR, self.rect)


if __name__ == "__main__":
    pass