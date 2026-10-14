import pygame
import sys
import numpy as np
import math

w, h = 1920, 1080
data = [(0, 0, 0)] * (w * h)
fov = 7
scale = 100
verteces = []
vertecesRaw = []
#triangles = []
splicedLine = []

with open('cube.obj', 'r') as file:
    for line in file:
        if line.startswith("v "):

            splicedLine = line.split()
            x = float(splicedLine[1])
            y = float(splicedLine[2])
            z = float(splicedLine[3])

            vertecesRaw.append([x,y,z])

        elif line.startswith("f "):
            triangles.append(tuple([int(group.split('/')[0]) -1 for group in line.split()[1:]]))

def setPixel(x, y, r, g, b, a=1):
    x, y = int(x), int(y)

    if 0 <= x < w and 0 <= y < h:
        bg = data[y * w + x]
        color = (
            int(r * a + bg[0] * (1 - a)),
            int(g * a + bg[1] * (1 - a)),
            int(b * a + bg[2] * (1 - a)),
        )
        i = y * w + x
        data[i] = color

def createFile():
    with open("out.ppm", "w") as f:
        ppm_body = " ".join(str(value) for pixel in data for value in pixel)
        f.write(f"P3\n{w} {h}\n255\n{ppm_body}\n")

def drawLineAA(x0, y0, x1, y1):
    if abs(y1 - y0) < abs(x1 - x0):
        if x1 < x0:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = y1 - y0
        m = dy / dx if dx != 0 else 0

        for i in range(int(dx) + 1):
            x = x0 + i
            y = y0 + m * i
            ix, iy = int(x), int(y)
            dist = y - iy
            setPixel(ix, iy, 255, 0, 0, 1 - dist)
            setPixel(ix, iy + 1, 255, 0, 0, dist)
    else:
        if y1 < y0:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = y1 - y0
        m = dx / dy if dy != 0 else 0

        for i in range(int(dy) + 1):
            x = x0 + i * m
            y = y0 + i
            ix, iy = int(x), int(y)
            dist = x - ix
            setPixel(ix, iy, 255, 0, 0, 1 - dist)
            setPixel(ix + 1, iy, 255, 0, 0, dist)

def drawLineH(x0, y0, x1, y1):
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    dx = x1 - x0
    dy = y1 - y0

    dir = -1 if dy < 0 else 1
    dy *= dir

    if dx != 0:
        y = y0
        p = 2 * dy - dx
        for i in range(dx + 1):
            setPixel(x0 + i, y, 255, 0, 0, 1)
            if p >= 0:
                y += dir
                p = p - 2 * dx
            p = p + 2 * dy

def drawLineV(x0, y0, x1, y1):
    if y0 > y1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    dy = y1 - y0
    dx = x1 - x0

    dir = -1 if dx < 0 else 1
    dx *= dir

    if dy != 0:
        x = x0
        p = 2 * dx - dy
        for i in range(dy + 1):
            setPixel(x, y0 + i, 255, 0, 0, 1)
            if p >= 0:
                x += dir
                p = p - 2 * dy
            p = p + 2 * dx

def drawLine(x0, y0, x1, y1):
    if abs(x1 - x0) > abs(y1 - y0):
        drawLineH(x0, y0, x1, y1)
    else:
        drawLineV(x0, y0, x1, y1)

def drawTriangle(tx, ty, lx, ly, rx, ry):
    drawLine(lx, ly, rx, ry)
    drawLine(tx, ty, rx, ry)
    drawLine(tx, ty, lx, ly)
    maxX = max(tx, lx, rx)
    maxY = max(ly, ry, ty)
    minX = min(tx,lx,rx)
    minY = min(ly,ry,ty)
    # for height in range(maxY - minY):
    #     for width in range(maxX - minX):
    #          setPixel(width + minX, height + minY, 255, 0, 0)

# FIX 1: Accept rotation angles as parameters
def objToScreen(deg_a, deg_b, deg_c):
    global data, verteces, triangles
    data = [(0, 0, 0)] * (w * h)
    verteces = []
    rad_a = math.radians(deg_a)
    rad_b = math.radians(deg_b)
    rad_c = math.radians(deg_c)

    for a in range(len(vertecesRaw)):
        x = vertecesRaw[a][0]
        y = vertecesRaw[a][1]
        z = vertecesRaw[a][2]

        xyzVector = np.array([[x],[y],[z]])
        rx = np.array([[1,0,0],[0,math.cos(rad_a),-math.sin(rad_a)],[0,math.sin(rad_a),math.cos(rad_a)]])
        ry = np.array([[math.cos(rad_b),0,math.sin(rad_b)],[0,1,0],[-math.sin(rad_b),0,math.cos(rad_b)]])
        rz = np.array([[math.cos(rad_c),-math.sin(rad_c),0],[math.sin(rad_c),math.cos(rad_c),0],[0,0,1]])

        rotated_vector = rz @ ry @ rx @ xyzVector
        x, y, z = rotated_vector.flatten()
        z += 3

        xs = int((w / 2) + ((fov / z) * x) * scale)
        ys = int((h / 2) - ((fov / z) * y) * scale)

        verteces.append((xs, ys))

    for i in range(len(triangles)):
        triangle = triangles[i]
        x1 = verteces[triangle[0]][0]
        y1 = verteces[triangle[0]][1]
        x2 = verteces[triangle[1]][0]
        y2 = verteces[triangle[1]][1]
        x3 = verteces[triangle[2]][0]
        y3 = verteces[triangle[2]][1]
        drawTriangle(x1,y1,x2,y2,x3,y3)

def update_surface():
    surface.fill((0, 0, 0)) # Clear Pygame surface buffer before updating
    for y in range(h):
        for x in range(w):
            color = data[y * w + x]
            if color != (0, 0, 0):
                surface.set_at((x, y), color)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

# --- Pygame Initialization ---
pygame.init()
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Software Renderer Output")
surface = pygame.Surface((w, h))

# Initial Draw
angle_a, angle_b, angle_c = 0, 0, 0
objToScreen(angle_a, angle_b, angle_c)
update_surface()

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # angle_b -= 1
    # objToScreen(angle_a, angle_b, angle_c)
    # update_surface()

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_d:
        #         angle_b -= 10
        #         objToScreen(angle_a, angle_b, angle_c)
        #         update_surface()
        #     if event.key == pygame.K_a:
        #         angle_b += 10
        #         objToScreen(angle_a, angle_b, angle_c)
        #         update_surface()
        #     if event.key == pygame.K_w:
        #         angle_a += 10
        #         objToScreen(angle_a, angle_b, angle_c)
        #         update_surface()
        #     if event.key == pygame.K_s:
        #         angle_a -= 10
        #         objToScreen(angle_a, angle_b, angle_c)
        #         update_surface()
        #     if event.key == pygame.K_e:
        #         angle_c -= 10
        #         objToScreen(angle_a, angle_b, angle_c)
        #         update_surface()
        #     if event.key == pygame.K_q:
        #         angle_c += 10
        #         objToScreen(angle_a, angle_b, angle_c)
        #         update_surface()

    clock.tick(0)

pygame.quit()
sys.exit()
