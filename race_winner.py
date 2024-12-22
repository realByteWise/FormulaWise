import sys
import pygame
import pygame_widgets
from resources import *
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import matplotlib.pyplot as plt
import fastf1.plotting


def show_podium(screen, current_bg_image_path):
    global year_text, active_box, error_message, dropdown, button
    logo_image = pygame.image.load(logo_image_path)
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    bg_image_path = current_bg_image_path
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
    dropdown = None
    button = None
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
                            if countries[0] == "Pre-Season Testing":
                                countries.remove("Pre-Season Testing")
                            dropdown_visible = True
                            dropdown = Dropdown(
                                screen, 685, 50, 550, 25, name='Select Grand Prix',
                                choices=countries, fontSize=25,
                                borderRadius=5, colour=pygame.Color('gray'), values=countries, direction='down',
                                textHAlign='centre', textColor=pygame.Color('Red')
                            )

                            button = Button(
                                screen, 900, 330, 150, 50, text='Submit',
                                margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
                                radius=5, onClick=position,
                                font=pygame.font.SysFont(pygame.font.match_font('Palatino'), 25),
                                textVAlign='center'
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

        screen.blit(bg_image, (0, 0))

        if not dropdown_visible:
            screen.blit(logo_image, (WIDTH // 2 - logo_image.get_width() // 2, 20))
            draw_text(screen, "Race Results", 100, WHITE, 400, logo_image.get_height() + 10, center=False)
            pygame.draw.rect(screen, RED, return_button)
            draw_text(screen, "Return to Menu", 24, WHITE, return_button.centerx, return_button.centery, center=True)
            pygame.draw.rect(screen, LIGHT_GRAY, year_box)
            pygame.draw.rect(screen, RED, submit_button)
            draw_text(screen, "Year", 24, WHITE, year_box.centerx, year_box.centery - 35, center=True)
            draw_text(screen, "Submit", 24, WHITE, submit_button.centerx, submit_button.centery, center=True)
            draw_text(screen, year_text, 24, BLACK, year_box.centerx, year_box.centery, center=True)

            if error_message:
                draw_text(screen, error_message, 20, RED, WIDTH // 2, HEIGHT // 2 + 100, center=True)
        else:
            screen.blit(logo_image, (70, 20))
            title_text = "Race Results"
            draw_text(screen, title_text, 100, WHITE, 75, logo_image.get_height() + 10, center=False)
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
            pygame.draw.rect(screen, RED, pygame.Rect(150, 550, 150, 50))
            draw_text(screen, "Return to Menu", 24, WHITE, 225, 575, center=True)

            if dropdown:
                dropdown.draw()
            if button:
                button.draw()
            pygame_widgets.update(events)

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.pos:
                    if return_button.collidepoint(event.pos):
                        return

        pygame.display.flip()


def position():
    fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')
    try:
        session = ff1.get_session(int(year_text), dropdown.getSelected(), 'R')
        session.load(telemetry=False, weather=False)

        fig, ax = plt.subplots(figsize=(8.0, 4.9))
        for drv in session.drivers:
            try:
                drv_laps = session.laps.pick_drivers(drv)

                abb = drv_laps['Driver'].iloc[0]
                style = fastf1.plotting.get_driver_style(identifier=abb, style=['color', 'linestyle'], session=session)

                ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=abb, **style)
            except Exception:
                continue

        ax.set_ylim([20.5, 0.5])
        ax.set_yticks([1, 5, 10, 15, 20])
        ax.set_xlabel('Lap')
        ax.set_ylabel('Position')
        ax.legend(bbox_to_anchor=(1.0, 1.02))
        plt.figure("Race Results")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error: {e}")  # Debugging
