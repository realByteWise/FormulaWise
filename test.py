import fastf1 as ff1
import pygame_widgets
import pygame
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import numpy as np
import matplotlib.pyplot as plt
ff1.Cache.enable_cache("cache")
pygame.init()
screen = pygame.display.set_mode((1280, 720))
session = ff1.get_event_schedule(2024)
countries = session["EventName"].tolist()
countries.remove("Pre-Season Testing")
dropdown = Dropdown(
    screen, 1050, 80, 200, 25, name='Select GP', choices=countries, fontSize=15, borderRadius=5,
    colour=pygame.Color('gray'), values=countries, direction='down', textHAlign='centre',textColor=pygame.Color('Red'),
)

def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

def plot_map():
    session = ff1.get_session(2024, dropdown.getSelected(), 'R')
    session.load()

    lap = session.laps.pick_fastest()
    pos = lap.get_pos_data()

    circuit_info = session.get_circuit_info()
    
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
        plt.scatter(text_x, text_y, color='grey', s=140)

        # Draw a line from the track to this circle.
        plt.plot([track_x, text_x], [track_y, text_y], color='grey')

        # Finally, print the corner number inside the circle.
        plt.text(text_x, text_y, txt,
                 va='center_baseline', ha='center', size='small', color='white')
    
    plt.title(session.event['Location'])
    plt.xticks([])
    plt.yticks([])
    plt.axis('equal')
    plt.show()    

def print_value():
    print(dropdown.getSelected(), 2025)

button = Button(
    screen, 10, 10, 100, 50, text='Print Value', fontSize=30,
    margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
      font=pygame.font.SysFont('calibri', 10),
    textVAlign='bottom', onClick=plot_map
)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
    screen.fill(pygame.Color('black'))
    pygame_widgets.update(events)
    pygame.display.update()
