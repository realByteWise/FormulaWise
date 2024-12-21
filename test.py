import pygame
import sys


pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mouse Position Tracker")
font = pygame.font.Font(None, 36)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.fill((0, 0, 0)) 
    text = font.render(f"Mouse Position: X: {mouse_x}, Y: {mouse_y}", True, (255, 255, 255))
    screen.blit(text, (10, 10)) 
    pygame.display.flip()
pygame.quit()
