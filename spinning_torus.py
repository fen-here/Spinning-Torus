import os
os.environ['SDL_VIDEO_WINDOW_TRANSPARENCY'] = '0.7'

import pygame
import math
import sys

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 80
X_SPACE = WINDOW_WIDTH // SCREEN_WIDTH
Y_SPACE = WINDOW_HEIGHT // SCREEN_HEIGHT

R1 = 1
R2 = 2
K2 = 5
K1 = 40  

Aascii_chars = ".,-~:;=!*#$@/"

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("3D ASCII Donut (Pygame)")
font = pygame.font.SysFont("Courier", 12, bold=True)
clock = pygame.time.Clock()

A = math.pi / 4
B = 0.0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    screen.fill((30, 30, 30))

    SCREEN_BUFFER = [[" " for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]
    Z_BUFFER = [[0.0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]


    theta = 0.0
    while theta < 2 * math.pi:
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        sin_A, cos_A = math.sin(A), math.cos(A)
        sin_B, cos_B = math.sin(B), math.cos(B)

        phi = 0.0
        while phi < 2 * math.pi:
            cos_phi = math.cos(phi)
            sin_phi = math.sin(phi)

            torus_x = R2 + R1 * cos_theta
            torus_y = R1 * sin_theta  

            local_x = torus_x * cos_phi
            local_y = torus_x * sin_phi
            local_z = torus_y

            #defining the torus and the center
            #x = (r_1 + R_2 cos0)-cos0
            #y=(R_2+R_1cos0)-sin0
            #z = R_1sin0


            #Spins the donut
            rot_x = local_x * cos_B - local_z * sin_B
            rot_z = local_x * sin_B + local_z * cos_B
            rot_y = local_y

            #x^1 = x cosB - z sin B
            #z^1 = x sin B + z cos B
    
            
            x_3d = rot_x
            y_3d = rot_y * cos_A - rot_z * sin_A
            z_3d = K2 + rot_y * sin_A + rot_z * cos_A

            #y^n = y^1 cos A - z^1 sin A
            #z^n = y^1 sin A + z^1 cos A

            ooz = 1.0 / z_3d

            #calculates the points
            xp = int(SCREEN_WIDTH / 2 + K1 * ooz * x_3d)
            yp = int(SCREEN_HEIGHT / 2 - K1 * ooz * y_3d)

            #x_screen = center_x + k_1 * x / z
            #y_screen = center_y - K_1 * y / z

            #the shading of the axies
            nx = cos_theta * cos_phi * sin_B + sin_theta * cos_B
            ny = cos_theta * sin_phi
            nz = -cos_theta * cos_phi * cos_B + sin_theta * sin_B

            #N^-> = (cos0-cos0, cos0-sin0,sin0)


            #calculates the shading
            raw_L = (ny - nz) / 1.41421
            L = (raw_L + 1.0) / 2.0

            #N^->*L^-> = (n_x * 0) +(n_y*1)+(n_z*-1) = n_y - n_z

            #Calculates the shading and lighting
            if 0 <= xp < SCREEN_WIDTH and 0 <= yp < SCREEN_HEIGHT:
                if ooz > Z_BUFFER[yp][xp]:
                    Z_BUFFER[yp][xp] = ooz
                    #1/z_new > 1/z_existing
                    char_index = int(L * (len(Aascii_chars) - 1))
                    if char_index >= len(Aascii_chars):
                        char_index = len(Aascii_chars) - 1
                    SCREEN_BUFFER[yp][xp] = Aascii_chars[char_index]
            phi += 0.03  
        theta += 0.07   

    #Draws to the screen.
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            char_token = SCREEN_BUFFER[y][x]
            if char_token != " ":
                text_surface = font.render(char_token, True, (255, 255, 255))
                screen.blit(text_surface, (x * X_SPACE, y * Y_SPACE))

    pygame.display.flip()
    B += 0.04
    clock.tick(1)


