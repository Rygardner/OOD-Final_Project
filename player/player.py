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
        self.y_vel: float = 0.0
        self.on_ground: bool = False
        self.can_wall_jump: bool = True

        # Track which side we are touching
        self.touching_left: bool = False
        self.touching_right: bool = False

    def handle_input(self, keys: pygame.key.ScancodeWrapper, walls: list[pygame.Rect]) -> None:
        """Handles input for moving left/right, jumping and wall bounce. """
        dx: int = 0

        # Check to move left or right based on key input
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.MOVE_SPEED

        # Move Left/Right
        self.rect.x += dx

        # Reset left/right wall flags
        self.touching_left = False
        self.touching_right = False

        # Wall Colision, checks if moving right or left when touching wall
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                    self.touching_right = True
                if dx < 0:
                    self.rect.left = wall.right
                    self.touching_left = True

        # Jumping and wall jump if on wall
        if keys[pygame.K_SPACE]:
            if self.on_ground:
                self.y_vel = -self.JUMP_SPEED
                self.on_ground = False
                self.can_wall_jump = True
            elif self.can_wall_jump and (self.touching_left or self.touching_right):
                self.y_vel = -self.JUMP_SPEED
                #********* Need to figure out how to smoothly apply this ************
                # if self.touching_left:
                #     self.rect.x += self.WALL_BOUNCE_VELOCITY
                # if self.touching_right:
                #     self.rect.x -= self.WALL_BOUNCE_VELOCITY
                self.can_wall_jump = False

    def apply_gravity(self, floor_y: int, walls: list[pygame.Rect]) -> None:
        """Applies gravity to player"""
        self.y_vel += self.GRAVITY
        self.rect.y += int(self.y_vel)

        self.on_ground = False

        # Floor colision
        if self.rect.bottom >= floor_y:
            self.rect.bottom = floor_y
            self.y_vel = 0
            self.on_ground = True
            self.can_wall_jump = True

        # Wall colision
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.y_vel > 0:  # falling
                    self.rect.bottom = wall.top
                    self.y_vel = 0
                    self.on_ground = True
                    self.can_wall_jump = True
                elif self.y_vel < 0:  # jumping up
                    self.rect.top = wall.bottom
                    self.y_vel = 0

    def update(self, keys: pygame.key.ScancodeWrapper, floor_y: int, walls: list[pygame.Rect]) -> None:
        """Wrapper function that calls both handle input and apply gravity to update player on pygame screen
        """
        self.handle_input(keys, walls)
        self.apply_gravity(floor_y, walls)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw player onto pygame screen (or surface to be technical)
        """
        pygame.draw.rect(surface, self.PLAYER_COLOR, self.rect)


if __name__ == "__main__":
    pass