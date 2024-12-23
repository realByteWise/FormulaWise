import sys
import pygame_widgets
import webbrowser
from resources import *
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown


def redirect():
    global error_message
    error_message = ""
    try:
        link = gp_info[tickets_dropdown.getSelected()][2]
        webbrowser.open(link)
    except Exception:
        error_message = "Please select a GP"

def buy_tickets(screen, current_bg_image_path):
    global error_message, tickets_dropdown
    logo_image = pygame.image.load(logo_image_path)
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    bg_image_path = current_bg_image_path
    bg_image = pygame.image.load(bg_image_path).convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    year = 2024  # Using 2024 temporarily since 2025 isn't available in fastf1 yet
    error_message = ""
    tickets_dropdown = None
    running = True

    session = ff1.get_event_schedule(year)
    countries = session["EventName"].tolist()

    if countries[0] == "Pre-Season Testing":
        countries.remove("Pre-Season Testing")

    tickets_dropdown = Dropdown(
        screen, 685, 20, 550, 27, name='Select Grand Prix',
        choices=countries, fontSize=25, borderRadius=5,
        colour=pygame.Color('gray'), values=countries, direction='down',
        textHAlign='centre', textColor=pygame.Color('Red')
    )

    buy_tickets_button = Button(
        screen, 890, 200, 150, 50, text='Buy Tickets',
        margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
        radius=5, font=pygame.font.SysFont(pygame.font.match_font('Palatino'), 25),
        textVAlign='centre', onClick=redirect
    )

    while running:
        events = pygame.event.get()
        screen.blit(bg_image, (0, 0))
        screen.blit(logo_image, (70, 20))
        draw_text(screen, "Buy Tickets", 100, WHITE, 110, logo_image.get_height() + 10, center=False)

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
            draw_text(screen, line, 24, WHITE, 20, description_start_y + i * 30, center=False)

        return_button = pygame.Rect(230, 550, 150, 50)
        pygame.draw.rect(screen, RED, return_button)
        draw_text(screen, "Return to Menu", 24, WHITE, return_button.centerx, return_button.centery, center=True)

        if error_message:
            draw_text(screen, error_message, 20, RED, WIDTH // 2, HEIGHT // 2 + 100, center=True)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.pos:
                if return_button.collidepoint(event.pos):
                    tickets_dropdown = None
                    buy_tickets_button = None
                    return  # Go back to the previous menu

        pygame_widgets.update(events)
        pygame.display.flip()

    tickets_dropdown = None
    buy_tickets_button = None
