import pygame
import random

# Initialize Pygame
pygame.init()

# Display settings
display_width, display_height = 800, 600
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Clouds and Rain')

# Colors
black = (0, 0, 0)
blue = (135, 206, 235)
water_color = (0, 0, 200)  # Dark blue for water

# Load and resize cloud image
cloud_image = pygame.image.load('cloud.png')
cloud_width, cloud_height = cloud_image.get_size()
cloud_width //= 2
cloud_height //= 2
cloud_image = pygame.transform.scale(cloud_image, (cloud_width, cloud_height))

cloud_y_limit = display_height // 6  # Clouds positioned higher

# Generate cloud positions ensuring they fit within the top part of the screen
clouds = []
for _ in range(6):
    x = random.randint(0, max(0, display_width - cloud_width))
    y = random.randint(0, max(0, cloud_y_limit - cloud_height))
    clouds.append((x, y))

# Raindrop class
class Raindrop:
    def __init__(self):
        self.x = random.randint(0, display_width)
        # Start raindrops just below the clouds
        self.y = random.randint(cloud_y_limit + cloud_height // 2, display_height)
        self.speed = random.uniform(9, 12)
    def fall(self):
        self.y += self.speed
        # Reset raindrop position to be just below the clouds
        if self.y > display_height:
            self.y = random.randint(cloud_y_limit + cloud_height // 4, display_height)
            self.x = random.randint(0, display_width)
    def draw(self):
        pygame.draw.line(game_display, blue, (self.x, self.y), (self.x, self.y + 10), 1)

raindrops = [Raindrop() for _ in range(200)]
water_height = 0.0
max_water_height = display_height
water_growth_rate = 0.3 

def draw_filling_water():
    pygame.draw.rect(game_display, water_color, (0, display_height - water_height, display_width, water_height))

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    game_display.fill(black)

    # Draw raindrops
    for drop in raindrops:
        drop.fall()
        drop.draw()
    draw_filling_water()
    if water_height < max_water_height:
        water_height += water_growth_rate
    for cloud in clouds:
        game_display.blit(cloud_image, cloud)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
