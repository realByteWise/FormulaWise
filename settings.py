import sys
from resources import *


music_on, current_theme_index, volume, login_date = load_preferences()

def play_current_track():
    pygame.mixer.music.load(themes[current_theme_index][0])
    pygame.mixer.music.play(-1)

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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_preferences(music_on, current_theme_index, volume, login_date)
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
        draw_image(screen, bg_image, 0, 0)
        music_button_color = RED if music_on else BLUE
        music_button_rect = pygame.Rect(550, 200, 200, 50)
        pygame.draw.rect(screen, music_button_color, music_button_rect)
        draw_text(screen, "Music: ON" if music_on else "Music: OFF", 24, WHITE, music_button_rect.centerx, music_button_rect.centery, center=True)
        pygame.draw.rect(screen, GRAY, slider_rect)
        pygame.draw.rect(screen, RED, slider_handle_rect)
        draw_text(screen, f"Volume: {int(volume * 100)}%", 24, WHITE,slider_rect.centerx, slider_rect.y - 30, center=True)
        pygame.draw.rect(screen, RED, change_music_button_rect)
        draw_text(screen, "Change Theme", 24, WHITE, change_music_button_rect.centerx, change_music_button_rect.centery, center=True)
        pygame.draw.rect(screen, RED, return_button_rect)
        draw_text(screen, "Save & Return", 24, WHITE, return_button_rect.centerx, return_button_rect.centery, center=True)

        pygame.display.flip()

    save_preferences(music_on, current_theme_index, volume, login_date)
    return current_bg_image_path
