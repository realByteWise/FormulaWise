import pygame
import os
import fastf1 as ff1
from time import sleep
from datetime import datetime
from dateutil import parser


# Creating cache directory if it doesn't exist
permission = True
try:
    os.mkdir("cache")
except FileExistsError:
    pass
except PermissionError:
    permission = False
    print("LOG: No permission.\nDefault cache directory: C:\\Users\\...\\AppData\\Local\\Temp\\fastf1")
else:
    print("LOG: Cache directory successfully created.")
    sleep(5)  # Waiting for directory to be created

if permission:
    ff1.Cache.enable_cache("cache")

# creating credentials file if it doesn't exist
try:
    with open("credentials.txt", "x"):
        pass
except FileExistsError:
    pass
else:
    print("LOG: credentials.txt successfully created.")

# creating preferences file if it doesn't exist
try:
    open("preferences.txt", "x")
    with open("preferences.txt", "w") as file:
        file.write("True,0,1.0,2023-10-03,1:1")  # default preferences
except FileExistsError:
    pass
else:
    print("LOG: preferences.txt successfully created.")

# variables
WIDTH = 1280
HEIGHT = 720
logo_width = 500
logo_height = 100
button_width = 150
button_height = 50
input_width = 300
input_height = 40
logo_image_path = "assets/fwise.png"

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (211, 211, 211)

gp_info_2025 = {
    'Australian Grand Prix': (datetime(2025, 3, 16), "assets/maps/australian-gp.jpg", "https://tickets.formula1.com/en/f1-3159-australia?_gl=1*1nu3ilq*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Chinese Grand Prix': (datetime(2025, 3, 23), "assets/maps/chinese-gp.jpg", "https://tickets.formula1.com/en/f1-3182-china?_gl=1*wg4daf*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Japanese Grand Prix': (datetime(2025, 4, 6), "assets/maps/japanese-gp.jpg", "https://tickets.formula1.com/en/f1-3309-japan?_gl=1*198wqvz*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Bahrain Grand Prix': (datetime(2025, 4, 13), "assets/maps/bahrain-gp.jpg", "https://tickets.formula1.com/en/f1-3176-bahrain?_gl=1*198wqvz*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Saudi Arabian Grand Prix': (datetime(2025, 4, 20), "assets/maps/saudi-gp.jpg", "https://tickets.formula1.com/en/f1-54298-saudi-arabia?_gl=1*198wqvz*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Miami Grand Prix': (datetime(2025, 5, 4), "assets/maps/miami-gp.jpg", "https://tickets.formula1.com/en/f1-54987-miami?_gl=1*1sp5is4*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Emilia Romagna Grand Prix': (datetime(2025, 5, 18), "assets/maps/imola-gp.jpg", "https://tickets.formula1.com/en/f1-53107-imola?_gl=1*1sp5is4*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Monaco Grand Prix': (datetime(2025, 5, 25), "assets/maps/monaco-gp.jpg", "https://tickets.formula1.com/en/f1-3202-monaco?_gl=1*hfdszw*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Spanish Grand Prix': (datetime(2025, 6, 1), "assets/maps/spanish-gp.jpg", "https://tickets.formula1.com/en/f1-3190-spain?_gl=1*hfdszw*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Canadian Grand Prix': (datetime(2025, 6, 15), "assets/maps/canadian-gp.jpg", "https://tickets.formula1.com/en/f1-3215-canada?_gl=1*hfdszw*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Austrian Grand Prix': (datetime(2025, 6, 29), "assets/maps/austrian-gp.jpg", "https://tickets.formula1.com/en/f1-3222-austria?_gl=1*17q81wl*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'British Grand Prix': (datetime(2025, 7, 6), "assets/maps/british-gp.jpg", "https://tickets.formula1.com/en/f1-3226-great-britain?_gl=1*17q81wl*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Belgian Grand Prix': (datetime(2025, 7, 27), "assets/maps/belgian-gp.jpg", "https://tickets.formula1.com/en/f1-3286-belgium?_gl=1*knywvx*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Hungarian Grand Prix': (datetime(2025, 8, 3), "assets/maps/hungarian-gp.jpg", "https://tickets.formula1.com/en/f1-3277-hungary?_gl=1*knywvx*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Dutch Grand Prix': (datetime(2025, 8, 31), "assets/maps/dutch-gp.jpg", "https://tickets.formula1.com/en/f1-42837-netherlands?_gl=1*knywvx*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Italian Grand Prix': (datetime(2025, 9, 7), "assets/maps/monza-gp.jpg", "https://tickets.formula1.com/en/f1-3293-italy?_gl=1*2qtm43*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Azerbaijan Grand Prix': (datetime(2025, 9, 21), "assets/maps/baku-gp.jpg", "https://tickets.formula1.com/en/f1-10851-azerbaijan?_gl=1*2qtm43*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Singapore Grand Prix': (datetime(2025, 10, 5), "assets/maps/singapore-gp.jpg", "https://tickets.formula1.com/en/f1-3301-singapore?_gl=1*1plqlbf*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'United States Grand Prix': (datetime(2025, 10, 19), "assets/maps/austin-gp.jpg", "https://tickets.formula1.com/en/f1-3320-united-states?_gl=1*1plqlbf*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Mexico City Grand Prix': (datetime(2025, 10, 26), "assets/maps/mexican-gp.jpg", "https://tickets.formula1.com/en/f1-4861-mexico?_gl=1*1plqlbf*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'São Paulo Grand Prix': (datetime(2025, 11, 9), "assets/maps/brazilian-gp.jpg", "https://tickets.formula1.com/en/f1-3325-brazil?_gl=1*1plqlbf*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Las Vegas Grand Prix': (datetime(2025, 11, 22), "assets/maps/las-vegas-gp.jpg", "https://tickets.formula1.com/en/f1-59007-las-vegas?_gl=1*1ct9pq4*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Qatar Grand Prix': (datetime(2025, 11, 30), "assets/maps/qatar-gp.jpg", "https://tickets.formula1.com/en/f1-56257-qatar?_gl=1*1ct9pq4*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE"),
    'Abu Dhabi Grand Prix': (datetime(2025, 12, 7), "assets/maps/abu-dhabi-gp.jpg", "https://tickets.formula1.com/en/f1-3312-abu-dhabi?_gl=1*1ct9pq4*_up*MQ..*_gs*MQ..&gclid=CjwKCAiAgoq7BhBxEiwAVcW0LOWPx0O_wrn_lEDtiJtCYXxbMiJ8jdXDXZlrKPPBzaSuaq-ttZz2kRoCAxkQAvD_BwE")
}

themes = [
    ('assets/music/gas.mp3', 'assets/bgs/main.jpg'),
    ('assets/music/krimuh.mp3', 'assets/bgs/krimuh.jpg'),
    ('assets/music/sigma.mp3', 'assets/bgs/sigma.jpg'),
    ('assets/music/chill.mp3', 'assets/bgs/chill.jpg'),
    ('assets/music/lifeforce.mp3', 'assets/bgs/lifeforce.jpg')
]

special_keys = (pygame.K_ESCAPE, pygame.K_DELETE, pygame.K_TAB, pygame.K_CAPSLOCK,
                pygame.K_KP_ENTER, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LCTRL,
                pygame.K_LALT, pygame.K_RALT, pygame.K_RCTRL, pygame.K_UP, pygame.K_DOWN,
                pygame.K_LEFT, pygame.K_RIGHT, pygame.K_HOME, pygame.K_END, pygame.K_PAGEUP,
                pygame.K_PAGEDOWN, pygame.K_NUMLOCK, pygame.K_NUMLOCKCLEAR, pygame.K_KP_ENTER,
                pygame.K_RETURN, pygame.K_PRINTSCREEN, pygame.K_F1, pygame.K_F2, pygame.K_F3,
                pygame.K_F4, pygame.K_F5, pygame.K_F6, pygame.K_F7, pygame.K_F8, pygame.K_F9,
                pygame.K_F10, pygame.K_F11, pygame.K_F12, pygame.K_F13, pygame.K_F14, pygame.K_F15)

# functions
class Button:
    def __init__(self, x, y, image, width, height):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

def draw_text(screen, text, size, color, x, y, center=False) -> None:
    font = pygame.font.Font(pygame.font.match_font('Palatino'), size)
    text_surface = font.render(text, True, color)
    if center:
        text_rect = text_surface.get_rect(center=(x, y))
    else:
        text_rect = text_surface.get_rect(topleft=(x, y))
    screen.blit(text_surface, text_rect)

def draw_image(screen, image, x, y, center=False) -> None:
    if center:
        image_rect = image.get_rect(center=(x, y))
    else:
        image_rect = image.get_rect(topleft=(x, y))
    screen.blit(image, image_rect)

def load_credentials() -> dict:
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
                        print(f"LOG: Skipping malformed line: {line}")
    except FileNotFoundError:
        print("LOG: Credentials file not found.")
    return credentials

def save_credentials(username: str, password: str) -> None:
    with open("credentials.txt", "a") as file:
        file.write(f"{username}:{password}\n")

def edit_credentials(old_user: str, password: str, new_user: str | None = None) -> None:
    credentials = {}
    with open("credentials.txt", "r") as read:
        for line in read.readlines():
            line = line.strip()
            if line:
                parts = line.split(":")
                if len(parts) == 2:
                    if old_user != parts[0]:
                        credentials[parts[0]] = parts[1]
                    else:
                        if new_user:
                            credentials[new_user] = password
                        else:
                            credentials[old_user] = password
                else:
                    print(f"LOG: Skipping malformed line: {line}")
    with open("credentials.txt", "w") as write:
        for username, password in credentials.items():
            write.write(f"{username}:{password}\n")

def load_preferences() -> tuple[bool, int, float, datetime, tuple[str, ...]]:
    try:
        with open("preferences.txt", "r") as file:
            line = file.readline().strip()
            if line:
                parts = line.split(",")
                if len(parts) == 5:
                    music_on = bool(parts[0])
                    theme = int(parts[1])
                    volume = float(parts[2])
                    login_date = parser.parse(parts[3])
                    details = tuple(parts[4].split(":"))
                else:
                    print(f"LOG: Skipping malformed line: {line}")
    except FileNotFoundError:
        print("LOG: Preferences file not found.")
    return music_on, theme, volume, login_date, details

def save_preferences(music_on: bool, theme: int, volume: float, login_date: datetime, details: tuple[str, ...]) -> None:
    with open("preferences.txt", "w") as file:
        if details:
            file.write(f"{music_on},{theme},{volume},{login_date.year}-{login_date.month}-{login_date.day},{details[0]}:{details[1]}")
        else:
            file.write(f"{music_on},{theme},{volume},{login_date.year}-{login_date.month}-{login_date.day},1:1")

def password_validator(password: str) -> tuple[bool, str]:
    if len(password) >= 6:
        letter = False
        digit = False
        special = False
        colon = False
        for char in password:
            if char.isalpha(): letter = True
            elif char.isdigit(): digit = True
            elif char == ":": colon = True
            else: special = True
        if colon:
            return False, "Password can't contain ':'"
        elif letter and digit and special:
            return True, ""
        else:
            return False, "Password must contain a letter, a digit and a special character."
    else:
        return False, "Password should be at least 6 characters long."

def username_validator(username: str) -> tuple[bool, str]:
    if 6 <= len(username) <= 30:
        letter = False
        invalid = False
        for char in username:
            if char.isalpha(): letter = True
            elif char.isdigit(): continue
            elif char == ".": continue
            elif char == "_": continue
            else: invalid = True
        if invalid:
            return False, "Username can only use letters, numbers, underscores and periods."
        if not letter:
            return False, "Usernames must contain at least one letter"
        else:
            return True, ""
    else:
        return False, "Username should be 6-30 characters long."

def show_credits():
    print("""
FormulaWise © 2025 by ByteWise (Gleon DSouza & Johan Jose) is licensed under Attribution
-NonCommercial-NoDerivatives 4.0 International.
To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/4.0/

FormulaWise is an independent application dedicated to providing statistics and insights about
Formula 1. However, it is not affiliated with, endorsed by, or associated with Formula 1, the
Fédération Internationale de l'Automobile (FIA), Formula One Management (FOM), or any related entities.

All trademarks, logos, and intellectual property related to Formula 1 are the property of their
respective owners. FormulaWise uses publicly available information to present data and insights
for educational and informational purposes only.
The official website can be found at https://formula1.com.

Other company and product names mentioned herein are trademarks of their respective companies.

Many thanks to the developers of the following Python libraries used in this program:

    fastf1
    pygame
    pygame_widgets
    matplotlib
    numpy
    datetime
    dateutil
    and many more...

Special thanks to the developers of the fastf1 Python library, which has been used in this program.
All Formula 1 Grand Prix data has been acquired from this library, and only converted to a
graphical form for easy viewing. This project would be impossible without fastf1. Certain parts of
the code have been reused.
This code along with the documentation can be found at https://docs.fastf1.dev

THE DATA IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Many thanks to the developers of pygame_widgets. Certain parts of the code have been reused.
This code along with the documentation can be found at https://pygamewidgets.readthedocs.io/en/stable/

Thank you to all those who have, directly or indirectly, lent a helping hand in the successful
completion of this project, with deepest gratitude to Mrs. Maheswari for her valuable guidance,
comments and suggestions. 
""")

