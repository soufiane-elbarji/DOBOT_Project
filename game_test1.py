import pygame
import sys
import time
from serial.tools import list_ports
from pydobot import Dobot

# Connect to DobotSerial
port = "COM3"
print(f"\n🔌 Connecting to Dobot on port {port}...")
device = Dobot(port=port, verbose=False)
device.speed(1000,1500)

# Initialize Pygame
pygame.init()

# Screen setup
width, height = 300, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Arrow Key Square Movement")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Square properties
square_size = 50
x, y = 200, 0
speed = 10
square_color = (0, 255, 0)  # green
device.move_to(x, y, 20, 0, wait=True)

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen with black

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key states
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    # Draw square
    pygame.draw.rect(screen, square_color, (x, y, square_size, square_size))
    device.move_to(x, y, 20, 0, wait=True)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
