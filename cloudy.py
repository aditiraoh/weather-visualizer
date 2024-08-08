import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
CLOUD_SPEED = 0.5
CLOTHES_SWAY_SPEED = 1
CLOTHES_FLY_SPEED = 3
CLOTHES_MOVE_SPEED = 1  # Speed at which clothes move to the left

# Colors
WHITE = (255, 255, 255)
LIGHT_GREY = (140, 140, 140)
DARK_GREY = (110, 110, 110)
GREY_SKY = (70, 70, 70)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
RED = (150, 0, 0)
BLUE = (0, 0, 255)
GREEN_COLOR = (0, 255, 0)
GRAY = (128, 128, 128)
LIGHT_BROWN = (210, 180, 140)
BLACK = (0, 0, 0)
WINDOW_COLOR = (173, 216, 230)

# Cloud parameters
NUM_CLOUDS = 20
LAND_HEIGHT = WINDOW_HEIGHT // 4

# Clothes parameters
CLOTHES = [
    {"color": GREEN_COLOR, "rect": pygame.Rect(330, WINDOW_HEIGHT - LAND_HEIGHT - 150, 30, 50)},
    {"color": RED, "rect": pygame.Rect(370, WINDOW_HEIGHT - LAND_HEIGHT - 150, 30, 50)},
    {"color": BLUE, "rect": pygame.Rect(410, WINDOW_HEIGHT - LAND_HEIGHT - 150, 30, 50)}
]
sway_directions = [1, 1]  # Direction for each cloth

# House position
house_x = 600

# Stick and rope positions
stick1_x = 250
stick2_x = 450
stick1_y = WINDOW_HEIGHT - LAND_HEIGHT - 120
stick2_y = WINDOW_HEIGHT - LAND_HEIGHT - 120

# Create a screen surface
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Cloudy Sky with Wind Animation')

# Generate random clouds
clouds = []
for _ in range(NUM_CLOUDS):
    x = random.randint(-200, WINDOW_WIDTH)
    y = random.randint(-50, WINDOW_HEIGHT // 2)
    size = random.randint(80, 200)
    clouds.append((x, y, size))

def draw_house():
    global house_x
    house_x -= 50  # Move the house 50 pixels to the left

    # Draw the base of the house
    pygame.draw.rect(screen, BROWN, (house_x, WINDOW_HEIGHT - LAND_HEIGHT - 200, 200, 200))
    
    # Draw the roof
    pygame.draw.polygon(screen, RED, [
        (house_x - 10, WINDOW_HEIGHT - LAND_HEIGHT - 200),  # Left corner of the roof
        (house_x + 210, WINDOW_HEIGHT - LAND_HEIGHT - 200), # Right corner of the roof
        (house_x + 100, WINDOW_HEIGHT - LAND_HEIGHT - 300)  # Peak of the roof
    ])
    
    # Draw the chimney
    pygame.draw.rect(screen, GRAY, (house_x + 130, WINDOW_HEIGHT - LAND_HEIGHT - 290, 40, 100))
    
    # Draw the door
    pygame.draw.rect(screen, LIGHT_BROWN, (house_x + 75, WINDOW_HEIGHT - LAND_HEIGHT - 100, 50, 100))
    pygame.draw.rect(screen, BLACK, (house_x + 75, WINDOW_HEIGHT - LAND_HEIGHT - 100, 50, 100), 2)
    
    # Draw windows
    pygame.draw.rect(screen, WINDOW_COLOR, (house_x + 25, WINDOW_HEIGHT - LAND_HEIGHT - 175, 50, 50))
    pygame.draw.rect(screen, BLACK, (house_x + 25, WINDOW_HEIGHT - LAND_HEIGHT - 175, 50, 50), 2)
    pygame.draw.line(screen, BLACK, (house_x + 50, WINDOW_HEIGHT - LAND_HEIGHT - 175), (house_x + 50, WINDOW_HEIGHT - LAND_HEIGHT - 125), 2)
    pygame.draw.line(screen, BLACK, (house_x + 25, WINDOW_HEIGHT - LAND_HEIGHT - 150), (house_x + 75, WINDOW_HEIGHT - LAND_HEIGHT - 150), 2)
    
    pygame.draw.rect(screen, WINDOW_COLOR, (house_x + 125, WINDOW_HEIGHT - LAND_HEIGHT - 175, 50, 50))
    pygame.draw.rect(screen, BLACK, (house_x + 125, WINDOW_HEIGHT - LAND_HEIGHT - 175, 50, 50), 2)
    pygame.draw.line(screen, BLACK, (house_x + 150, WINDOW_HEIGHT - LAND_HEIGHT - 175), (house_x + 150, WINDOW_HEIGHT - LAND_HEIGHT - 125), 2)
    pygame.draw.line(screen, BLACK, (house_x + 125, WINDOW_HEIGHT - LAND_HEIGHT - 150), (house_x + 175, WINDOW_HEIGHT - LAND_HEIGHT - 150), 2)
    
    house_x += 50  # Reset house_x to its original position for other calculations



# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move clouds horizontally
    for i in range(len(clouds)):
        x, y, size = clouds[i]
        x += CLOUD_SPEED
        if x > WINDOW_WIDTH:
            x = random.randint(-200, -size)
            y = random.randint(-50, WINDOW_HEIGHT // 2)
        clouds[i] = (x, y, size)

    # Clear screen and draw grey sky
    screen.fill(GREY_SKY)

    # Draw clouds
    for cloud in clouds:
        x, y, size = cloud
        cloud_color = random.choice([LIGHT_GREY,LIGHT_GREY,LIGHT_GREY, DARK_GREY])
        pygame.draw.ellipse(screen, cloud_color, (x, y, size, size // 2))
        pygame.draw.ellipse(screen, cloud_color, (x + size // 2, y - size // 4, size, size // 2))
        pygame.draw.ellipse(screen, cloud_color, (x - size // 2, y - size // 4, size, size // 2))

    # Draw clothes
    for idx, cloth in enumerate(CLOTHES):
        rect = cloth["rect"]
        color = cloth["color"]
        pygame.draw.rect(screen, color, rect)

        if idx < len(CLOTHES) - 1:  # Sway the first two clothes
            rect.y += sway_directions[idx] * CLOTHES_SWAY_SPEED
            if rect.y <= WINDOW_HEIGHT - LAND_HEIGHT - 160 or rect.y >= WINDOW_HEIGHT - LAND_HEIGHT - 140:
                sway_directions[idx] *= -1
        else:  # Make the last cloth fly up and to the right
            rect.x += CLOTHES_FLY_SPEED
            rect.y -= CLOTHES_FLY_SPEED
            if rect.y < -rect.height or rect.x > WINDOW_WIDTH:
                rect.x, rect.y = 480, WINDOW_HEIGHT - LAND_HEIGHT - 150  # Reset position

    # Draw ground
    pygame.draw.rect(screen, GREEN, (0, WINDOW_HEIGHT - LAND_HEIGHT, WINDOW_WIDTH, LAND_HEIGHT))
    draw_house()

    # Draw sticks
    pygame.draw.rect(screen, BROWN, (stick1_x, stick1_y, 5, 120))
    pygame.draw.rect(screen, BROWN, (stick2_x, stick2_y, 5, 120))

    # Draw rope
    rope_start = (stick1_x + 2, stick1_y)
    rope_end = (stick2_x + 2, stick2_y)
    pygame.draw.line(screen, WHITE, rope_start, rope_end, 2)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
