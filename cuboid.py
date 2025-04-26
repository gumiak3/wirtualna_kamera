import numpy as np
import math

class Cubiod:

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # przednia dolna ścianka
        (4, 5), (5, 6), (6, 7), (7, 4),  # tylna górna ścianka
        (0, 4), (1, 5), (2, 6), (3, 7),  # “pionowe” krawędzie
    ]

    def __init__(self, verticles: list[list[float]], screen: list[float]):
        self.vertices = np.array(verticles)
        self.prime_verices = np.array(verticles)
        self.screen_width, self.screen_height = screen

    def reset(self):
        self.vertices = self.prime_verices.copy()

    def translation_matrix(self, tx, ty, tz):
        return np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])

    def rotation_matrix_axis_x(self, angle):
        return np.array([
            [1, 0, 0, 0],
            [0, math.cos(angle), -math.sin(angle), 0 ],
            [0, math.sin(angle), math.cos(angle), 0 ],
            [0, 0, 0, 1]
        ])

    def rotation_matrix_axis_y(self, angle):
        return np.array([
            [math.cos(angle), 0, math.sin(angle), 0],
            [0, 1, 0, 0],
            [-math.sin(angle), 0, math.cos(angle), 0],
            [0, 0, 0, 1]
        ])

    def scale_matrix(self, sx, sy, sz):
        return np.array([
            [sx,  0,  0, 0],
            [ 0, sy,  0, 0],
            [ 0,  0, 1, 0],
            [ 0,  0,  0, 1],
        ])

    def rotation_matrix_axis_z(self, angle):
        return np.array([
            [math.cos(angle), -math.sin(angle), 0, 0],
            [math.sin(angle), math.cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

    def zoom(self, zoom):
        scale_matrix = self.scale_matrix(zoom, zoom, zoom)
        self.vertices = self.vertices.dot(scale_matrix.T)

    def translation(self, camera_pos: list[float]):
        translation_matrix = self.translation_matrix(camera_pos[0], camera_pos[1], camera_pos[2])

        self.vertices = self.vertices.dot(translation_matrix.T)

    def rotate(self, axis, angle):
        if(axis == 'x'):
            rotation_matrix = self.rotation_matrix_axis_x(angle)
            self.vertices = self.vertices.dot(rotation_matrix.T)
        elif(axis == 'y'):
            rotation_matrix = self.rotation_matrix_axis_y(angle)
            self.vertices = self.vertices.dot(rotation_matrix.T)
        elif(axis == 'z'):
            rotation_matrix = self.rotation_matrix_axis_z(angle)
            self.vertices = self.vertices.dot(rotation_matrix.T)

    def project(self, f = 100):
        cx = self.screen_width / 2
        cy = self.screen_height / 2
        projected = []
        for x, y, z, w in self.vertices:
            if z <= 0:
                z = 1e-6

            x_ndc = (x * f) / z
            y_ndc = (y * f) / z

            screen_x = int(cx + x_ndc)
            screen_y = int(cy - y_ndc)

            projected.append([screen_x, screen_y])

        return projected