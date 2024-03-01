import pygame, time, math
from utils import scale_image, blit_rotate_center

pygame.init()



TRACK = scale_image(pygame.image.load("race-track-square.jpg"), 1.1)
TRACK_BORDER = scale_image(pygame.image.load("race-track-square-border.png"), 1.1)

FINISH_POS = (503, 441)
FINISH = pygame.image.load('finish_line.png')
FINISH_MASK = pygame.mask.from_surface(FINISH)

CAR = scale_image(pygame.image.load("simple-travel-car-top_view.svg"),0.05)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

run = True

class AbstractCar:

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
    def draw(self, win):
        blit_rotate_center(win, self.IMG, (self.x, self.y), self.angle)
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
    def move(self):
        radians = math.radians(self.angle)
        horizontal = math.cos(radians) * self.vel
        vertical = math.sin(radians) * self.vel

        self.y -= vertical
        self.x += horizontal
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.IMG)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset) 
        return poi
    def reset(self):
        self.x,self.y = self.START_POS
        self.angle = 0
        self.vel = 0
    


class PlayerCar(AbstractCar):
    IMG = CAR
    START_POS = (450, 450)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()
    
    def bounce(self):
        self.vel = -self.vel
        self.move()

class ComputerCar(AbstractCar):
    IMG = CAR
    START_POS = (450, 475)

    def __init__(self,max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255,0,0), point, 5)

    def draw(self,win):
        super().draw(win)
        self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        desired_radian_angle = math.atan2(x_diff, y_diff)
        desired_angle = math.degrees(desired_radian_angle) % 360

        # Your existing angle adjustment logic here
        angle_diff = (desired_angle - self.angle + 90) % 360 - 180
        # Adjust the car's angle by the minimum between the rotation speed and the absolute angle difference
        if angle_diff > 0:
            self.angle -= min(self.rotation_vel, abs(angle_diff))
        else:
            self.angle += min(self.rotation_vel, abs(angle_diff))
        self.angle %= 360  # Normalize the angle


    
    def update_path_point(self):

        target_x, target_y = self.path[self.current_point]
        distance_to_point = math.sqrt((target_x - self.x) ** 2 + (target_y - self.y) ** 2)

        # Check if the car is close enough to the target point to consider it "reached"
        if distance_to_point < 100:  # You can adjust this threshold as needed
            self.current_point += 1
            if self.current_point >= len(self.path):
                self.vel = 0  # Stop the car if it has reached the last point
            else:
                self.vel = self.max_vel  # Reset velocity to ensure the car keeps moving


    def move(self):
        if self.current_point >= len(self.path):
            return 
        
        self.calculate_angle()
        self.update_path_point()
        super().move()

def draw(win, images, player_car, computer_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    computer_car.draw(win)
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

FPS = 60
path = [(553, 485), (608, 488), (665, 491), (713, 462), (737, 398), (745, 348), (743, 280), (740, 211), (730, 144), (663, 97), (603, 90), (552, 90), (471, 91), (388, 89), (308, 87), (222, 99), (170, 123), (141, 168), (134, 250), (130, 339), (151, 443), (197, 472), (245, 485), (328, 492), (409, 498), (488, 494)]
clock = pygame.time.Clock()
images = [(TRACK, (0,0)),(FINISH,FINISH_POS), (TRACK_BORDER, (0,0))]
player_car = PlayerCar(3,3)
computer_car = ComputerCar(2,5, path)

while run:
    clock.tick(FPS)
    
    draw(WINDOW, images, player_car,computer_car)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            computer_car.path.append(pos)
    move_player(player_car)
    computer_car.move()
    if player_car.collide(FINISH_MASK) != None:
        print('collision')
    
    finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POS)
    if finish_poi_collide != None:
        if finish_poi_collide[0] == 0:
            #while player_car.vel != 0:
            player_car.reduce_speed()
            print('hit')
        else:
            #player_car.reset()
            print('finish')
print(computer_car.path)
pygame.quit()