"""player_test.py

A small pygame window to test player object. Has a floor y position so player
doesn't go lower than the floor position set. Has a left wall and right wall to
test player wall bounce if it works. Player update takes in keys (keys pressed),
floor, and walls.
"""

import pygame
from player import Player


def main() -> None:
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Player test")
    clock = pygame.time.Clock()

    # Create floor, left/right wall, and a platform
    floor_rect = pygame.Rect(0, 550, 800, 600 - 550)
    left_wall = pygame.Rect(100, 0, 20, 550)
    right_wall = pygame.Rect(680, 0, 20, 550)
    platform = pygame.Rect(300, 400, 200, 20)

    # Create a list of solids with above rects
    solids: list[pygame.Rect] = [floor_rect, left_wall, right_wall, platform]

    player = Player(200, 200)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # get player input
        keys = pygame.key.get_pressed()
        player.update(keys, solids)

        screen.fill((0, 0, 0))

        # draw rects
        pygame.draw.rect(screen, (0, 200, 0), floor_rect)
        pygame.draw.rect(screen, (200, 0, 0), left_wall)
        pygame.draw.rect(screen, (200, 0, 0), right_wall)
        pygame.draw.rect(screen, (0, 0, 200), platform)

        # draw player
        player.draw(screen)

        # update screen
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
