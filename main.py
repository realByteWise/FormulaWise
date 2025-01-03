import sys
from resources import *
from view_maps import view_maps
from buy_tickets import buy_tickets
from heatmaps import heatmaps
from race_results import show_positions
from settings import show_settings
from datetime import timedelta


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FormulaWise")
icon_image = pygame.image.load("assets/fw.png")
pygame.display.set_icon(icon_image)

# defining image variables
bytewise = pygame.image.load("assets/bytewise.png")
bytewise = pygame.transform.scale(bytewise, (75, 75))
music_on, current_theme_index, volume, login_date, details = load_preferences()
current_bg_image_path = themes[current_theme_index][1]
bg_image = pygame.image.load(current_bg_image_path)
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
logo_image = pygame.image.load(logo_image_path)
logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
settings_button_image = pygame.image.load("assets/settings.png")
settings_button_rect = settings_button_image.get_rect(center=(260, 900))
settings_button_image = pygame.transform.scale(settings_button_image, (50, 50))
show_password_image = pygame.image.load("assets/show_password.jpg").convert()
hide_password_image = pygame.image.load("assets/hide_password.jpg").convert()

pygame.mixer.init()
pygame.mixer.music.load(themes[current_theme_index][0])
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volume)

# defining text and flag variables
username_text = ""
hidden_password = ""
password_text = ""
confirm_password_text = ""
hidden_confirm_password = ""
error_message = ""
active_box = None
is_signing_up = False
credits_page = False
show_password = False
show_confirm_password = False

credentials = load_credentials()
today = datetime.today()
valid_date = today - timedelta(days=8)
if login_date < valid_date:
    is_logged_in = False
else:
    is_logged_in = True

# defining box and button variables
username_box = pygame.Rect(WIDTH // 2 - input_width // 2, HEIGHT // 2 - 100, input_width, input_height)
password_box = pygame.Rect(WIDTH // 2 - input_width // 2, HEIGHT // 2 - 20, input_width, input_height)
confirm_password_box = pygame.Rect(WIDTH // 2 - input_width // 2, HEIGHT // 2 + 60, input_width, input_height)
login_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 60, button_width, button_height)
signup_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 130, button_width, button_height)
cancel_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 200, button_width, button_height)
buttons = [
    (pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 130, button_width, button_height), GRAY, "VIEW MAPS"),
    (pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 60, button_width, button_height), GRAY, "BUY TICKETS"),
    (pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 10, button_width, button_height), GRAY, "HEATMAPS"),
    (pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 80, button_width, button_height), GRAY, "RACE RESULTS"),
    (pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 150, button_width, button_height), RED, "SIGN OUT")
]

running = True
while running:
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif not is_logged_in:
            if event.type == pygame.MOUSEBUTTONDOWN:
                credits_page = False
                if username_box.collidepoint(event.pos):
                    active_box = "username"
                elif password_box.collidepoint(event.pos):
                    active_box = "password"
                elif login_button and login_button.collidepoint(event.pos):
                    if username_text and password_text:
                        if username_text in credentials and credentials[username_text] == password_text:
                            login_date = datetime.today()
                            is_logged_in = True
                            save_preferences(music_on, current_theme_index, volume, login_date, (username_text, password_text))
                            username_text, error_message = "", ""
                            password_text, hidden_password = "", ""
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
                                valid_pass = password_validator(password_text)
                                if valid_pass[0]:
                                    valid_user = username_validator(username_text)
                                    if valid_user[0]:
                                        if username_text in credentials:
                                            error_message = "Username already exists!"
                                        else:
                                            credentials[username_text] = password_text
                                            save_credentials(username_text, password_text)
                                            error_message = "Sign-Up Successful! Please log in."
                                            username_text, password_text, confirm_password_text, = "", "", ""
                                            hidden_password, hidden_confirm_password = "", ""
                                            is_signing_up = False
                                            login_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 60, button_width, button_height)
                                    else:
                                        error_message = valid_user[1]
                                else:
                                    error_message = valid_pass[1]
                            else:
                                error_message = "Passwords don't match."
                        else:
                            error_message = "Please fill all fields."
                elif is_signing_up:
                    if confirm_password_box.collidepoint(event.pos):
                        active_box = "confirm_password"
                    elif cancel_button.collidepoint(event.pos):
                        confirm_password_text, error_message, hidden_confirm_password = "", "", ""
                        is_signing_up = False
                        login_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 60, button_width, button_height)
                elif settings_button_rect.collidepoint(event.pos):
                    username_text, password_text, hidden_password = "", "", ""
                    current_bg_image_path = show_settings(screen,current_bg_image_path)
                    music_on, current_theme_index, volume, login_date, details = load_preferences()
                    bg_image = pygame.image.load(current_bg_image_path).convert()
                    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_F1, pygame.KSCAN_F1):
                    show_credits()
                    credits_page = True
                if active_box == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    else:
                        username_text += event.unicode
                elif active_box == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                        hidden_password = hidden_password[:-1]
                    else:
                        password_text += event.unicode
                        if event.key not in special_keys:
                            hidden_password += "*"
                elif active_box == "confirm_password":
                    if event.key == pygame.K_BACKSPACE:
                        confirm_password_text = confirm_password_text[:-1]
                        hidden_confirm_password = hidden_confirm_password[:-1]
                    else:
                        confirm_password_text += event.unicode
                        if event.key not in special_keys:
                            hidden_confirm_password += "*"
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                credits_page = False
                for i, button in enumerate(buttons):
                    if button[0].collidepoint(event.pos):
                        if i == 0:
                            view_maps(screen, current_bg_image_path)
                        elif i == 1:
                            buy_tickets(screen, current_bg_image_path)
                        elif i == 2:
                            heatmaps(screen,current_bg_image_path)
                        elif i == 3:
                            show_positions(screen, current_bg_image_path)
                        elif i == 4:
                            login_date = datetime(2023, 10, 3)
                            details = ("1", "1")
                            save_preferences(music_on, current_theme_index, volume, login_date, details)
                            is_logged_in = False

                if settings_button_rect.collidepoint(event.pos):
                    current_bg_image_path = show_settings(screen,current_bg_image_path)
                    music_on, current_theme_index, volume, login_date, details = load_preferences()
                    bg_image = pygame.image.load(current_bg_image_path).convert()
                    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_F1, pygame.KSCAN_F1):
                    show_credits()
                    credits_page = True

    # rendering
    draw_image(screen, bg_image, 0, 0)
    draw_image(screen, logo_image, WIDTH // 2, 160, center=True)
    draw_image(screen, settings_button_image, 35, 675, center=True)
    draw_text(screen, "Settings", 24, WHITE, 35, 710, center=True)
    draw_image(screen, bytewise, 1240, 680, center=True)

    if credits_page:
        draw_text(screen, "Check console for credits.", 30, RED, WIDTH // 2, 650, center=True)

    if not is_logged_in:
        pygame.draw.rect(screen, LIGHT_GRAY, username_box, border_radius=5)
        pygame.draw.rect(screen, LIGHT_GRAY, password_box, border_radius=5)
        pygame.draw.rect(screen, RED, signup_button, border_radius=5)

        draw_text(screen, "Username", 24, WHITE, username_box.centerx, username_box.centery - 40, center=True)
        draw_text(screen, "Password", 24, WHITE, password_box.centerx, password_box.centery - 40, center=True)
        draw_text(screen, "Sign Up", 24, WHITE, signup_button.centerx, signup_button.centery, center=True)

        draw_text(screen, username_text, 24, BLACK, username_box.centerx, username_box.centery, center=True)

        if show_password:
            draw_text(screen, password_text, 24, BLACK, password_box.centerx, password_box.centery, center=True)
        else:
            draw_text(screen, hidden_password, 40, BLACK, password_box.centerx, password_box.centery + 7, center=True)

        if password_text:
            show_password_button = Button(WIDTH // 2 + 105, 340, hide_password_image if show_password else show_password_image,40, 40)
            if show_password_button.draw(screen):
                sleep(0.05)
                show_password = not show_password

        if not is_signing_up:
            pygame.draw.rect(screen, RED, login_button, border_radius=5)
            draw_text(screen, "Login", 24, WHITE, login_button.centerx, login_button.centery, center=True)

            if error_message:
                draw_text(screen, error_message, 20, RED, WIDTH // 2, HEIGHT // 2 + 40, center=True)
        else:
            pygame.draw.rect(screen, LIGHT_GRAY, confirm_password_box, border_radius=5)
            pygame.draw.rect(screen, RED, cancel_button, border_radius=5)
            draw_text(screen, "Confirm Password", 24, WHITE, confirm_password_box.centerx, confirm_password_box.centery - 40, center=True)
            draw_text(screen, "Cancel", 24, WHITE, cancel_button.centerx, cancel_button.centery, center=True)

            if show_confirm_password:
                draw_text(screen, confirm_password_text, 24, BLACK, confirm_password_box.centerx, confirm_password_box.centery, center=True)
            else:
                draw_text(screen, hidden_confirm_password, 40, BLACK, confirm_password_box.centerx, confirm_password_box.centery + 7, center=True)

            if confirm_password_text:
                show_confirm_password_button = Button(WIDTH // 2 + 105, 420, hide_password_image if show_confirm_password else show_password_image, 40, 40)
                if show_confirm_password_button.draw(screen):
                    sleep(0.05)
                    show_confirm_password = not show_confirm_password

            if error_message:
                draw_text(screen, error_message, 20, RED, WIDTH // 2, HEIGHT // 2 + 115, center=True)
    else:
        for i, button in enumerate(buttons):
            pygame.draw.rect(screen, button[1], button[0], border_radius=5)
            draw_text(screen, button[2], 24, BLACK if i != 4 else WHITE, button[0].centerx, button[0].centery, center=True)

    pygame.display.flip()

save_preferences(music_on, current_theme_index, volume, login_date, details)
pygame.quit()
sys.exit()
