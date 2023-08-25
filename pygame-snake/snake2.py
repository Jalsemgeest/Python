# Added movement
import pygame, random, sys

# Initialize Pygame
pygame.init()

# # Screen dimensions
screen_width = 640
screen_height = 480

# Colors
WHITE, BLACK, GREEN, RED = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0)

# # Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jake the Snake")

# Snake properties
snake_block = 20
snake_speed = 15

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

def gameLoop():
    game_over = False
    game_close = False

    # Snake initial position
    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    while not game_over:
        if game_close:
            screen.fill(BLACK)
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)

        pygame.draw.rect(screen, WHITE, [x1, y1, snake_block, snake_block])
        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
