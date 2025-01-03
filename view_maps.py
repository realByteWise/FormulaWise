import sys
import pygame_widgets
import numpy as np
import matplotlib.pyplot as plt
from resources import *
from pygame_widgets.dropdown import Dropdown


def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

def plot_map():
    try:
        session = ff1.get_session(int(year_text), maps_dropdown.getSelected(), 'R')
        session.load(weather=False, messages=False)
        lap = session.laps.pick_fastest()
        pos = lap.get_pos_data()
        circuit_info = session.get_circuit_info()
        plt.style.use('dark_background')
        track = pos.loc[:, ('X', 'Y')].to_numpy()
        track_angle = circuit_info.rotation / 180 * np.pi
        rotated_track = rotate(track, angle=track_angle)
        plt.plot(rotated_track[:, 0], rotated_track[:, 1])
        offset_vector = [500, 0]

        for _, corner in circuit_info.corners.iterrows():
            txt = f"{corner['Number']}{corner['Letter']}"
            offset_angle = corner['Angle'] / 180 * np.pi
            offset_x, offset_y = rotate(offset_vector, angle=offset_angle)
            text_x = corner['X'] + offset_x
            text_y = corner['Y'] + offset_y
            text_x, text_y = rotate([text_x, text_y], angle=track_angle)
            track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle)
            plt.scatter(text_x, text_y, color='red', s=140)
            plt.plot([track_x, text_x], [track_y, text_y], color='red')
            plt.text(text_x, text_y, txt,
                     va='center_baseline', ha='center', size='small', color='black')

        plt.title(session.event['Location'])
        plt.xticks([])
        plt.yticks([])
        plt.axis('equal')
        plt.show()
    except Exception as e:
        print(f"Error: {e}")  # Debugging
        return "Error fetching data. Please try again."
    return "Please check the loaded window for the map."

def view_maps(screen, current_bg_image_path):
    global year_text, maps_dropdown
    logo_image = pygame.image.load(logo_image_path)
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    bg_image = pygame.image.load(current_bg_image_path).convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    year_box = pygame.Rect(int(WIDTH * (3 / 4)) - input_width // 2, 30, input_width, input_height)
    submit_button = pygame.Rect(885, 270, button_width, button_height)
    return_button = pygame.Rect(245, 600, button_width, button_height)

    year_text = ""
    error_message = ""
    active_box = None
    dropdown_visible = False
    maps_dropdown = None

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if year_box.collidepoint(event.pos) and not dropdown_visible:
                    active_box = "year"
                elif submit_button.collidepoint(event.pos):
                    if year_text:
                        if not dropdown_visible:
                            try:
                                session = ff1.get_event_schedule(int(year_text))
                                events = session["EventName"].tolist()

                                if int(year_text) > 2019:
                                    countries = [i for i in events if "pre-season" not in i.lower()]
                                else:
                                    countries = events

                                dropdown_visible = True
                                error_message = ""

                                maps_dropdown = Dropdown(
                                    screen, 685, 90, 550, 25, name='Select Grand Prix',
                                    choices=countries, fontSize=25, borderRadius=5, textHAlign='centre',
                                    colour=pygame.Color('gray'), values=countries, direction='down'
                                )
                            except ValueError:
                                error_message = "Please enter a valid year."
                        elif dropdown_visible and maps_dropdown:
                            if maps_dropdown.getSelected() is not None:
                                error_message = plot_map()
                            else:
                                error_message = "Please select a GP."
                    else:
                        error_message = "Please enter a year."

                elif return_button.collidepoint(event.pos):
                    if maps_dropdown:
                        maps_dropdown.toggleDropped() if maps_dropdown.isDropped() else ...
                        maps_dropdown.hide()
                    return
            elif event.type == pygame.KEYDOWN:
                if active_box == "year":
                    if event.key == pygame.K_BACKSPACE:
                        year_text = year_text[:-1]
                    else:
                        year_text += event.unicode

        draw_image(screen, bg_image, 0, 0)
        draw_image(screen, logo_image, WIDTH // 4, logo_image.get_height() - 30, center=True)
        draw_text(screen, "View Maps", 80, WHITE, WIDTH // 4, logo_image.get_height() + 40, center=True)
        pygame.draw.rect(screen, RED, return_button, border_radius=5)
        pygame.draw.rect(screen, LIGHT_GRAY, year_box, border_radius=5)
        pygame.draw.rect(screen, RED, submit_button, border_radius=5)
        draw_text(screen, "Return to Menu", 24, WHITE, return_button.centerx, return_button.centery, center=True)
        draw_text(screen, "Year", 24, WHITE, year_box.centerx, year_box.centery - 35, center=True)
        draw_text(screen, year_text, 24, BLACK, year_box.centerx, year_box.centery, center=True)

        description_lines = [
            "Welcome to the View Maps page. As the name suggests, you can view the map",
            "of a race track of a certain year. But that's not all. This is an interactable feature,",
            "which means you can move around on the map.",
            " ",
            "The map includes numbered corners which are different for each track.",
            " ",
            "Enter the desired year and click 'Load' to get a list of available races.",
            "Select a Grand Prix from the dropdown menu and click 'View Map'.",
            " ",
            "NOTE: It may take ~30 to 45 seconds for the map to load.We'll try to make",
            "this faster in the future :)"
        ]
        current_height = 250

        for i, line in enumerate(description_lines):
            if line == " ":
                current_height += 15
            else:
                draw_text(screen, line, 24, WHITE if i < 9 else RED, 45, current_height, center=False)
                current_height += 30

        draw_text(screen, "Load" if not dropdown_visible else "View Maps", 24, WHITE, submit_button.centerx,
                  submit_button.centery, center=True)

        if error_message:
            draw_text(screen, error_message, 30, RED, int(WIDTH * (3 / 4)), 240, center=True)

        pygame_widgets.update(events)
        pygame.display.flip()
