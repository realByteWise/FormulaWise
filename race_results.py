import sys
import pygame_widgets
import matplotlib.pyplot as plt
import fastf1.plotting
from resources import *
from pygame_widgets.dropdown import Dropdown


def plot_positions():
    fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')
    try:
        session = ff1.get_session(int(year_text), positions_dropdown.getSelected(), 'R')
        session.load(telemetry=False, weather=False, messages=False)
        fig, ax = plt.subplots(figsize=(8.0, 4.9))

        for drv in session.drivers:
            try:
                drv_laps = session.laps.pick_drivers(drv)
                abb = drv_laps['Driver'].iloc[0]
                style = fastf1.plotting.get_driver_style(identifier=abb, style=['color', 'linestyle'], session=session)
                ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=abb, **style)
            except IndexError:
                continue

        ax.set_ylim([20.5, 0.5])
        ax.set_yticks([1, 5, 10, 15, 20])
        ax.set_xlabel('Lap')
        ax.set_ylabel('Position')
        ax.legend(bbox_to_anchor=(1.0, 1.02))
        plt.tight_layout()
        plt.show()
    except (ValueError, IndexError) as e:
        print(f"Error: {e}")  # Debugging
        return "Error fetching data. Please try again."
    return "Please check the loaded window for the data."

def show_positions(screen, current_bg_image_path):
    global year_text, positions_dropdown
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
    positions_dropdown = None

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

                                positions_dropdown = Dropdown(
                                    screen, 685, 90, 550, 25, name='Select Grand Prix',
                                    choices=countries, fontSize=25, borderRadius=5, textHAlign='centre',
                                    colour=pygame.Color('gray'), values=countries, direction='down'
                                )
                            except ValueError:
                                error_message = "Please enter a valid year."
                        elif dropdown_visible and positions_dropdown:
                            if positions_dropdown.getSelected() is not None:
                                error_message = plot_positions()
                            else:
                                error_message = "Please select a GP."
                    else:
                        error_message = "Please enter a year."

                elif return_button.collidepoint(event.pos):
                    if positions_dropdown:
                        positions_dropdown.toggleDropped() if positions_dropdown.isDropped() else ...
                        positions_dropdown.hide()
                    return

            elif event.type == pygame.KEYDOWN:
                if active_box == "year":
                    if event.key == pygame.K_BACKSPACE:
                        year_text = year_text[:-1]
                    else:
                        year_text += event.unicode

        draw_image(screen, bg_image, 0, 0)
        draw_image(screen, logo_image, WIDTH // 4, logo_image.get_height() - 30, center=True)
        draw_text(screen, "Race Results", 80, WHITE, WIDTH // 4, logo_image.get_height() + 40, center=True)
        pygame.draw.rect(screen, RED, return_button, border_radius=5)
        pygame.draw.rect(screen, LIGHT_GRAY, year_box, border_radius=5)
        pygame.draw.rect(screen, RED, submit_button, border_radius=5)
        draw_text(screen, "Return to Menu", 24, WHITE, return_button.centerx, return_button.centery, center=True)
        draw_text(screen, "Year", 24, WHITE, year_box.centerx, year_box.centery - 35, center=True)
        draw_text(screen, year_text, 24, BLACK, year_box.centerx, year_box.centery, center=True)

        description_lines = [
            "Welcome to the Race Results page. This feature lets you view the results of",
            "the selected race of a year. An interactive window pops up where you can",
            "see a graph indicating what position each driver was on in the whole race.",
            "The graph also has crash / retirement data ( hence the sudden line cuts ).",
            " ",
            "Simply enter the desired year and click 'Load' to see the available races.",
            "Select a Grand Prix from the dropdown menu and click 'View Results' to",
            "view a detailed graph of the race.",
            " ",
            "Explore historical data to analyze past performances and trends. This",
            "feature is perfect for fans wanting to revisit memorable races. Stay",
            "updated with the latest statistics and records from previous seasons.",
            " ",
            "NOTE: It may take ~30 to 45 seconds for data to load if not saved in cache."
        ]
        current_height = 200

        for i, line in enumerate(description_lines):
            if line == " ":
                current_height += 15
            else:
                draw_text(screen, line, 24, WHITE if i != 13 else RED, 45, current_height, center=False)
                current_height += 30

        draw_text(screen, "Load" if not dropdown_visible else "View Results", 24, WHITE, submit_button.centerx,
                  submit_button.centery, center=True)

        if error_message:
            draw_text(screen, error_message, 30, RED, int(WIDTH * (3 / 4)), 240, center=True)

        pygame_widgets.update(events)
        pygame.display.flip()
