import sys
from resources import *
from view_maps import view_maps
from buy_tickets import buy_tickets
from heatmaps import heatmaps
from race_positions import show_positions
from settings import show_settings


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FormulaWise")
icon_image = pygame.image.load("assets/fw.png")
pygame.display.set_icon(icon_image)
music_on, current_theme_index, volume = load_preferences()
current_bg_image_path = themes[current_theme_index][1]
bg_image = pygame.image.load(current_bg_image_path)
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
logo_image = pygame.image.load(logo_image_path)
logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
settings_button_image = pygame.image.load("assets/settings.png")
settings_button_rect = settings_button_image.get_rect(center=(260, 900))  
settings_button_image = pygame.transform.scale(settings_button_image, (50, 50))
font = pygame.font.Font(pygame.font.match_font('Palatino'), 24)
input_width, input_height = 300, 40
pygame.init()
pygame.mixer.init()
if music_on:
    pygame.mixer.music.load(themes[current_theme_index][0])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(volume)
username_box = pygame.Rect(WIDTH // 2 - input_width // 2, HEIGHT // 2 - 100, input_width, input_height)
password_box = pygame.Rect(WIDTH // 2 - input_width // 2, HEIGHT // 2 - 20, input_width, input_height)
confirm_password_box = pygame.Rect(WIDTH // 2 - input_width // 2, HEIGHT // 2 + 60, input_width, input_height)
login_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 60, 150, 50)
signup_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 130, 150, 50)
cancel_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 200, 150, 50)

username_text = ""
password_text = ""
confirm_password_text = ""
active_box = None
error_message = ""
is_signing_up = False
credentials = load_credentials()
is_logged_in = False

button_width, button_height = 150, 50
buttons = [
    pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 130, button_width, button_height),
    pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 60, button_width, button_height),
    pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 10, button_width, button_height),
    pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 80, button_width, button_height),
    pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 150, button_width, button_height),
]
button_colors = [GRAY, GRAY, GRAY, GRAY, RED]
button_labels = ["VIEW MAPS", "BUY TICKETS", "HEATMAPS", "RESULTS", "SIGN OUT"]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif not is_logged_in:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_box.collidepoint(event.pos):
                    active_box = "username"
                elif password_box.collidepoint(event.pos):
                    active_box = "password"
                elif login_button and login_button.collidepoint(event.pos):
                    if username_text and password_text:
                        if username_text in credentials and credentials[username_text] == password_text:
                            is_logged_in = True
                            username_text, password_text, error_message = "", "", ""
                        else:
                            error_message = "Invalid username or password."
                    else:
                        error_message = "Please fill all fields."
                elif signup_button.collidepoint(event.pos):
                    if not is_signing_up:
                        error_message = ""
                        login_button = None
                        is_signing_up = True
                    else:
                        if username_text and password_text and confirm_password_text:
                            if password_text == confirm_password_text:
                                if username_text in credentials:
                                    error_message = "Username already exists!"
                                else:
                                    credentials[username_text] = password_text
                                    save_credentials(username_text, password_text)
                                    error_message = "Sign-Up Successful! Please log in."
                                    username_text, password_text, confirm_password_text = "", "", ""
                                    is_signing_up = False
                                    login_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 60, 150, 50)
                            else:
                                error_message = "Passwords don't match."
                        else:
                            error_message = "Please fill all fields."
                elif is_signing_up:
                    if confirm_password_box.collidepoint(event.pos):
                        active_box = "confirm_password"
                    elif cancel_button.collidepoint(event.pos):
                        confirm_password_text, error_message = "", ""
                        is_signing_up = False
                        login_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 60, 150, 50)
                elif settings_button_rect.collidepoint(event.pos):
                    current_bg_image_path = show_settings(screen,current_bg_image_path)
                    bg_image = pygame.image.load(current_bg_image_path).convert()
                    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
            elif event.type == pygame.KEYDOWN:
                if active_box == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    else:
                        username_text += event.unicode
                elif active_box == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    else:
                        password_text += event.unicode
                elif active_box == "confirm_password":
                    if event.key == pygame.K_BACKSPACE:
                        confirm_password_text = confirm_password_text[:-1]
                    else:
                        confirm_password_text += event.unicode
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        if i == 0:
                            view_maps(screen, current_bg_image_path)
                        elif i == 1:
                            buy_tickets(screen, current_bg_image_path)
                        elif i == 2:
                            heatmaps(screen,current_bg_image_path)
                        elif i == 3:
                            show_positions(screen, current_bg_image_path)
                        elif i == 4:
                            is_logged_in = False  

                if settings_button_rect.collidepoint(event.pos):
                    current_bg_image_path = show_settings(screen,current_bg_image_path)  
                    bg_image = pygame.image.load(current_bg_image_path).convert()
                    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    screen.blit(bg_image, (0, 0))
    screen.blit(settings_button_image, settings_button_rect.topleft)
    if not is_logged_in:
        screen.blit(logo_image, (WIDTH // 2 - 250, HEIGHT // 2 - 250))
        pygame.draw.rect(screen, LIGHT_GRAY, username_box)
        pygame.draw.rect(screen, LIGHT_GRAY, password_box)
        pygame.draw.rect(screen, RED, signup_button)

        draw_text(screen, "Username", 24, WHITE, username_box.centerx, username_box.centery - 40, center=True)
        draw_text(screen, "Password", 24, WHITE, password_box.centerx, password_box.centery - 40, center=True)
        draw_text(screen, "Sign Up", 24, WHITE, signup_button.centerx, signup_button.centery, center=True)

        draw_text(screen, username_text, 24, BLACK, username_box.centerx, username_box.centery, center=True)
        draw_text(screen, password_text, 24, BLACK, password_box.centerx, password_box.centery, center=True)

        if not is_signing_up:
            pygame.draw.rect(screen, RED, login_button)
            draw_text(screen, "Login", 24, WHITE, login_button.centerx, login_button.centery, center=True)

            if error_message:
                draw_text(screen, error_message, 20, RED, WIDTH // 2, HEIGHT // 2 + 40, center=True)
        else:
            pygame.draw.rect(screen, LIGHT_GRAY, confirm_password_box)
            pygame.draw.rect(screen, RED, cancel_button)
            draw_text(screen, "Confirm Password", 24, WHITE, confirm_password_box.centerx, confirm_password_box.centery - 40, center=True)
            draw_text(screen, "Cancel", 24, WHITE, cancel_button.centerx, cancel_button.centery, center=True)
            draw_text(screen, confirm_password_text, 24, BLACK, confirm_password_box.centerx, confirm_password_box.centery, center=True)

            if error_message:
                draw_text(screen, error_message, 20, RED, WIDTH // 2, HEIGHT // 2 + 115, center=True)

    else:
        screen.blit(logo_image, (WIDTH // 2 - 250, HEIGHT // 2 - 250))
        for i, button in enumerate(buttons):
            pygame.draw.rect(screen, button_colors[i], button)
            draw_text(screen, button_labels[i], 24, WHITE, button.centerx, button.centery, center=True)
    pygame.display.flip()

pygame.quit()
sys.exit()
