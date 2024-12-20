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
        link = gp_info[dropdown.getSelected()][2]
        webbrowser.open(link)
    except Exception as e:
        error_message = "Please select a GP"

def buy_ticket(screen):
    global error_message, dropdown
    logo_image = pygame.image.load(logo_image_path)
    logo_image = pygame.transform.scale(logo_image, (300, 100))
    bg_image = pygame.image.load(bg_image_path).convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    year = 2024  # Using 2024 temporarily since 2025 isn't available in fastf1 yet
    dropdown = None  # Initialize dropdown variable
    error_message = ""
    running = True

    session = ff1.get_event_schedule(year)
    countries = session["EventName"].tolist()
    if countries[0] == "Pre-Season Testing":
        countries.remove("Pre-Season Testing")

    dropdown = Dropdown(
        screen, 685, 20, 550, 27, name='Select Grand Prix',
        choices=countries, fontSize=25,
        borderRadius=5, colour=pygame.Color('gray'), values=countries, direction='down', textHAlign='centre',
        textColor=pygame.Color('Red')
    )

    button = Button(
        screen, 890, 200, 150, 50, text='Buy Tickets',
        margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
        font=pygame.font.SysFont('arial', 25, bold=True), radius=5,
        textVAlign='centre', onClick=redirect
    )

    while running:
        events = pygame.event.get()

        # Drawing the background
        screen.blit(bg_image, (0, 0))

        # Move the logo to the left side
        screen.blit(logo_image, (150, 20))

        # Draw the title "Buy Ticket" below the logo
        draw_text(screen, "Buy Tickets", 100, WHITE, 110, logo_image.get_height() + 10, center=False)

        # Draw the description below the title
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

        # Adjust the starting Y position for the description
        description_start_y = logo_image.get_height() + 100  # Move down to make space for the title
        for i, line in enumerate(description_lines):
            draw_text(screen, line, 24, WHITE, 20, description_start_y + i * 30, center=False)

        # Draw the return button below the description
        return_button = pygame.Rect(230, 550, 150, 50)

        # Draw the return button
        pygame.draw.rect(screen, RED, return_button)
        draw_text(screen, "Return to Menu", 24, WHITE, return_button.centerx, return_button.centery, center=True)

        if error_message:
            draw_text(screen, error_message, 20, RED, WIDTH // 2, HEIGHT // 2 + 200, center=True)

        # Handle events after drawing
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.pos:  # Check if event has pos
                if return_button.collidepoint(event.pos):
                    return  # Go back to the previous menu

        # Draw the dropdown menu if it is visible
        dropdown.draw()
        pygame_widgets.update(events)

        pygame.display.flip()
