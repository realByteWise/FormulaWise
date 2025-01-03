import sys
import matplotlib as mpl
import numpy as np
import fastf1.plotting
import pygame_widgets
from resources import *
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from pygame_widgets.dropdown import Dropdown


def plot_heatmap(driver, year, gp):
    fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')
    try:
        session = ff1.get_session(year, gp, 'R')
        session.load(weather=False, messages=False)
        lap = session.laps.pick_drivers(driver).pick_fastest()
        x = lap.telemetry['X']
        y = lap.telemetry['Y']
        color = lap.telemetry['Speed']
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        fig, ax = plt.subplots(figsize=(12, 6.75))
        fig.suptitle(f'{session.event.name} {year} - {driver} - Speed', size=24, y=0.97)
        ax.axis('off')
        ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)
        norm = plt.Normalize(color.min(), color.max())
        lc = LineCollection(segments, cmap=mpl.cm.plasma, norm=norm, linestyle='-', linewidth=5)
        lc.set_array(color)
        ax.add_collection(lc)
        cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
        normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
        mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=mpl.cm.plasma, orientation="horizontal")
        plt.show()
    except Exception as e:
        print(f"Error: {e}")  # Debugging
        return "Error fetching data. Please try again."
    return "Please check the loaded window for the data."

def heatmaps(screen,current_bg_image_path):
    bg_image = pygame.image.load(current_bg_image_path).convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    logo_image = pygame.image.load(logo_image_path)
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    year_box = pygame.Rect(int(WIDTH * (3 / 4)) - input_width // 2, 30, input_width, input_height)
    submit_button = pygame.Rect(885, 270, button_width, button_height)
    return_button = pygame.Rect(245, 600, button_width, button_height)
    return_prev_button = pygame.Rect(855, 340, 210, button_height)

    year_text = ""
    error_message = ""
    active_box = None
    gp_dropdown = None
    drivers_dropdown = None
    stage = 1

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if year_box.collidepoint(event.pos) and stage == 1:
                    active_box = "year"
                elif submit_button.collidepoint(event.pos):
                    if year_text:
                        if stage == 1:
                            try:
                                session = ff1.get_event_schedule(int(year_text))
                                events = session["EventName"].tolist()

                                if int(year_text) > 2019:
                                    countries = [i for i in events if "pre-season" not in i.lower()]
                                else:
                                    countries = events

                                error_message = ""
                                stage = 2

                                gp_dropdown = Dropdown(
                                    screen, 685, 90, 550, 25, name='Select Grand Prix',
                                    choices=countries, fontSize=25, borderRadius=5, textHAlign='centre',
                                    colour=pygame.Color('gray'), values=countries, direction='down'
                                )
                            except ValueError:
                                error_message = "Please enter a valid year."

                        elif stage == 2 and gp_dropdown:
                            if gp_dropdown.getSelected() is not None:
                                try:
                                    session = ff1.get_session(int(year_text), gp_dropdown.getSelected(), 'R')
                                    session.load(laps=False, weather=False, messages=False)
                                    drivers = [driver for driver in session.results['Abbreviation']]

                                    gp_dropdown.toggleDropped() if gp_dropdown.isDropped() else ...
                                    gp_dropdown.hide()
                                    stage = 3
                                    error_message = ""

                                    drivers_dropdown = Dropdown(
                                        screen, 850, 20, 220, 27, name='Select Driver',
                                        choices=drivers, fontSize=25, borderRadius=5, textHAlign='centre',
                                        colour=pygame.Color('gray'), values=drivers, direction='down'
                                    )
                                except ValueError:
                                    error_message = "Error fetching data. Please try again."
                            else:
                                error_message = "Please select a Grand Prix."

                        elif stage == 3 and drivers_dropdown:
                            if drivers_dropdown.getSelected() is not None:
                                error_message =  plot_heatmap(drivers_dropdown.getSelected(), int(year_text), gp_dropdown.getSelected())
                            else:
                                error_message = "Please select a Driver."
                    else:
                        error_message = "Please enter year."
                elif return_prev_button.collidepoint(event.pos):
                    if drivers_dropdown:
                        drivers_dropdown.toggleDropped() if drivers_dropdown.isDropped() else ...
                        drivers_dropdown.hide()
                    stage = 1
                    error_message = ""
                elif return_button.collidepoint(event.pos):
                    if gp_dropdown:
                        gp_dropdown.toggleDropped() if gp_dropdown.isDropped() else ...
                        gp_dropdown.hide()
                    if drivers_dropdown:
                        drivers_dropdown.toggleDropped() if drivers_dropdown.isDropped() else ...
                        drivers_dropdown.hide()
                    return

            if event.type == pygame.KEYDOWN:
                if active_box == "year":
                    if event.key == pygame.K_BACKSPACE:
                        year_text = year_text[:-1]
                    else:
                        year_text += event.unicode

        draw_image(screen, bg_image, 0, 0)
        draw_image(screen, logo_image, WIDTH // 4, logo_image.get_height() - 30, center=True)
        draw_text(screen, "Heatmaps", 80, WHITE, WIDTH // 4, logo_image.get_height() + 40, center=True)

        description_lines = [
            "Welcome to the Heatmaps page. This feature lets you view a heatmap of a",
            "driver in a Grand Prix in of a year entered. A heatmap is a color-based",
            "speed graph, which means a color on a part of the map depending on the",
            "speed at which the driver was driving.",
            " ",
            "There is also a legend on the bottom of the graph, showing a certain color",
            "for that speed. In short: Blue means slower, Yellow means faster.",
            " ",
            "Enter the desired year and click 'Load' to see the available races.",
            "Select a Grand Prix from the dropdown menu to view detailed results.",
            " ",
            "Explore historical data to analyze past performances and trends. This",
            "feature is perfect for fans wanting to revisit memorable races.",
            " ",
            "NOTE: It may take ~30 to 45 seconds for data to load if not saved in cache."
        ]
        current_height = 200

        for i, line in enumerate(description_lines):
            if line == " ":
                current_height += 15
            else:
                draw_text(screen, line, 24, WHITE if i != 14 else RED, 45, current_height, center=False)
                current_height += 30

        pygame.draw.rect(screen, RED, return_button, border_radius=5)
        pygame.draw.rect(screen, RED, submit_button, border_radius=5)
        draw_text(screen, "Return to Menu", 24, WHITE, return_button.centerx, return_button.centery, center=True)

        if stage == 3:
            pygame.draw.rect(screen, RED, return_prev_button, border_radius=5)
            draw_text(screen, "View Heatmap", 24, WHITE, submit_button.centerx, submit_button.centery, center=True)
            draw_text(screen, "Return to Previous Menu", 24, WHITE, return_prev_button.centerx, return_prev_button.centery, center=True)
        else:
            pygame.draw.rect(screen, LIGHT_GRAY, year_box, border_radius=5)
            draw_text(screen, "Year", 24, WHITE, year_box.centerx, year_box.centery - 30, center=True)
            draw_text(screen, year_text, 24, BLACK, year_box.centerx, year_box.centery, center=True)
            draw_text(screen, "Load" if stage == 1 else "Submit", 24, WHITE, submit_button.centerx, submit_button.centery, center=True)

        if error_message:
            draw_text(screen,error_message, 30, RED, int(WIDTH * (3 / 4)), 240, center=True)

        pygame_widgets.update(events)
        pygame.display.flip()
