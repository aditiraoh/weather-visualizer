import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
display_width = 800
display_height = 600
display = pygame.display.set_mode((display_width, display_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Sunny Weather Simulation")

# Set up OpenGL
glClearColor(0.2, 0.4, 0.8, 1.0)  # Light blue sky color
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glMatrixMode(GL_PROJECTION)
gluOrtho2D(0, display_width, 0, display_height)
glMatrixMode(GL_MODELVIEW)

# Variables for Ferris wheel rotation
ferris_wheel_rotation_angle = 0.0
ferris_wheel_rotation_speed = 0.5  # Increased speed of rotation

# Cloud variables
clouds = [
    [random.randint(0, display_width), random.randint(display_height // 2, display_height - 100)],
    [random.randint(0, display_width), random.randint(display_height // 2, display_height - 100)],
    [random.randint(0, display_width), random.randint(display_height // 2, display_height - 100)]
]
cloud_translation_speed = 0.5  # Speed of cloud movement

def draw_sun(x, y, radius, num_rays):
    glColor3f(1.0, 1.0, 0.0)  # Yellow color for sun
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(num_rays + 1):
        angle = i * (360 / num_rays)
        glVertex2f(x + radius * math.cos(math.radians(angle)), y + radius * math.sin(math.radians(angle)))
    glEnd()

    glColor4f(1.0, 1.0, 1.0, 0.5)  # White color with transparency for rays
    glBegin(GL_LINES)
    for i in range(num_rays):
        angle = i * (360 / num_rays)
        glVertex2f(x, y)
        glVertex2f(x + radius * 1.5 * math.cos(math.radians(angle)), y + radius * 1.5 * math.sin(math.radians(angle)))
    glEnd()

def draw_ferris_wheel(x, y, radius, num_cars):
    global ferris_wheel_rotation_angle

    # Draw Ferris wheel stand
    glColor3f(0.3, 0.3, 0.3)  # Dark gray color for stand
    glBegin(GL_QUADS)
    glVertex2f(x - 10, y - 20)
    glVertex2f(x + 10, y - 20)
    glVertex2f(x + 20, y - radius - 50)
    glVertex2f(x - 20, y - radius - 50)
    glEnd()

    # Draw Ferris wheel frame
    glColor3f(0.4, 0.4, 0.4)  # Gray color for frame
    glLineWidth(8)  # Thicker frame
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        angle = math.radians(i)
        glVertex2f(x + radius * math.cos(angle), y + radius * math.sin(angle))
    glEnd()
    glLineWidth(1)  # Reset line width

    # Draw Ferris wheel cars
    for i in range(num_cars):
        angle = ferris_wheel_rotation_angle + (i * (360 / num_cars))
        car_x = x + radius * math.cos(math.radians(angle))
        car_y = y + radius * math.sin(math.radians(angle)) - 20

        draw_ferris_wheel_car(car_x, car_y)

    # Draw Ferris wheel spokes
    glColor3f(0.4, 0.4, 0.4)  # Gray color for spokes
    glBegin(GL_LINES)
    for i in range(num_cars):
        angle = ferris_wheel_rotation_angle + (i * (360 / num_cars))
        glVertex2f(x, y)
        glVertex2f(x + radius * math.cos(math.radians(angle)), y + radius * math.sin(math.radians(angle)))
    glEnd()

    # Update rotation angle
    ferris_wheel_rotation_angle += ferris_wheel_rotation_speed
    if ferris_wheel_rotation_angle >= 360:
        ferris_wheel_rotation_angle = 0

def draw_ferris_wheel_car(x, y):
    car_width = 40
    car_height = 20

    # Draw car body
    glColor3f(0.0, 0.6, 0.8)  # Light blue color for car body
    glBegin(GL_QUADS)
    glVertex2f(x - car_width / 2, y)
    glVertex2f(x + car_width / 2, y)
    glVertex2f(x + car_width / 2, y + car_height)
    glVertex2f(x - car_width / 2, y + car_height)
    glEnd()

    # Draw car roof
    glColor3f(0.8, 0.1, 0.1)  # Red color for car roof
    glBegin(GL_TRIANGLES)
    glVertex2f(x - car_width / 2, y + car_height)
    glVertex2f(x + car_width / 2, y + car_height)
    glVertex2f(x, y + car_height + 10)
    glEnd()

    # Draw car windows
    glColor3f(1.0, 1.0, 1.0)  # White color for windows
    window_width = 8
    window_height = 10
    num_windows = 3
    for i in range(num_windows):
        glBegin(GL_QUADS)
        glVertex2f(x - car_width / 2 + 5 + (i * (window_width + 5)), y + 5)
        glVertex2f(x - car_width / 2 + 5 + (i * (window_width + 5)) + window_width, y + 5)
        glVertex2f(x - car_width / 2 + 5 + (i * (window_width + 5)) + window_width, y + 5 + window_height)
        glVertex2f(x - car_width / 2 + 5 + (i * (window_width + 5)), y + 5 + window_height)
        glEnd()

def draw_cloud(x, y):
    glColor4f(1.0, 1.0, 1.0, 0.8)  # White color with slight transparency for clouds

    # Draw cloud with multiple ellipses
    cloud_positions = [
        (x - 30, y), (x - 10, y - 10), (x + 10, y), (x + 30, y - 10),
        (x, y + 10),(x+10,y+10)
    ]
    
    for pos in cloud_positions:
        cx, cy = pos
        glBegin(GL_TRIANGLE_FAN)
        for i in range(360):
            angle = math.radians(i)
            glVertex2f(cx + 30 * math.cos(angle), cy + 15 * math.sin(angle))
        glEnd()


def draw_grass():
    glColor3f(0.34, 0.68, 0.2)  # Grass green color
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(display_width, 0)
    glVertex2f(display_width, display_height // 4)
    glVertex2f(0, display_height // 4)
    glEnd()

def draw_sunny():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw the sun
    draw_sun(700, 500, 50, 16)  # Adjust position and radius as needed

    # Draw clouds
    for cloud in clouds:
        draw_cloud(cloud[0], cloud[1])
        cloud[0] -= cloud_translation_speed
        if cloud[0] < -50:
            cloud[0] = display_width + 50
            cloud[1] = random.randint(display_height // 2, display_height - 100)

    # Draw grass
    draw_grass()

    # Draw Ferris wheel
    draw_ferris_wheel(400, 200, 120, 8)  # Reduced radius

    # Update the display
    pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_sunny()

# Quit Pygame
pygame.quit()
