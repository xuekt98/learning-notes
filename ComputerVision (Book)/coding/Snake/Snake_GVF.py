from Snake_base import Snake_base
import cv2
import numpy as np
import math
import scipy.ndimage as nd


class GVF:
    def __init__(self, input_image, mu, times):
        edge_map = input_image
        edge_map = edge_map.astype(np.float64) / 255.0
        self.h, self.w = edge_map.shape

        # get gradiant in x, y direction
        gradient_x = nd.sobel(edge_map, 1)
        gradient_y = nd.sobel(edge_map, 0)

        # set compute gvf parameters
        self.mu = mu
        self.times = times

        gvf_x, gvf_y = self.compute_gvf(gradient_x, gradient_y)

        gvf_mag = (gvf_y ** 2 + gvf_x ** 2)

        # normalize gvf array
        normalized_gvf = gvf_mag / gvf_mag.max()

        self.gvf = np.sqrt(normalized_gvf) * 655000

    def get_gvf(self):
        return self.gvf

    def compute_gvf(self, gradient_x, gradient_y):
        radius = 0.2
        dx = 1.0
        dy = 1.0
        b = gradient_x ** 2.0 + gradient_y ** 2.0
        c, d = b * gradient_x, b * gradient_y
        dt = dx * dy / (radius * self.mu)

        current_u = gradient_x
        current_v = gradient_y

        # iterate for get gvf values based on recursive formula mentioned in paper
        iteration_count = int(max(1, self.times * np.sqrt(self.h * self.w)))
        for i in range(iteration_count):
            next_u = radius * nd.laplace(current_u) + (1.0 - b * dt) * current_u + c * dt
            next_v = radius * nd.laplace(current_v) + (1.0 - b * dt) * current_v + d * dt
            current_u, current_v = next_u, next_v

        return current_u, current_v


class Snake_GVF(Snake_base):
    def __init__(self, image, primitive_points, alpha=3, beta=1.75, mu=0.1):
        Snake_base.__init__(self, image, primitive_points)

        self.SEARCH_KERNEL_SIZE = 5
        self.first_step_points_number = 150
        self.alpha = alpha
        self.average_factor = 0.85
        self.beta = beta
        self.mu = mu
        self.times = 1

        # initialise gvf input image
        gvf_input_image = self.gray.copy()
        gvf_input_image = nd.gaussian_filter(gvf_input_image, .5)
        gvf_input_image = cv2.Canny(gvf_input_image, 75, 150)
        gvf_input_image = cv2.adaptiveThreshold(gvf_input_image,
                                                255,
                                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY,
                                                13,
                                                0)

        self.gvf_input_image = gvf_input_image.copy().astype('float64') / 255.0

        # instantiate gvf and get gvf array
        self.gvf = GVF(self.gvf_input_image, mu=self.mu, times=self.times).get_gvf()

    def step(self):
        self.snake_length = self.calculate_snake_length()

        # initial m, n (viterbi algorithm)
        m = self.SEARCH_KERNEL_SIZE ** 2
        n = len(self.points)

        # make copy from points
        new_snake = self.points.copy()

        # initial energy table and optimum argument
        energy_table = np.zeros((m, n), dtype='int64')
        optimum_argument = np.zeros((m, n), dtype='int64')

        def get_row_col(index):
            size = self.SEARCH_KERNEL_SIZE
            y = index // size
            x = index % size
            return x - size // 2, y - size // 2

        k = self.SEARCH_KERNEL_SIZE // 2
        degree = [i - k for i in range(self.SEARCH_KERNEL_SIZE)]
        grid_x, grid_y = np.meshgrid(degree, degree)
        for k in range(0, n + 1):
            k = k % n
            old_cur = self.points[k]
            old_prev = self.points[(k + len(self.points) - 1) % len(self.points)]
            for i in range(m):
                offset_x, offset_y = get_row_col(i)
                new_cur_x = old_cur[0] + offset_x if old_cur[0] + offset_x >= 0 else 0
                new_cur_x = new_cur_x if old_cur[0] + offset_x <= self.width - 1 else self.width - 1
                new_cur_y = old_cur[1] + offset_y if old_cur[1] + offset_y >= 0 else 0
                new_cur_y = new_cur_y if old_cur[1] + offset_y <= self.height - 1 else self.height - 1

                new_cur = np.array([new_cur_x, new_cur_y])

                def gvf_term(point):
                    return -self.gvf[point[1]][point[0]]

                gvf_energy = gvf_term(new_cur)

                prev_area_x = old_prev[0] + grid_x
                prev_area_y = old_prev[1] + grid_y

                def uniformity_term(point, prev_points_area_x, prev_points_area_y):
                    average_distance = self.snake_length / len(self.points)
                    point_x = point[0]
                    point_y = point[1]
                    return ((point_y - prev_points_area_y) ** 2 +
                            (point_x - prev_points_area_x) ** 2 -
                            self.average_factor * average_distance) ** 2

                uniformity_energy = uniformity_term(new_cur, prev_area_x, prev_area_y)

                energy = self.alpha * uniformity_energy + self.beta * gvf_energy

                last_energy = (energy.ravel() + energy_table[:, k - 1])

                energy_table[i, k] = last_energy.min()
                optimum_argument[i, k] = last_energy.argmin()

        argument = energy_table[:, 0].argmin()

        # build contour based on optimum argument value in O(n)
        for k in range(n + 1):
            k = n - 1 - k
            k = k % n
            old_pt = self.points[k]
            pt_x_offset, pt_y_offset = get_row_col(argument)
            argument = optimum_argument[argument, k]
            new_pt_x = old_pt[0] + pt_x_offset
            new_pt_y = old_pt[1] + pt_y_offset
            new_snake[k] = np.array([new_pt_x, new_pt_y])

        # set new snakes point to points parameter of snake class
        self.points = new_snake

        # remove overlapping points
        self.remove_overlapping_points()

        # add missing points
        self.add_missing_points()
