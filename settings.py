import sys
from resources import *
from datetime import timedelta


def play_current_track(current_theme_index, music_on):
    pygame.mixer.music.load(themes[current_theme_index][0])
    pygame.mixer.music.play(-1)
    if not music_on:
        pygame.mixer.music.pause()

def show_settings(screen, current_bg_image_path):
    global bg_image, login_date, details, return_button_rect
    music_on, current_theme_index, volume, login_date, details = load_preferences()
    bg_image = pygame.image.load(themes[current_theme_index][1]).convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    slider_rect = pygame.Rect(540, 390, 200, 10)
    slider_handle_rect = pygame.Rect(slider_rect.x + volume * slider_rect.width - 10, slider_rect.y - 10, 20, 30)  
    return_button_rect = pygame.Rect(540, 500, 200, 50)
    change_music_button_rect = pygame.Rect(540, 430, 200, 50)
    music_button_rect = pygame.Rect(540, 295, 200, 50)
    edit_profile_button_rect = pygame.Rect(540, 225, 200, 50)
    pygame.mixer.music.set_volume(volume)

    dragging = False
    username_text = details[0]
    password_text = details[1]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_preferences(music_on, current_theme_index, volume, login_date, (username_text, password_text))
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if slider_handle_rect.collidepoint(event.pos):
                        dragging = True
                    elif music_button_rect.collidepoint(event.pos):
                        music_on = not music_on
                        if music_on:
                            pygame.mixer.music.unpause()  
                        else:
                            pygame.mixer.music.pause()
                            
                    elif change_music_button_rect.collidepoint(event.pos):
                        current_theme_index = (current_theme_index + 1) % len(themes)
                        play_current_track(current_theme_index, music_on)
                        bg_image = pygame.image.load(themes[current_theme_index][1]).convert()
                        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))  
                        current_bg_image_path = themes[current_theme_index][1]

                    elif edit_profile_button_rect.collidepoint(event.pos):
                        save_preferences(music_on, current_theme_index, volume, login_date, (username_text, password_text))
                        edit_profile(screen)
                    elif return_button_rect.collidepoint(event.pos):
                        running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
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
        draw_text(screen, "Settings", 80, WHITE, WIDTH // 2, 100, center=True)
        pygame.draw.rect(screen, RED, edit_profile_button_rect, border_radius=5)
        draw_text(screen, "Edit Profile", 24, WHITE, edit_profile_button_rect.centerx, edit_profile_button_rect.centery, center=True)
        pygame.draw.rect(screen, RED if music_on else BLUE, music_button_rect, border_radius=5)
        draw_text(screen, "Music: ON" if music_on else "Music: OFF", 24, WHITE, music_button_rect.centerx, music_button_rect.centery, center=True)
        pygame.draw.rect(screen, GRAY, slider_rect, border_radius=5)
        pygame.draw.rect(screen, RED, slider_handle_rect, border_radius=5)
        draw_text(screen, f"Volume: {int(volume * 100)}%", 24, WHITE,slider_rect.centerx, slider_rect.y - 25, center=True)
        pygame.draw.rect(screen, RED, change_music_button_rect, border_radius=5)
        draw_text(screen, "Change Theme", 24, WHITE, change_music_button_rect.centerx, change_music_button_rect.centery, center=True)
        pygame.draw.rect(screen, RED, return_button_rect, border_radius=5)
        draw_text(screen, "Save & Return", 24, WHITE, return_button_rect.centerx, return_button_rect.centery, center=True)

        pygame.display.flip()

    save_preferences(music_on, current_theme_index, volume, login_date, (username_text, password_text))
    return current_bg_image_path

def edit_profile(screen):
    global bg_image, login_date, details, return_button_rect

    show_password_image = pygame.image.load("assets/show_password.jpg").convert()
    hide_password_image = pygame.image.load("assets/hide_password.jpg").convert()

    username_box = pygame.Rect(WIDTH // 2 - 150, 215, input_width, input_height)
    password_box = pygame.Rect(WIDTH // 2 - 150, 285, input_width, input_height)
    confirm_password_box = pygame.Rect(WIDTH // 2 - 150, 355, input_width, input_height)
    edit_username_box = pygame.Rect(WIDTH // 2 + 170, 215, 200, input_height)
    edit_password_box = pygame.Rect(WIDTH // 2 + 170, 285, 200, input_height)
    cancel_button_username = pygame.Rect(1030, 215, 200, input_height)
    cancel_button_password = pygame.Rect(WIDTH // 2 + 170, 355, 200, input_height)

    username_text, password_text = details[0], details[1]
    old_username, old_password = details[0], details[1]
    confirm_password_text, hidden_confirm_password = "", ""
    hidden_password = "*" * len(password_text)
    error_message = ""
    active_box = None
    edit_username = False
    edit_password = False
    show_password = False
    show_confirm_password = False

    today = datetime.today()
    valid_date = today - timedelta(days=8)
    if login_date < valid_date:
        is_logged_in = False
    else:
        is_logged_in = True

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if username_box.collidepoint(event.pos):
                    active_box = "username"
                elif password_box.collidepoint(event.pos):
                    active_box = "password"
                elif confirm_password_box.collidepoint(event.pos):
                    active_box = "confirm_password"
                elif edit_username_box.collidepoint(event.pos):
                    if not edit_password:
                        if edit_username:
                            if username_text:
                                if username_text != old_username:
                                    valid_user = username_validator(username_text)
                                    if valid_user[0]:
                                        edit_credentials(old_username, password_text, username_text)
                                        edit_username = False
                                        error_message = "New username successfully saved."
                                    else:
                                        error_message = valid_user[1]
                                else:
                                    error_message = "Please make a new username or cancel."
                            else:
                                error_message = "Please fill username field."
                        else:
                            edit_username = True
                    else:
                        error_message = "Please save password first."
                elif edit_password_box.collidepoint(event.pos):
                    if not edit_username:
                        if edit_password:
                            if password_text and confirm_password_text:
                                if password_text == confirm_password_text:
                                    if password_text != old_password:
                                        valid_pass = password_validator(password_text)
                                        if valid_pass[0]:
                                            edit_credentials(old_username, password_text)
                                            edit_password = False
                                            error_message = "New password successfully saved."
                                        else:
                                            error_message = valid_pass[1]
                                    else:
                                        error_message = "Please use a different password or cancel."
                                else:
                                    error_message = "Passwords don't match."
                            else:
                                error_message = "Please fill all fields."
                        else:
                            edit_password = True
                            password_text, hidden_password = "", ""
                    else:
                        error_message = "Please save username first."
                elif cancel_button_password.collidepoint(event.pos):
                    edit_password = False
                    password_text, hidden_password = old_password, "*" * len(old_password)
                    confirm_password_text, hidden_confirm_password, error_message = "", "", ""
                elif cancel_button_username.collidepoint(event.pos):
                    edit_username = False
                    username_text, error_message = old_username, ""
                elif return_button_rect.collidepoint(event.pos):
                    return

            elif event.type == pygame.KEYDOWN:
                if active_box == "username" and edit_username:
                    if event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    else:
                        username_text += event.unicode
                elif active_box == "password" and edit_password:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                        hidden_password = hidden_password[:-1]
                    else:
                        password_text += event.unicode
                        if event.key not in special_keys:
                            hidden_password += "*"
                elif active_box == "confirm_password" and edit_password:
                    if event.key == pygame.K_BACKSPACE:
                        confirm_password_text = confirm_password_text[:-1]
                        hidden_confirm_password = hidden_confirm_password[:-1]
                    else:
                        confirm_password_text += event.unicode
                        if event.key not in special_keys:
                            hidden_confirm_password += "*"

        draw_image(screen, bg_image, 0, 0)
        pygame.draw.rect(screen, RED, return_button_rect, border_radius=5)
        draw_text(screen, "Return", 24, WHITE, return_button_rect.centerx, return_button_rect.centery, center=True)

        if is_logged_in:
            pygame.draw.rect(screen, LIGHT_GRAY, username_box, border_radius=5)
            pygame.draw.rect(screen, LIGHT_GRAY, password_box, border_radius=5)
            draw_text(screen, "Edit Profile", 80, WHITE, WIDTH // 2, 100, center=True)
            draw_text(screen, "Username:", 30, WHITE, 250, 225)
            draw_text(screen, username_text, 24, BLACK, username_box.centerx, username_box.centery, center=True)
            draw_text(screen, "Password:" if not edit_password else "New Password:", 30, WHITE, 250, 300)

            if show_password:
                draw_text(screen, password_text, 24, BLACK, password_box.centerx, password_box.centery, center=True)
            else:
                draw_text(screen, hidden_password, 40, BLACK, password_box.centerx, password_box.centery + 7, center=True)

            if password_text:
                show_password_button = Button(WIDTH // 2 + 105, 285, hide_password_image if show_password else show_password_image, 40, 40)
                if show_password_button.draw(screen):
                    sleep(0.05)
                    show_password = not show_password

            pygame.draw.rect(screen, RED, edit_username_box, border_radius=5)
            pygame.draw.rect(screen, RED, edit_password_box, border_radius=5)
            draw_text(screen, "Edit Username" if not edit_username else "Save Username", 24, WHITE, edit_username_box.centerx,
                      edit_username_box.centery, center=True)
            draw_text(screen, "Change Password" if not edit_password else "Save Password", 24, WHITE, edit_password_box.centerx,
                      edit_password_box.centery, center=True)

            if edit_username:
                pygame.draw.rect(screen, RED, cancel_button_username, border_radius=5)
                draw_text(screen, "Cancel", 24, WHITE, cancel_button_username.centerx, cancel_button_username.centery, center=True)

            if edit_password:
                pygame.draw.rect(screen, RED, cancel_button_password, border_radius=5)
                pygame.draw.rect(screen, LIGHT_GRAY, confirm_password_box, border_radius=5)
                draw_text(screen, "Cancel", 24, WHITE, cancel_button_password.centerx, cancel_button_password.centery, center=True)
                draw_text(screen, "Confirm Password:", 30, WHITE, 250, 365)

                if show_confirm_password:
                    draw_text(screen, confirm_password_text, 24, BLACK, confirm_password_box.centerx, confirm_password_box.centery, center=True)
                else:
                    draw_text(screen, hidden_confirm_password, 40, BLACK, confirm_password_box.centerx, confirm_password_box.centery + 7, center=True)

                if confirm_password_text:
                    show_confirm_password_button = Button(WIDTH // 2 + 105, 355, hide_password_image if show_confirm_password else show_password_image, 40, 40)
                    if show_confirm_password_button.draw(screen):
                        sleep(0.05)
                        show_confirm_password = not show_confirm_password

            if error_message:
                draw_text(screen, error_message, 30, RED, WIDTH // 2, 450, center=True)
        else:
            draw_text(screen, "Not Logged in.", 200, WHITE, WIDTH // 2, HEIGHT // 2 - 100, center=True)

        pygame.display.flip()
