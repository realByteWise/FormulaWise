import sys
import pygame_widgets
import webbrowser
from resources import *
from pygame_widgets.dropdown import Dropdown


def redirect():
    try:
        link = gp_info_2025[tickets_dropdown.getSelected()][2]
        webbrowser.open(link)
    except Exception:
        return "Please select a GP"
    return "Please check redirected window."

def buy_tickets(screen, current_bg_image_path):
    global tickets_dropdown
    logo_image = pygame.image.load(logo_image_path)
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    bg_image = pygame.image.load(current_bg_image_path).convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    return_button = pygame.Rect(245, 600, 150, 50)
    buy_tickets_button = pygame.Rect(885, 100, 150, 50)

    error_message = ""
    running = True
    today = datetime.today()
    countries = [location for location, details in gp_info_2025.items() if today <= details[0]]

    tickets_dropdown = Dropdown(
        screen, 685, 20, 550, 27, name='Select Grand Prix',
        choices=countries, fontSize=25, borderRadius=5, textHAlign='centre',
        colour=pygame.Color('gray'), values=countries, direction='down'
    )

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buy_tickets_button.collidepoint(event.pos):
                    error_message = redirect()
                if return_button.collidepoint(event.pos):
                    tickets_dropdown.toggleDropped() if tickets_dropdown.isDropped() else ...
                    tickets_dropdown.hide()
                    return

        draw_image(screen, bg_image, 0, 0)
        draw_image(screen, logo_image, WIDTH // 4, logo_image.get_height() - 30, center=True)
        draw_text(screen, "Buy Tickets", 80, WHITE, WIDTH // 4, logo_image.get_height() + 40, center=True)

        description_lines = [
            "Welcome to the Buy Tickets page. Here you can select a Grand Prix of the year",
            "2025 through the dropdown menu. This is a date-based system, which means",
            "if a Grand Prix is already over, it won't show in the dropdown menu.",
            " ",
            "When you select a Grand Prix, a map of the race track will appear on the",
            "'[ MAP ]' placeholder. So if you don't know details of a track, such as the name",
            "or the seat placement, you can see it on the map and confirm it.",
            " ",
            "Once you have selected a Grand Prix, click the 'Buy Tickets' button. You will",
            "then be redirected to the official Formula 1 ticket store. This feature has been",
            "made for a safe, reliable and accurate ticket buying experience."
        ]
        current_height = 250

        for line in description_lines:
            if line == " ":
                current_height += 15
            else:
                draw_text(screen, line, 24, WHITE, 45, current_height, center=False)
                current_height += 30

        pygame.draw.rect(screen, RED, return_button)
        pygame.draw.rect(screen, RED, buy_tickets_button)
        draw_text(screen, "Return to Menu", 24, WHITE, return_button.centerx, return_button.centery, center=True)
        draw_text(screen, "Buy Tickets", 24, WHITE, buy_tickets_button.centerx, buy_tickets_button.centery, center=True)

        gp = tickets_dropdown.getSelected()
        if gp is not None:
            if error_message != "Please check redirected window.":
                error_message = ""
            map_image = pygame.image.load(gp_info_2025[gp][1])
            map_image = pygame.transform.scale(map_image, (500, 500))
            draw_image(screen, map_image, int(WIDTH * (3 / 4)), 438, center=True)
        else:
            draw_text(screen, "[ MAP ]", 80, WHITE, int(WIDTH * (3 / 4)), 438, center=True)

        if error_message:
            draw_text(screen, error_message, 30, RED, int(WIDTH * (3 / 4)), 75, center=True)

        pygame_widgets.update(events)
        pygame.display.flip()
