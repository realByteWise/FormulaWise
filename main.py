import sys
from resources import *
from view_map import view_map
from buy_ticket import buy_ticket
from heatmaps import heatmaps
from race_winner import show_podium

show_main_menu_buttons = True
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(r'assets\Gas.mp3')
pygame.mixer.music.play(-1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FormulaWise")
bg_image = pygame.image.load("assets/bg.jpg")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
logo_image = pygame.image.load("assets/f1.png")
logo_image = pygame.transform.scale(logo_image, (300, 100))
font = pygame.font.Font(pygame.font.match_font('Palatino'), 24)
input_width, input_height = 300, 40
username_box = pygame.Rect(WIDTH // 2 - input_width // 2, HEIGHT // 2 - 100, input_width, input_height)
password_box = pygame.Rect(WIDTH // 2 - input_width // 2, HEIGHT // 2 - 30, input_width, input_height)
login_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 60, 150, 50)
signup_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 130, 150, 50)
username_text = ""
password_text = ""
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
button_colors = [GRAY, GRAY, GRAY,GRAY, RED]
button_labels = ["VIEW MAP", "BUY TICKET", "HEATMAPS", "RACE WINNER",'SIGN OUT']

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
                elif login_button.collidepoint(event.pos):
                    if is_signing_up:
                        if username_text and password_text:
                            if username_text in credentials:
                                error_message = "Username already exists!"
                            else:
                                credentials[username_text] = password_text
                                save_credentials(username_text, password_text)
                                error_message = "Sign-Up Successful! Please log in."
                                username_text, password_text = "", ""
                                is_signing_up = False
                        else:
                            error_message = "Please fill all fields."
                    else:
                        if username_text in credentials and credentials[username_text] == password_text:
                            is_logged_in = True
                            username_text, password_text = "", ""
                        else:
                            error_message = "Invalid username or password."
                elif signup_button.collidepoint(event.pos):
                    is_signing_up = True
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

        else:  
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        if i == 0:
                            view_map(screen)
                            screen.blit(bg_image, (0, 0))
                        elif i == 1:
                            buy_ticket(screen)
                        elif i == 2:
                            screen.blit(bg_image, (0, 0))
                            heatmaps(screen) 
                        elif i == 3:
                            screen.blit(bg_image, (0, 0))
                            show_podium(screen)
                        elif i == 4:
                            is_logged_in=False
    screen.blit(bg_image, (0, 0))
    if not is_logged_in:
        screen.blit(logo_image, (WIDTH // 2 - 150, HEIGHT // 2 - 250))
        pygame.draw.rect(screen, LIGHT_GRAY, username_box)
        pygame.draw.rect(screen, LIGHT_GRAY, password_box)
        pygame.draw.rect(screen, RED, login_button)
        pygame.draw.rect(screen, RED, signup_button)

        draw_text(screen, "Username", 24, WHITE, username_box.centerx, username_box.centery - 40, center=True)
        draw_text(screen, "Password", 24, WHITE, password_box.centerx, password_box.centery - 35, center=True)
        draw_text(screen, "Login", 24, WHITE, login_button.centerx, login_button.centery, center=True)
        draw_text(screen, "Sign Up", 24, WHITE, signup_button.centerx, signup_button.centery, center=True)
        if error_message:
            draw_text(screen, error_message, 20, RED, WIDTH // 2, HEIGHT // 2 + 200, center=True)
        draw_text(screen, username_text, 24, BLACK, username_box.centerx, username_box.centery, center=True)
        draw_text(screen, password_text, 24, BLACK, password_box.centerx, password_box.centery, center=True)

    else:
        for i, button in enumerate(buttons):
            pygame.draw.rect(screen, button_colors[i], button)
            draw_text(screen, button_labels[i], 24, WHITE, button.centerx, button.centery, center=True)

    pygame.display.flip()

pygame.quit()
sys.exit()
