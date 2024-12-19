import sys
import pygame
import pygame_widgets
import numpy as np
import matplotlib.pyplot as plt
from resources import *
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown

def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

def plot_map():
    session = ff1.get_session(int(year_text), dropdown.getSelected(), 'R')
    session.load()

    lap = session.laps.pick_fastest()
    pos = lap.get_pos_data()

    circuit_info = session.get_circuit_info()
    
    plt.style.use('dark_background')
    
    # Get an array of shape [n, 2] where n is the number of points and the second
    # axis is x and y.
    track = pos.loc[:, ('X', 'Y')].to_numpy()

    # Convert the rotation angle from degrees to radian.
    track_angle = circuit_info.rotation / 180 * np.pi

    # Rotate and plot the track map.
    rotated_track = rotate(track, angle=track_angle)
    plt.plot(rotated_track[:, 0], rotated_track[:, 1])
    
    offset_vector = [500, 0]  # offset length is chosen arbitrarily to 'look good'

    # Iterate over all corners.
    for _, corner in circuit_info.corners.iterrows():
        # Create a string from corner number and letter
        txt = f"{corner['Number']}{corner['Letter']}"

        # Convert the angle from degrees to radian.
        offset_angle = corner['Angle'] / 180 * np.pi

        # Rotate the offset vector so that it points sideways from the track.
        offset_x, offset_y = rotate(offset_vector, angle=offset_angle)

        # Add the offset to the position of the corner
        text_x = corner['X'] + offset_x
        text_y = corner['Y'] + offset_y

        # Rotate the text position equivalently to the rest of the track map
        text_x, text_y = rotate([text_x, text_y], angle=track_angle)

        # Rotate the center of the corner equivalently to the rest of the track map
        track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle)

        # Draw a circle next to the track.
        plt.scatter(text_x, text_y, color='red', s=140)

        # Draw a line from the track to this circle.
        plt.plot([track_x, text_x], [track_y, text_y], color='red')

        # Finally, print the corner number inside the circle.
        plt.text(text_x, text_y, txt,
                 va='center_baseline', ha='center', size='small', color='black')
    
    plt.title(session.event['Location'])
    plt.xticks([])
    plt.yticks([])
    plt.axis('equal')
    plt.show()

def view_map(screen):
    global year_text, active_box, error_message, dropdown
    bg_image_path = 'assets/bg.jpg'
    logo_image = pygame.image.load("assets/f1.png")
    logo_image = pygame.transform.scale(logo_image, (300, 100))
    bg_image = pygame.image.load(bg_image_path).convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    input_width, input_height = 300, 40
    year_box = pygame.Rect(WIDTH // 2 - input_width // 2, HEIGHT // 2 - 30, input_width, input_height)
    submit_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 40, 150, 50)
    return_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 110, 150, 50)
    year_text = ""
    active_box = None
    error_message = ""
    dropdown_visible = False
    dropdown = None  # Initialize dropdown variable
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if year_box.collidepoint(event.pos) and not dropdown_visible:
                    active_box = "year"
                elif submit_button.collidepoint(event.pos) and not dropdown_visible:
                    if year_text:
                        try:
                            session = ff1.get_event_schedule(int(year_text))
                            countries = session["EventName"].tolist()
                            if countries[0]=="Pre-Season Testing":
                                countries.remove("Pre-Season Testing")
                            dropdown_visible = True
                            dropdown = Dropdown(
                                screen, 685, 20, 550, 27, name='Select Grand Prix',
                                choices=countries, fontSize=25,
                                borderRadius=5, colour=pygame.Color('gray'), values=countries, direction='down', textHAlign='centre', textColor=pygame.Color('Red')
                            )
                            
                            button = Button(
                                screen, 890, 200, 150, 50, text='View Map',
                                margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
                                font=pygame.font.SysFont('arial', 25, bold=True), radius=5,
                                textVAlign='centre', onClick=plot_map
                            )
                            
                        except Exception as e:
                            error_message = "Error fetching data. Please try again."
                elif return_button.collidepoint(event.pos):
                    return
                else:
                    error_message = "Please enter a year."

            if event.type == pygame.KEYDOWN:
                if active_box == "year":
                    if event.key == pygame.K_BACKSPACE:
                        year_text = year_text[:-1]
                    else:
                        year_text += event.unicode

        # Drawing the background
        screen.blit(bg_image, (0, 0))

        if not dropdown_visible:
            # Draw the logo in the center at the top
            screen.blit(logo_image, (WIDTH // 2 - logo_image.get_width() // 2, 20))
            draw_text(screen, "View Maps", 100, WHITE, 460, logo_image.get_height() + 10, center=False)

            # Draw the return button
            pygame.draw.rect(screen, RED, return_button)
            draw_text(screen, "Return to Menu", 24, WHITE, return_button.centerx, return_button.centery, center=True)

            # Draw input fields and buttons
            pygame.draw.rect(screen, LIGHT_GRAY, year_box)
            pygame.draw.rect(screen, RED, submit_button)

            draw_text(screen, "Year", 24, WHITE, year_box.centerx, year_box.centery - 35, center=True)
            draw_text(screen, "Submit", 24, WHITE, submit_button.centerx, submit_button.centery, center=True)
            draw_text(screen, year_text, 24, BLACK, year_box.centerx, year_box.centery, center=True)

            if error_message:
                draw_text(screen, error_message, 20, RED, WIDTH // 2, HEIGHT // 2 + 100, center=True)
        else:
            # Move the logo to the left side
            screen.blit(logo_image, (150, 20))

            # Draw the title "Buy Ticket" below the logo
            draw_text(screen, "View Maps", 100, WHITE, 110, logo_image.get_height() + 10, center=False)

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

