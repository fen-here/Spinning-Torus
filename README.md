# Spinning-Torus

Ai was used to understand the math behind the project and help explain the Sudo code for the project. The math implementation was written by me.
I made a donut spin :D

Math behind it:

### defining the torus and the center
$x = (r_1 + R_2 cos0)-cos0$
$y=(R_2+R_1cos0)-sin0$
$z = R_1sin0$

### Spinning the Torus:
$x^1 = x cosB - z sinB$
$z^1 = x sinB + z cosB$

$y^n = y^1 cos A - z^1 sin A$
$z^n = y^1 sin A + z^1 cos A$

### Calculates the points:
$x_screen = center_x + k_1 * x / z$
$y_screen = center_y - K_1 * y / z$

### Shading of the axies:
$N^-> = (cos0-cos0, cos0-sin0,sin0)$

#### Calculating Shading:
$N^->*L^-> = (n_x * 0) +(n_y*1)+(n_z*-1) = n_y - n_z$

#### Calculates the shading and lighting:

$1/z_new > 1/z_existing$
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
