import pygame, time, math
from utils import scale_image, blit_rotate_center

pygame.init()



TRACK = scale_image(pygame.image.load("race-track-square.jpg"), 1.1)
TRACK_BORDER = scale_image(pygame.image.load("race-track-square-border.png"), 1.1)

CAR = scale_image(pygame.image.load("simple-travel-car-top_view.svg"),0.05)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

run = True

class AbstractCar:

    def __init__(self, max_vel, rotation_vel):
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.5
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
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()


class PlayerCar(AbstractCar):
    IMG = CAR
    START_POS = (450, 450)

def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()

FPS = 60
clock = pygame.time.Clock()
images = [(TRACK, (0,0)), (TRACK_BORDER, (0,0))]
player_car = PlayerCar(3,3)

while run:
    clock.tick(FPS)
    
    draw(WINDOW, images, player_car)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()

    if not moved:
        player_car.reduce_speed()
pygame.quit()