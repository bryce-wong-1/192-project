import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
track_image = pygame.image.load('race-track-square.jpg')
car_image = pygame.image.load('simple-travel-car-top_view.svg').convert_alpha()
# Scale the car image if it's too big or too small
car_image = pygame.transform.scale(car_image, (40, 20))

# Colors
WHITE = (255, 255, 255)

# Frame rate
FPS = 60
clock = pygame.time.Clock()

# Car settings
user_car_pos = [400, 428]
user_car_angle = 0
user_car_speed = 0
user_car_max_speed = 5
user_car_acceleration = 0.2
user_car_rotation_speed = 5

computer_car_pos = [400, 400]
computer_car_rect = car_image.get_rect(midbottom = (40,20))
computer_car_angle = 0
computer_car_speed = 3
computer_car_path = [(400, 400), (620, 400), (620, 110), (500,120), (140,130), (150,390)]  # Add waypoints for the computer car to follow
current_waypoint = 0

start_rect = pygame.Rect(380, 418, 40, 20)

# Start the timer
# Start the timer
start_time = None  # Initialize start_time as None
lap_completed = False  # Flag to indicate the car has completed a lap


pygame.draw.rect(screen, (0, 255, 0), start_rect)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    computer_car_rect = pygame.Rect(computer_car_pos[0], computer_car_pos[1], 40, 20)  # Update with computer car size
    if computer_car_rect.colliderect(start_rect):
        if not lap_completed:
            # If lap_completed is False, it means the car has just collided with the start rect again
            if start_time is not None:  # To avoid printing the time at the very start of the race
                time_elapsed = (pygame.time.get_ticks() - start_time) / 1000.0  # Time in seconds
                print(f"Collision time: {time_elapsed} seconds")
            start_time = pygame.time.get_ticks()  # Reset the timer
            lap_completed = True  # Set the flag to True as the car is on the starting line
    else:
        # If the car is not colliding, reset the lap_completed flag to allow timing for the next lap
        lap_completed = False
    # User car control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:  # Accelerate
        user_car_speed = min(user_car_speed + user_car_acceleration, user_car_max_speed)
    elif keys[pygame.K_DOWN]:  # Decelerate
        user_car_speed = max(user_car_speed - user_car_acceleration, -user_car_max_speed / 2)
    else:  # Natural deceleration
        user_car_speed *= 0.98

    if keys[pygame.K_LEFT]:  # Rotate left
        user_car_angle += user_car_rotation_speed
    if keys[pygame.K_RIGHT]:  # Rotate right
        user_car_angle -= user_car_rotation_speed

    # Update user car position
    user_car_pos[0] += user_car_speed * math.cos(math.radians(user_car_angle))
    user_car_pos[1] += user_car_speed * math.sin(math.radians(user_car_angle))

    # Computer car logic (basic example, follows a set of waypoints)
    target_pos = computer_car_path[current_waypoint]
    computer_car_angle = math.atan2(target_pos[1] - computer_car_pos[1], target_pos[0] - computer_car_pos[0])
    computer_car_pos[0] += computer_car_speed * math.cos(computer_car_angle)
    computer_car_pos[1] += computer_car_speed * math.sin(computer_car_angle)
    
    # Check if the computer car reached the waypoint
    if math.hypot(computer_car_pos[0] - target_pos[0], computer_car_pos[1] - target_pos[1]) < 10:
        current_waypoint = (current_waypoint + 1) % len(computer_car_path)

    # Drawing
    screen.fill(WHITE)
    screen.blit(track_image, (0, 0))
    
    rotated_user_car = pygame.transform.rotate(car_image, user_car_angle)
    screen.blit(rotated_user_car, user_car_pos)

    rotated_computer_car = pygame.transform.rotate(car_image, math.degrees(computer_car_angle))
    screen.blit(rotated_computer_car, computer_car_pos)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
