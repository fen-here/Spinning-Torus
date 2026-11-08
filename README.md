# Spinning-Torus
I made a donut spin :D

                                                            :;;;;=                                                         
                                                       ~:;;;:::::;==!                                                     
                                                     -:;==;;:::~~~:;=!#                                                   
                                                    -:;=!=!=:~----~:;=!                                                   
                                                    ~;;!*###   .,-~:;=!#                                                  
                                                    ~;==!*#    ,-~~:;=!#                                                  
                                                    -:;;;==;:~~~~:;;==!#                                                  
                                                    -~:::;;:::::;;;==!*                                                   
                                                     ~~:::::;;;;;;;==!                                                    
                                                      -~::::;;;;;==!*                                                     
                                                          :;;;;==   


---

## Inspiration of this:
I wanted to understand how you create geomatry with code and how to render it to a screen. I was some what inspired by videos of rotating objects in ascii. This allowed me to learn the math concepts and break the project down into a understandable concepts.

### What I learnt:
- The geometric math of a torus
- Sudo Code
- shading mathimatical objects and rendering to a screen.

##### Did I use AI?
AI was used to understand the math behind the project and help explain the Sudo code for the project. The math implementation was written by me.


### Math behind it:
### defining the torus and the center
For this I had to create the torus. 

$x=(r_1+R_2 cos0)-cos0$
$y=(R_2+R_1cos0)-sin0$
$z=R_1sin0$

```py
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
```



### Spinning the Torus:
The next part was calculating the rotation of the torus. This concept was hard for me to understand.
$x^1=xcosB-zsinB$
$z^1=xsinB+zcosB$
$y^n = y^1 cos A - z^1 sin A$
$z^n = y^1 sin A + z^1 cos A$

```py
rot_x = local_x * cos_B - local_z * sin_B
rot_z = local_x * sin_B + local_z * cos_B
rot_y = local_y

x_3d = rot_x
y_3d = rot_y * cos_A - rot_z * sin_A
z_3d = K2 + rot_y * sin_A + rot_z * cos_A

ooz = 1.0 / z_3d
```

### Calculates the points:
This was calculating the points of the torus to the screen width as well as getting the values of the torus to the screen. This is important for shading the object in ascii appropriate to it's **Z-depth**.

$x_screen=center_x+k_1*x/z$
$y_screen=center_y-K_1*y/z$
$N^->=(cos0-cos0, cos0-sin0,sin0)$

```py
xp = int(SCREEN_WIDTH / 2 + K1 * ooz * x_3d)
yp = int(SCREEN_HEIGHT / 2 - K1 * ooz * y_3d)

nx = cos_theta * cos_phi * sin_B + sin_theta * cos_B
ny = cos_theta * sin_phi
nz = -cos_theta * cos_phi * cos_B + sin_theta * sin_B
```

#### Calculating Shading:
$N^->*L^->=(n_x * 0)+(n_y*1)+(n_z*-1)=n_y-n_z$

#### Calculates the shading and lighting:
$1/z_new>1/z_existing$

```py
if 0 <= xp < SCREEN_WIDTH and 0 <= yp < SCREEN_HEIGHT:
  if ooz > Z_BUFFER[yp][xp]:
    Z_BUFFER[yp][xp] = ooz
    char_index = int(L * (len(Aascii_chars) - 1))
    if char_index >= len(Aascii_chars):
      char_index = len(Aascii_chars) - 1
    SCREEN_BUFFER[yp][xp] = Aascii_chars[char_index]
```


### Rendering:
```py
for y in range(SCREEN_HEIGHT):
  for x in range(SCREEN_WIDTH):
    char_token = SCREEN_BUFFER[y][x]
    if char_token != " ":
      text_surface = font.render(char_token, True, (255, 255, 255))
      screen.blit(text_surface, (x * X_SPACE, y * Y_SPACE))
```
