"""player_test.py

A small pygame window to test player object. Has a floor y position so player 
doesn't go lower than the floor position set. Has a left wall and right wall to 
test player wall bounce if it works. Player update takes in keys (keys pressed),
floor_y, and walls. 
"""

import pygame
from player import Player


# Test player
def main() -> None:
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    floor_y: int = HEIGHT - 50

    left_wall = pygame.Rect(100, 0, 20, floor_y)
    right_wall = pygame.Rect(WIDTH - 120, 0, 20, floor_y)
    walls: list[pygame.Rect] = [left_wall, right_wall]

    player = Player(200, 200)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.update(keys, floor_y, walls)

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 200, 0), (0, floor_y, WIDTH, HEIGHT - floor_y))
        for wall in walls:
            pygame.draw.rect(screen, (200, 0, 0), wall)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
