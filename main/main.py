import pygame
import math
from utils import scale_image, blit_rotate_center

# Initialize pygame
pygame.init()
pygame.font.init()

# Load images
TRACK = scale_image(pygame.image.load("CITYPLAN.png"), 0.9)
TRACK_BORDER = scale_image(pygame.image.load("CITYPLAN_mask.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

TERMINAL = scale_image(pygame.image.load("terminal.png"),0.5)

RED_CAR = scale_image(pygame.image.load("taxi.png"), 0.15)
GREEN_CAR = scale_image(pygame.image.load("Mini_van.png"), 0.15)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DRIVE IN THE CITY!")

FPS = 60

# List of paths to follow
PATH = [
    (545, 747), 
    (545, 694), (538, 663), (435, 640), (370, 640),
    (220, 645), (180, 627),
    (180, 380), (100, 340), 
    (70, 320), (69, 180), (68, 82),
    (65, -50)
]
PAUSE_DURATION = 0.3
PAUSE_POINTS = [3, 4, 7, 9, 10, 11, 12]


class AbstractCar:
    def __init__(self, max_vel, rotation_vel, start_pos, img):
        self.img = img
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = start_pos
        self.prev_x, self.prev_y = start_pos  # Initialize previous position
        self.acceleration = 0.1
        self.total_distance = 0  # Distance traveled

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
        
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        # Store old position
        self.prev_x, self.prev_y = self.x, self.y

        # Calculate new position based on velocity and angle
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        # Update position
        self.x -= horizontal
        self.y -= vertical

        # Calculate distance traveled this frame
        distance = math.sqrt((self.x - self.prev_x) ** 2 + (self.y - self.prev_y) ** 2)
        self.total_distance += distance/50  # Update total distance

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0
        
class PlayerCar(AbstractCar):
    IMG = RED_CAR  # Assigning the specific car image
    START_POS = (550, 680)  # Starting position from the PATH list

    def __init__(self, max_vel, rotation_vel):
        super().__init__(max_vel, rotation_vel, self.START_POS, self.IMG)
        self.prev_x, self.prev_y = self.START_POS 
        self.total_distance = 0  

    def move(self):
        # Store old position before moving
        self.prev_x, self.prev_y = self.x, self.y
        
        # Calculate new position based on velocity and angle
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        
        # Update position
        self.x -= horizontal
        self.y -= vertical
        
        # Calculate distance traveled this frame
        distance = math.sqrt((self.x - self.prev_x) ** 2 + (self.y - self.prev_y) ** 2)
        self.total_distance += distance/100  # Update total distance

    def reduce_speed(self):
        # Reduce the speed by half the acceleration rate
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()  # Ensure to move after adjusting the speed to update distance accordingly

    def bounce(self):
        # Reverse the velocity
        self.vel = -self.vel
        self.move()  # Move after bouncing to update position and distance

        
def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()

def draw_text(surface, text, font, color, position):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)
def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


# Define font, size and color
font_size = 20
font_color = (255, 255, 0)  # Yellow color for visibility
try:
    font = pygame.font.Font("Minecraft.ttf", font_size)
except IOError:
    # Fallback if the custom font cannot be loaded
    print("Failed to load the specified font. Falling back to default font.")
    font = pygame.font.Font(None, font_size)

run = True
clock = pygame.time.Clock()
images = [(TRACK, (0, 0)),(TERMINAL, (250, 50))]

player_car = PlayerCar(1, 2)

STOPS = 0

def fuel_check(stops, distance):
    FS = 1.4*((0.01)/8.2)*stops + distance/8.2
    FSS = 1.4*((0.01)/8.2/1.9)*stops + distance/8.2 #system improves mpg
    SAVED = FS - FSS
    PS = 3.95*(SAVED)
    
    return FS, FSS, SAVED, PS
    
while run:
    clock.tick(FPS)

    # Clear the screen by filling it with a color, typically do this before drawing everything
    WIN.fill((0, 0, 0))  # Fill with black or another contrasting color
    
    # Draw everything else
    draw(WIN, images, player_car)

    # Render text
    draw_text(WIN, f"Stops: {STOPS}", font, font_color, (260, 60))
    draw_text(WIN, f"Distance Traveled: {player_car.total_distance:.2f} miles", font, font_color, (260, 80))
    draw_text(WIN, f"Fuel spent without system: {fuel_check(STOPS, player_car.total_distance)[0]:.2f} gallons", font, font_color, (260, 100))
    draw_text(WIN, f"Fuel spent with system: {fuel_check(STOPS, player_car.total_distance)[1]:.2f} gallons", font, font_color, (260, 120))
    draw_text(WIN, f"Fuel saved: {fuel_check(STOPS, player_car.total_distance)[2]:.2f} gallons", font, font_color, (260, 140))
    draw_text(WIN, f"Potential Savings: ${fuel_check(STOPS, player_car.total_distance)[3]:.2f}", font, font_color, (260, 160))

    # Handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            player_car.path.append(pos)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                STOPS += 1

    # Update game state
    move_player(player_car)

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()
    # Update display
    pygame.display.update()
pygame.quit()
