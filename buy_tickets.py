import sys
import pygame_widgets
import webbrowser
from resources import *
from pygame_widgets.dropdown import Dropdown


def redirect():
    global error_message
    try:
        link = gp_info_2025[tickets_dropdown.getSelected()][2]
        webbrowser.open(link)
    except Exception:
        error_message = "Please select a GP"
    error_message = "Please check redirected window."

def buy_tickets(screen, current_bg_image_path):
    global error_message, tickets_dropdown
    logo_image = pygame.image.load(logo_image_path)
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    bg_image = pygame.image.load(current_bg_image_path).convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    return_button = pygame.Rect(245, 550, 150, 50)
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
                    redirect()
                if return_button.collidepoint(event.pos):
                    tickets_dropdown.toggleDropped() if tickets_dropdown.isDropped() else ...
                    tickets_dropdown.hide()
                    return

        draw_image(screen, bg_image, 0, 0)
        draw_image(screen, logo_image, WIDTH // 4, logo_image.get_height() - 30, center=True)
        draw_text(screen, "Buy Tickets", 80, WHITE, WIDTH // 4, logo_image.get_height() + 40, center=True)

        description_lines = [
            "This feature allows you to select a previous Grand Prix of the year entered.",
            "You can view the standings of the race along with the podium finishers.",
            "Simply enter the desired year and click submit to see the available races.",
            "Select a Grand Prix from the dropdown menu to view detailed results.",
            "The standings will include driver positions, points earned, and team information.",
            "Explore historical data to analyze past performances and trends.",
            "This feature is perfect for fans wanting to revisit memorable races.",
            "Stay updated with the latest statistics and records from previous seasons.",
            "Easily navigate through different years to find your favorite races.",
            "Feature implementation date: 19/12/2024."
        ]
        description_start_y = logo_image.get_height() + 100

        for i, line in enumerate(description_lines):
            draw_text(screen, line, 24, WHITE, 45, description_start_y + i * 30, center=False)

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
