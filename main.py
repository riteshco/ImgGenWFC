import pygame
import sys

pygame.init()

screen_width, screen_height = 800, 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('My Pygame Window')

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
    
    screen.fill((0, 0, 0))    
    
    # Update the display to show the changes
    pygame.display.flip()


pygame.quit()
sys.exit()