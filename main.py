import pygame
import load_data
from cuboid import Cubiod

# pygame setup
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
FOV = 256
CAM_DIST = 2
COLOR = (0,0,0)

camera_pos = [0, 0, 0]
STEP = 0.1
ANGLE = 0.02
ZOOM = 1.2

cuboids_vertices_data = load_data.load_data('data.json')

cuboids: Cubiod = []
for cuboid_vertices in cuboids_vertices_data:
    cuboids.append(Cubiod(cuboid_vertices['vertices'], [width, height]))


def translation_cuboids(camera_pos: list[float], cuboids):
    for cuboid in cuboids:
        cuboid.translation(camera_pos)

def rotate_cuboids(angle, cuboids, axis):
    for cuboid in cuboids:
        cuboid.rotate(axis , angle)

def zoom_cuboids(zoom, cuboids):
    for cuboid in cuboids:
        cuboid.zoom(zoom)

def cuboids_reset():
    for cuboid in cuboids:
        cuboid.reset()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                zoom_cuboids(ZOOM, cuboids)
            elif event.y < 0:
                zoom_cuboids(1/ZOOM, cuboids)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        camera_pos[0] += STEP
    elif keys[pygame.K_d]:
        camera_pos[0] -= STEP
    elif keys[pygame.K_w]:
        camera_pos[1] -= STEP
    elif keys[pygame.K_s]:
        camera_pos[1] += STEP
    elif keys[pygame.K_UP]:
        rotate_cuboids(ANGLE, cuboids, 'x')
    elif keys[pygame.K_DOWN]:
        rotate_cuboids(-ANGLE, cuboids, 'x')
    elif keys[pygame.K_LEFT]:
        rotate_cuboids(ANGLE, cuboids, 'y')
    elif keys[pygame.K_RIGHT]:
        rotate_cuboids(-ANGLE, cuboids, 'y')
    elif keys[pygame.K_q]:
        camera_pos[2] = -STEP
    elif keys[pygame.K_e]:
        camera_pos[2] = STEP
    elif keys[pygame.K_z]:
        rotate_cuboids(-ANGLE, cuboids, 'z')
    elif keys[pygame.K_x]:
        rotate_cuboids(ANGLE, cuboids, 'z')
    elif keys[pygame.K_r]:
        cuboids_reset()


    translation_cuboids(camera_pos, cuboids)
    camera_pos = [0, 0, 0]

    screen.fill('white')
    for cuboid in cuboids:
        vertices = cuboid.vertices
        lines = cuboid.edges

        for i, j in lines:
            clipped = cuboid.clip_edge(vertices[i], vertices[j])

            if clipped is None:
                continue  # Obie strony za kamerą — nie rysujemy

            p1, p2 = clipped

            start = cuboid.project_point(p1)
            end = cuboid.project_point(p2)

            pygame.draw.line(screen, COLOR, start, end, 2)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()