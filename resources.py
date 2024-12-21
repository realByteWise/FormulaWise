import pygame
import os
import fastf1 as ff1
from time import sleep
from datetime import datetime

# Creating cache directory if it doesn't exist
permission = True
try:
    os.mkdir("cache")
except FileExistsError:
    pass
except PermissionError:
    permission = False
    print("No permission.\nDefault cache directory: C:\\Users\\...\\AppData\\Local\\Temp\\fastf1")
else:
    print("Cache directory successfully created.")
    sleep(5)  # Waiting for directory to be created

if permission:
    ff1.Cache.enable_cache("cache")

try:
    with open("credentials.txt", "x"):
        pass
except FileExistsError:
    pass
else:
    print("credentials.txt successfully created.")

# Variables
WIDTH = 1280
HEIGHT = 720
logo_width = 500
logo_height = 100
logo_image_path = "assets/fwise.png"

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (211, 211, 211)
GOLD = (255, 215, 0)
SILVER = (128, 128, 128)
BRONZE = (205, 127, 50)

gp_info = {'Australian Grand Prix': [datetime(2025, 3, 16), "assets/maps/australian-gp.png", "https://tickets.formula1.com/en/f1-3159-australia?_gl=1*1nu3ilq*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Chinese Grand Prix': [datetime(2025, 3, 23), "assets/maps/chinese-gp.jpg", "https://tickets.formula1.com/en/f1-3182-china?_gl=1*wg4daf*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Japanese Grand Prix': [datetime(2025, 4, 6), "assets/maps/japanese-gp.jpg", "https://tickets.formula1.com/en/f1-3309-japan?_gl=1*198wqvz*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Bahrain Grand Prix': [datetime(2025, 4, 13), "assets/maps/bahrain-gp.jpg", "https://tickets.formula1.com/en/f1-3176-bahrain?_gl=1*198wqvz*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Saudi Arabian Grand Prix': [datetime(2025, 4, 20), "assets/maps/saudi-gp.jpeg", "https://tickets.formula1.com/en/f1-54298-saudi-arabia?_gl=1*198wqvz*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Miami Grand Prix': [datetime(2025, 5, 4), "assets/maps/miami-gp.jpg", "https://tickets.formula1.com/en/f1-54987-miami?_gl=1*1sp5is4*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Emilia Romagna Grand Prix': [datetime(2025, 5, 18), "assets/maps/imola-gp.jpg", "https://tickets.formula1.com/en/f1-53107-imola?_gl=1*1sp5is4*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Monaco Grand Prix': [datetime(2025, 5, 25), "assets/maps/monaco-gp.jpg", "https://tickets.formula1.com/en/f1-3202-monaco?_gl=1*hfdszw*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Spanish Grand Prix': [datetime(2025, 6, 1), "assets/maps/spanish-gp.jpg", "https://tickets.formula1.com/en/f1-3190-spain?_gl=1*hfdszw*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Canadian Grand Prix': [datetime(2025, 6, 15), "assets/maps/canadian-gp.jpg", "https://tickets.formula1.com/en/f1-3215-canada?_gl=1*hfdszw*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Austrian Grand Prix': [datetime(2025, 6, 29), "assets/maps/austrian-gp.jpg", "https://tickets.formula1.com/en/f1-3222-austria?_gl=1*17q81wl*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'British Grand Prix': [datetime(2025, 7, 6), "assets/maps/british-gp.jpg", "https://tickets.formula1.com/en/f1-3226-great-britain?_gl=1*17q81wl*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Belgian Grand Prix': [datetime(2025, 7, 27), "assets/maps/belgian-gp.jpg", "https://tickets.formula1.com/en/f1-3286-belgium?_gl=1*knywvx*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Hungarian Grand Prix': [datetime(2025, 8, 3), "assets/maps/hungarian-gp.jpg", "https://tickets.formula1.com/en/f1-3277-hungary?_gl=1*knywvx*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Dutch Grand Prix': [datetime(2025, 8, 31), "assets/maps/dutch-gp.jpg", "https://tickets.formula1.com/en/f1-42837-netherlands?_gl=1*knywvx*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Italian Grand Prix': [datetime(2025, 9, 7), "assets/maps/monza-gp.jpg", "https://tickets.formula1.com/en/f1-3293-italy?_gl=1*2qtm43*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Azerbaijan Grand Prix': [datetime(2025, 9, 21), "assets/maps/baku-gp.jpg", "https://tickets.formula1.com/en/f1-10851-azerbaijan?_gl=1*2qtm43*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Singapore Grand Prix': [datetime(2025, 10, 5), "assets/maps/singapore-gp.jpg", "https://tickets.formula1.com/en/f1-3301-singapore?_gl=1*1plqlbf*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'United States Grand Prix': [datetime(2025, 10, 19), "assets/maps/austin-gp.jpg", "https://tickets.formula1.com/en/f1-3320-united-states?_gl=1*1plqlbf*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Mexico City Grand Prix': [datetime(2025, 10, 26), "assets/maps/mexico-gp.jpg", "https://tickets.formula1.com/en/f1-4861-mexico?_gl=1*1plqlbf*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'São Paulo Grand Prix': [datetime(2025, 11, 9), "assets/maps/brazilian-gp.jpg", "https://tickets.formula1.com/en/f1-3325-brazil?_gl=1*1plqlbf*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Las Vegas Grand Prix': [datetime(2025, 11, 22), "assets/maps/las-vegas-gp.jpg", "https://tickets.formula1.com/en/f1-59007-las-vegas?_gl=1*1ct9pq4*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Qatar Grand Prix': [datetime(2025, 11, 30), "assets/maps/qatar-gp.jpg", "https://tickets.formula1.com/en/f1-56257-qatar?_gl=1*1ct9pq4*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"],
           'Abu Dhabi Grand Prix': [datetime(2025, 12, 7), "assets/maps/abu-dhabi-gp.jpg", "https://tickets.formula1.com/en/f1-3312-abu-dhabi?_gl=1*1ct9pq4*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"]}

# Functions
def draw_text(screen, text, size, color, x, y, center=False):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def load_credentials():
    credentials = {}
    try:
        with open("credentials.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(":")
                    if len(parts) == 2:
                        username, password = parts
                        credentials[username] = password
                    else:
                        print(f"Skipping malformed line: {line}")
    except FileNotFoundError:
        print("Credentials file not found.")
    return credentials

def save_credentials(username, password):
    with open("credentials.txt", "a") as file:
        file.write(f"{username}:{password}\n")
