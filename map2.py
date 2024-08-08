import pygame
import requests
import subprocess
from pygame.locals import *
import time

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 700, 700
API_KEY = '7e58ae6f42ca61a488040d5cff73153a'

# Dictionary of selected famous locations in Bengaluru with their coordinates (latitude, longitude)
locations = {
    "Bannerghatta": (12.8000, 77.5770),
    "Kengeri": (12.9122, 77.4850),
    "Banashankari": (12.9255, 77.5468),
    "Anekal": (12.7100, 77.6918),
    "Krishnarajapura": (13.0018, 77.7038),
    "Tavarekere": (12.9290, 77.5485),
    "Yelahanka": (13.1007, 77.5963),
    "Peenya": (13.0329, 77.5276),
    "Bommasandra": (12.8163, 77.6910),
    "Koramangala": (12.9352, 77.6245),
    "Malleshwaram": (13.0033, 77.5680),
}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Clickable Bengaluru Map with Weather Info')
font = pygame.font.Font(None, 18)
outline_font = pygame.font.Font(None, 18)  # Font for text outline
popup_font = pygame.font.Font(None, 24)

# Load the Bangalore map image
bangalore_map = pygame.image.load('mapimg.jpg')

# Get the dimensions of the map image
map_width, map_height = bangalore_map.get_size()

# Calculate the initial zoom level to fit the map inside the window
initial_zoom = min(WINDOW_WIDTH / map_width, WINDOW_HEIGHT / map_height)
zoom_level = initial_zoom
zoom_increment = 0.1

def fetch_weather_data(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description'].lower()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        return [
            f"Weather: {weather_description}",
            f"Temperature: {temperature}°C",
            f"Humidity: {humidity}%",
            f"Wind Speed: {wind_speed} m/s"
        ]
    else:
        return ["Error fetching weather data"]

# Main event loop
location_positions = {
    "Bannerghatta": (300, 550),     # Adjusted position based on the map
    "Kengeri": (120, 600),          # Adjusted position based on the map
    "Banashankari": (280, 480),     # Adjusted position based on the map
    "Anekal": (420, 620),           # Adjusted position based on the map
    "Krishnarajapura": (680, 370),  # Adjusted position based on the map
    "Tavarekere": (110, 420),       # Adjusted position based on the map
    "Yelahanka": (350, 150),        # Adjusted position based on the map
    "Peenya": (190, 270),           # Adjusted position based on the map
    "Bommasandra": (600, 500),      # Adjusted position based on the map
    "Koramangala": (390, 370), 
    "Malleshwaram": (240,350)     # Adjusted position based on the map
}

def apply_zoom(coordinates):
    return [(int(x * zoom_level), int(y * zoom_level)) for x, y in coordinates]

def launch_animation(weather_description):  
    animation_process = None
    if 'clear' in weather_description or 'sunny' in weather_description:
        animation_process = subprocess.Popen(['python', 'sunny.py'])
    elif 'rain' in weather_description or 'shower' in weather_description or 'drizzle' in weather_description:
        animation_process = subprocess.Popen(['python', 'rainy.py'])
    elif 'cloud' in weather_description:
        animation_process = subprocess.Popen(['python', 'cloudy.py'])
    else:
        print("No matching animation for this weather description.")
    
    return animation_process

running = True
current_popup = None
popup_timer = None  # Variable to track popup display time
animation_process = None  # Variable to track animation process
animation_start_time = None  # Variable to track animation start time

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Terminate animation process if running
            if animation_process:
                animation_process.terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for location, (lat, lon) in locations.items():
                x_pos, y_pos = location_positions[location]
                x_pos, y_pos = int(x_pos * zoom_level), int(y_pos * zoom_level)
                text = font.render(location, True, (0, 0, 128))  # Dark blue color
                outline_text = outline_font.render(location, True, (255, 255, 255))  # White outline
                text_rect = text.get_rect(center=(x_pos, y_pos))
                outline_text_rect = outline_text.get_rect(center=(x_pos + 1, y_pos + 1))  # Offset for outline
                if text_rect.collidepoint(x, y):
                    weather_info = fetch_weather_data(lat, lon)
                    current_popup = [f"Weather at {location}:"] + weather_info
                    popup_timer = time.time()  # Start the timer for popup display
                    # Launch animation based on weather description
                    if animation_process:
                        animation_process.terminate()  # Terminate current animation if running
                    animation_process = launch_animation(weather_info[0].split(": ")[1])  # Start new animation process
                    animation_start_time = time.time()  # Record animation start time

    # Hide popup after 5 seconds
    if popup_timer and time.time() - popup_timer > 5:
        current_popup = None
        popup_timer = None

    # Check animation timeout (changed to 8 seconds)
    if animation_start_time and time.time() - animation_start_time > 8:
        if animation_process:
            animation_process.terminate()
        animation_process = None
        animation_start_time = None

    # Draw Bangalore map as background
    screen.fill((255, 255, 255))  # Fill with white to clear previous drawings
    scaled_map_width = int(map_width * zoom_level)
    scaled_map_height = int(map_height * zoom_level)
    scaled_bangalore_map = pygame.transform.scale(bangalore_map, (scaled_map_width, scaled_map_height))
    screen.blit(scaled_bangalore_map, (0, 0))

    # Render clickable location names with outline and dark blue color
    for loc, (x_pos, y_pos) in location_positions.items():
        x_pos, y_pos = int(x_pos * zoom_level), int(y_pos * zoom_level)
        text = font.render(loc, True, (0, 0, 128))  # Dark blue color
        outline_text = outline_font.render(loc, True, (255, 255, 255))  # White outline
        text_rect = text.get_rect(center=(x_pos, y_pos))
        outline_text_rect = outline_text.get_rect(center=(x_pos + 1, y_pos + 1))  # Offset for outline
        screen.blit(outline_text, outline_text_rect)
        screen.blit(text, text_rect)

    # Render popup if exists
    if current_popup:
        popup_x = 10  # Position the popup near the top left corner of the window
        popup_y = 10
        popup_width = WINDOW_WIDTH // 3
        popup_height = len(current_popup) * 40

        pygame.draw.rect(screen, (0, 0, 0), (popup_x, popup_y, popup_width, popup_height), 0)
        pygame.draw.rect(screen, (255, 193, 7), (popup_x + 2, popup_y + 2, popup_width - 4, popup_height - 4), 0)

        for i, line in enumerate(current_popup):
            popup_surf = popup_font.render(line, True, (0, 0, 0))  # Black text
            popup_rect = popup_surf.get_rect(center=(popup_x + popup_width // 2, popup_y + 30 + i * 30))
            screen.blit(popup_surf, popup_rect)

    pygame.display.flip()

pygame.quit()
