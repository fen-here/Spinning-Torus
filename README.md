# Spinning Torus
I made a donut spin! :D

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

## Project Inspiration
I wanted to understand how to create 3D geometry using code and render it directly to a screen. I was highly inspired by videos of rotating objects rendered in ASCII art. This project allowed me to learn foundational mathematics and break a complex programming problem down into understandable concepts.

### What I Learned:
*   The geometric math of a torus
*   Writing and implementing pseudocode
*   Shading mathematical objects and implementing a rendering pipeline

##### Did I use AI?
AI was used to help understand the core math equations behind the project and clarify the pseudocode structures. The actual Python implementation of the math was written entirely by me.

---

## The Math Behind It

### 1. Defining the Torus and Center
First, I needed to define the structural geometry of the torus using parametric equations:

$[x = (R_2 + R_1 \cos\theta)\cos\phi\]$
$[y = (R_2 + R_1 \cos\theta)\sin\phi\]$
$[z = R_1 \sin\theta\]$

```python
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

### 2. Spinning the Torus
The next part involved calculating the real-time rotation matrices of the torus across multiple axes (\(A\) and \(B\)). 

\[x' = x \cos B - z \sin B\]
\[z' = x \sin B + z \cos B\]
\[y'' = y' \cos A - z' \sin A\]
\[z'' = y' \sin A + z' \cos A\]

```python
rot_x = local_x * cos_B - local_z * sin_B
rot_z = local_x * sin_B + local_z * cos_B
rot_y = local_y

x_3d = rot_x
y_3d = rot_y * cos_A - rot_z * sin_A
z_3d = K2 + rot_y * sin_A + rot_z * cos_A

ooz = 1.0 / z_3d
```

### 3. Calculating the Screen Points
This phase projects the 3D coordinates onto a 2D screen coordinate system based on the screen width and height. This step tracks \(1/z\) (`ooz`), which is essential for shading the object appropriately based on its **Z-depth**.

\[x_{\text{screen}} = \text{center}_x + K_1 \cdot \frac{x}{z}\]
\[y_{\text{screen}} = \text{center}_y - K_1 \cdot \frac{y}{z}\]

```python
xp = int(SCREEN_WIDTH / 2 + K1 * ooz * x_3d)
yp = int(SCREEN_HEIGHT / 2 - K1 * ooz * y_3d)

nx = cos_theta * cos_phi * sin_B + sin_theta * cos_B
ny = cos_theta * sin_phi
nz = -cos_theta * cos_phi * cos_B + sin_theta * sin_B
```

### 4. Calculating Shading and Lighting
Here, the code checks the surface normal against a light source vector. It uses a **Z-buffer** to ensure that closer points overwrite points behind them, preventing the back of the donut from bleeding through the front.

\[\frac{1}{z_{\text{new}}} > \frac{1}{z_{\text{existing}}}\]
\[\vec{N} \cdot \vec{L} = (n_x \cdot 0) + (n_y \cdot 1) + (n_z \cdot -1) = n_y - n_z\]

```python
raw_L = (ny - nz) / 1.41421
L = (raw_L + 1.0) / 2.0

if 0 <= xp < SCREEN_WIDTH and 0 <= yp < SCREEN_HEIGHT:
    if ooz > Z_BUFFER[yp][xp]:
        Z_BUFFER[yp][xp] = ooz
        char_index = int(L * (len(ASCII_CHARS) - 1))
        if char_index >= len(ASCII_CHARS):
            char_index = len(ASCII_CHARS) - 1
        SCREEN_BUFFER[yp][xp] = ASCII_CHARS[char_index]
```

### 5. Rendering to the Screen
Finally, the nested loops iterate through the screen buffer grid to blit the text characters frame-by-frame using Pygame.

```python
for y in range(SCREEN_HEIGHT):
    for x in range(SCREEN_WIDTH):
        char_token = SCREEN_BUFFER[y][x]
        if char_token != " ":
            text_surface = font.render(char_token, True, (255, 255, 255))
            screen.blit(text_surface, (x * X_SPACE, y * Y_SPACE))
```
