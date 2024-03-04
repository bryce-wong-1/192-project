import pygame
import time
import math, pandas as pd
from utils import scale_image, blit_rotate_center
import random
pygame.init()
GRASS = scale_image(pygame.image.load("grass.webp"),3)
TRACK = scale_image(pygame.image.load("race-track-square-border.png"), 0.9)

FINISH = pygame.image.load("finish_line.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (360, 305)

RED_CAR = scale_image(pygame.image.load("red-car.png"), 0.5)
GREEN_CAR = scale_image(pygame.image.load("green-car.png"), 0.5)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

FPS = 60
PATH_USER = [(395,0)]
PATH_COMP = [(395,0)]

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        self.start_time = None
        self.distance_traveled = 0
        self.finished = False

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
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        old_x, old_y = self.x, self.y

        if not self.finished:
            if self.start_time is None:
                self.start_time = time.time()
            old_x, old_y = self.x, self.y

        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

        self.distance_traveled += math.hypot(self.x - old_x, self.y - old_y)

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
    IMG = GREEN_CAR
    START_POS = (365, 310)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()


class ComputerCar(AbstractCar):
    def __init__(self,image, max_vel, rotation_vel, path=[], start_pos=(0, 0)):
        self.IMG = image
        self.START_POS = start_pos
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.x, self.y = self.START_POS
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 1)

    def draw(self, win):
        super().draw(win)
        self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()


def draw(win, images, player_car, computer_car,othercars = []):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    computer_car.draw(win)
    for i in range(len(othercars)):
        othercars[i].draw(win)
    pygame.display.update()


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


def handle_collision(player_car, computer_car):
    computer_finish_poi_collide = computer_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide != None:
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()
            computer_car.reset()

def handle_finish(car):
    if not car.finished:
        finish_time = time.time()
        elapsed_time = finish_time - car.start_time
        car.finished = True
        
        # Construct the file path
        file_path = 'track data.xlsx'

        # Define the sheet name where you want to append the data
        sheet_name = 'Sheet4'

        # Create a DataFrame for the new data, now including Rotational Speed
        new_data = pd.DataFrame({
            'Distance': [car.distance_traveled],
            'Time': [elapsed_time],
            'Finish Time': [finish_time],
            "Start Time": [car.start_time],
            'Unit Velocity': [car.distance_traveled/elapsed_time],
            'Max Velocity': [car.max_vel],
            "Rotation Velocity": [car.rotation_vel]
        })

        # Use a context manager to handle reading and writing to Excel file
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            # Try to read the existing data (if any) from the specified sheet
            try:
                existing_data = pd.read_excel(file_path, sheet_name=sheet_name)
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            except FileNotFoundError:
                updated_data = new_data
            except ValueError:  # If the sheet does not exist, write new data
                updated_data = new_data

            # Save the updated data back to the Excel file in the specified sheet
            updated_data.to_excel(writer, sheet_name=sheet_name, index=False)

e,f = 5,8
c = [random.uniform(e,f),random.uniform(e,f),random.uniform(e,f),random.uniform(e,f),random.uniform(e,f),random.uniform(e,f),random.uniform(e,f)]
a,b = [0.85, 1.15]
run = True
clock = pygame.time.Clock()
images = [(GRASS,(0,0)),(TRACK, (0, 0)),(FINISH, FINISH_POSITION)]
player_car = ComputerCar(GREEN_CAR, 6, 6,PATH_USER,(395, 530))
computer_car = ComputerCar(GREEN_CAR,c[0], c[0], PATH_COMP,(395, 530))
othercar1 = ComputerCar(GREEN_CAR,c[1], c[1], PATH_COMP,(395, 530))
othercar2 = ComputerCar(GREEN_CAR,c[2], c[2], PATH_COMP,(395, 530))
othercar3 = ComputerCar(GREEN_CAR,c[3], c[3], PATH_COMP,(395, 530))
othercar4 = ComputerCar(GREEN_CAR,c[4], c[4], PATH_COMP,(395, 530))
othercar5 = ComputerCar(GREEN_CAR,c[5], c[5], PATH_COMP,(395, 530))
othercars = [othercar1,othercar2,othercar3,othercar4,othercar5]

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car, computer_car,othercars)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            player_car.path.append(pos)

    for i in range(len(othercars)):
        othercars[i].move()


    for i in range(len(othercars)):
        if othercars[i].collide(FINISH_MASK, *FINISH_POSITION) and not othercars[i].finished:
            handle_finish(othercars[i])


    
    #handle_collision(player_car, computer_car)

print(player_car.path)
pygame.quit()
