import sys
import matplotlib as mpl
import numpy as np
from resources import *
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

def heatmaps(screen):
    global driver_text, year_text, week_text, active_box, error_message
    bg_image = pygame.image.load(bg_image_path).convert()
    input_width, input_height = 300, 40
    driver_box = pygame.Rect(WIDTH // 2 - input_width // 2, HEIGHT // 2 - 100, input_width, input_height)
    year_box = pygame.Rect(WIDTH // 2 - input_width // 2, HEIGHT // 2 - 30, input_width, input_height)
    week_box = pygame.Rect(WIDTH // 2 - input_width // 2, HEIGHT // 2 + 40, input_width, input_height)
    submit_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 100, 150, 50)
    return_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 160, 150, 50)

    driver_text = ""
    year_text = ""
    week_text = ""
    active_box = None
    error_message = ""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if driver_box.collidepoint(event.pos):
                    active_box = "driver"
                elif year_box.collidepoint(event.pos):
                    active_box = "year"
                elif week_box.collidepoint(event.pos):
                    active_box = "week"
                elif submit_button.collidepoint(event.pos):
                    if driver_text and year_text and week_text:
                        if plot_heatmap(driver_text, int(year_text), int(week_text)):
                            driver_text, year_text, week_text = "", "", ""
                        else:
                            error_message = "Invalid input. Please try again."
                    else:
                        error_message = "Please fill all fields."
                elif return_button.collidepoint(event.pos):
                    return  

            if event.type == pygame.KEYDOWN:
                if active_box == "driver":
                    if event.key == pygame.K_BACKSPACE:
                        driver_text = driver_text[:-1]
                    else:
                        driver_text += event.unicode
                elif active_box == "year":
                    if event.key == pygame.K_BACKSPACE:
                        year_text = year_text[:-1]
                    else:
                        year_text += event.unicode
                elif active_box == "week":
                    if event.key == pygame.K_BACKSPACE:
                        week_text = week_text[:-1]
                    else:
                        week_text += event.unicode

        # Drawing the plot
        
        pygame.draw.rect(screen, LIGHT_GRAY, driver_box)
        pygame.draw.rect(screen, LIGHT_GRAY, year_box)
        pygame.draw.rect(screen, LIGHT_GRAY, week_box)
        pygame.draw.rect(screen, RED, submit_button)
        pygame.draw.rect(screen, RED, return_button)

        draw_text(screen,"Driver", 24, WHITE, driver_box.centerx, driver_box.centery - 40, center=True)
        draw_text(screen,"Year", 24, WHITE, year_box.centerx, year_box.centery - 35, center=True)
        draw_text(screen,"Week", 24, WHITE, week_box.centerx, week_box.centery - 35, center=True)
        draw_text(screen,"Submit", 24, WHITE, submit_button.centerx, submit_button.centery, center=True)
        draw_text(screen,"Return to Menu", 24, WHITE, return_button.centerx, return_button.centery, center=True)

        draw_text(screen,driver_text, 24, BLACK, driver_box.centerx, driver_box.centery, center=True)
        draw_text(screen,year_text, 24, BLACK, year_box.centerx, year_box.centery, center=True)
        draw_text(screen,week_text, 24, BLACK, week_box.centerx, week_box.centery, center=True)

        if error_message:
            draw_text(screen,error_message, 20, RED, WIDTH // 2, HEIGHT // 2 + 200, center=True)

        pygame.display.flip()

def plot_heatmap(driver, year, week):
    try:
        session = ff1.get_session(year, week, 'R')
        session.load()
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
    except Exception as e: # Debugging
        print(f"Error: {e}")
        return False
    return True
