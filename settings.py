import sys
import pygame
from resources import *


music_on, current_theme_index, volume = load_preferences()

def play_current_track():
    pygame.mixer.music.load(themes[current_theme_index][0])
    pygame.mixer.music.play(-1)

def draw_text(screen, text, size, color, x, y, center=False):
    font = pygame.font.Font(pygame.font.match_font('Palatino'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y)) if center else text_surface.get_rect(topleft=(x, y))
    screen.blit(text_surface, text_rect)

def show_settings(screen, current_bg_image_path):
    global music_on, current_theme_index, volume
    bg_image = pygame.image.load(themes[current_theme_index][1]).convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    pygame.mixer.music.set_volume(volume)
    slider_rect = pygame.Rect(550, 300, 200, 10) 
    slider_handle_rect = pygame.Rect(slider_rect.x + volume * slider_rect.width - 10, slider_rect.y - 10, 20, 30)  
    dragging = False 
    return_button_rect = pygame.Rect(550, 475, 200, 50)  
    change_music_button_rect = pygame.Rect(550, 375, 200, 50) 
    button_color = (255, 0, 0)  

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if slider_handle_rect.collidepoint(event.pos):
                        dragging = True
                    music_button_rect = pygame.Rect(550, 200, 200, 50)
                    if music_button_rect.collidepoint(event.pos):
                        music_on = not music_on
                        if music_on:
                            pygame.mixer.music.unpause()  
                        else:
                            pygame.mixer.music.pause()
                            
                    if change_music_button_rect.collidepoint(event.pos):
                        current_theme_index = (current_theme_index + 1) % len(themes)
                        play_current_track()  
                        bg_image = pygame.image.load(themes[current_theme_index][1]).convert()
                        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))  
                        current_bg_image_path = themes[current_theme_index][1]
                    if return_button_rect.collidepoint(event.pos):
                        running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    dragging = False

            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x = event.pos[0]
                    if slider_rect.x <= mouse_x <= slider_rect.x + slider_rect.width:
                        slider_handle_rect.x = mouse_x - 10
                    elif mouse_x < slider_rect.x:
                        slider_handle_rect.x = slider_rect.x
                    elif mouse_x > slider_rect.x + slider_rect.width:
                        slider_handle_rect.x = slider_rect.x + slider_rect.width - 20


                    volume = (slider_handle_rect.x - slider_rect.x) / (slider_rect.width - 20)
                    volume = max(0.0, min(volume, 1.0))
                    pygame.mixer.music.set_volume(volume)
        screen.blit(bg_image, (0, 0))
        music_button_color = (255, 0, 0) if music_on else (0, 0, 255)
        music_button_rect = pygame.Rect(550, 200, 200, 50)
        pygame.draw.rect(screen, music_button_color, music_button_rect)
        draw_text(screen, "Music: ON" if music_on else "Music: OFF", 24, (255, 255, 255), music_button_rect.centerx, music_button_rect.centery, center=True)
        pygame.draw.rect(screen, (200, 200, 200), slider_rect)  
        pygame.draw.rect(screen, (255, 0, 0), slider_handle_rect)  
        draw_text(screen, f"Volume: {int(volume * 100)}%", 24, (255, 255, 255),slider_rect.centerx, slider_rect.y - 30, center=True)
        pygame.draw.rect(screen, button_color, change_music_button_rect)
        draw_text(screen, "Change Theme", 24, (255, 255, 255), change_music_button_rect.centerx, change_music_button_rect.centery, center=True)
        pygame.draw.rect(screen, button_color, return_button_rect)
        draw_text(screen, "Return", 24, (255, 255, 255), return_button_rect.centerx, return_button_rect.centery, center=True)

        pygame.display.flip()

    save_preferences(music_on, current_theme_index, volume)
    return current_bg_image_path
