import cv2
import numpy as np
import math
import scipy.ndimage as nd
import matplotlib.pyplot as pp
import pdb


def Snake_old(img, xs, ys):
    wl = 1.
    we = 1.
    wt = 1.
    alpha = 0.5
    beta = 0.5
    gamma = 0.5
    kappa = 0.5

    height, width = img.shape[0], img.shape[1]

    xs = np.arange(100)
    ys = np.arange(100)
    xs = np.cos(xs * np.pi / 50) * 100 + width / 2
    ys = np.cos(ys * np.pi / 50) * 100 + height / 2

    Gaussian_kernel_size = (3, 3)
    Gaussian_sigma = 0.1

    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurImage = cv2.GaussianBlur(grayImage, Gaussian_kernel_size, Gaussian_sigma)

    # 计算外部力 E_line,E_edge,
    # 计算 E_line，就是经过高斯平滑后的图像
    # pdb.set_trace()
    E_line = blurImage

    # 计算 E_edge 利用Sobel算子来获取图像的梯度
    gradx = cv2.Sobel(blurImage, cv2.CV_16S, 1, 0)
    grady = cv2.Sobel(blurImage, cv2.CV_16S, 0, 1)

    E_edge = -np.sqrt(gradx ** 2 + grady ** 2)

    # 计算 E_term 端点能量，
    m1 = np.array([-1, 1])
    m2 = np.array([[-1], [1]])
    m3 = np.array([1, -2, 1])
    m4 = np.array([[1], [-2], [1]])
    m5 = np.array([[1, -1], [-1, 1]])

    cx = cv2.filter2D(blurImage, -1, m1)
    cy = cv2.filter2D(blurImage, -1, m2)
    cxx = cv2.filter2D(blurImage, -1, m3)
    cyy = cv2.filter2D(blurImage, -1, m4)
    cxy = cv2.filter2D(blurImage, -1, m5)

    # 最后加一个很小的常数防止除0的情况发生
    E_term = (cyy * cx ** 2 - 2 * cxy * cx * cy + cxx * cy ** 2) / ((cx ** 2 + cy ** 2)**1.5 + 1.e-4)

    # 计算总体的外部能量
    E_ext = (wl * E_line + we * E_edge - wt * E_term)
    # pdb.set_trace()
    fx = cv2.Sobel(E_ext, -1, dx=1, dy=0, ksize=1, scale=0.5, delta=0, borderType=cv2.BORDER_CONSTANT)
    fy = cv2.Sobel(E_ext, -1, dx=0, dy=1, ksize=1, scale=0.5, delta=0, borderType=cv2.BORDER_CONSTANT)

    xs = xs.T
    ys = ys.T
    m, n = xs.shape[0], 1
    mm, nn = fx.shape[1], fx.shape[0]

    b = np.array([beta, -(alpha+4*beta), 2*alpha+6*beta, -(alpha+4*beta), beta])

    # 计算五对角带状矩阵
    I0 = np.identity(m)
    I0 = np.roll(I0, 2, axis=1)
    A = b[0]*I0

    I1 = np.identity(m)
    I1 = np.roll(I1, 1, axis=1)
    A += b[1]*I1

    I2 = np.identity(m)
    A += b[2]*I2

    I3 = np.identity(m)
    I3 = np.roll(I3, -1, axis=1)
    A += b[3]*I3

    I4 = np.identity(m)
    I4 = np.roll(I4, -2, axis=1)
    A += b[4]*I4

    A = A + gamma*np.identity(m)
    A_inv = np.linalg.pinv(A)

    for i in range(300):
        intFx = cv2.remap(fx, xs, ys, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)
        intFy = cv2.remap(fy, xs, ys, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)

        ssx = gamma * xs - kappa * intFx
        ssy = gamma * ys - kappa * intFy

        xs = A_inv * ssx
        ys = A_inv * ssy
        cv2.circle(img, (xs, ys), radius=2, color=(0,255,0), thickness=2)

        cv2.imshow('result', img)
        cv2.waitKey(30)


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


class Snake:
    # the search kernel size
    SEARCH_KERNEL_SIZE = 5

    # initial points number size
    first_step_points_number = 150

    # uniformity term factors
    alpha = 3
    average_factor = .85

    # gvf term factor
    beta = 1.75

    # gvf camputation factor
    mu = .1
    times = 1

    def __init__(self, image, primitive_points, average_factor):
        self.width = image.shape[1]
        self.height = image.shape[0]

        self.image = image
        self.average_factor = average_factor
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # initialise gvf input image
        gvf_input_image = gray.copy()
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

        # assign input points
        self.points = primitive_points

        # remove overlapping points
        self.remove_overlapping_points()

        # add missing points
        self.add_missing_points()

        self.snake_length = 0

    def calculate_snake_length(self):
        size = len(self.points)
        return np.sum([Snake.distance(self.points[i], self.points[(i + 1) % size]) for i in range(0, size)])

    min_distance = 5

    def remove_overlapping_points(self):
        size = len(self.points)
        for i in range(0, size):
            for j in range(size - 1, i + 1, -1):
                if i == j:
                    continue

                curr = self.points[i]
                end = self.points[j]

                dist = Snake.distance(curr, end)

                if dist < self.min_distance:
                    if i != 0 and j != size - 1:
                        removal_indices = range(i + 1, j)
                        removal_size = len(removal_indices)

                    else:
                        removal_indices = [j]
                        removal_size = 1

                    non_remove_size = size - removal_size
                    if non_remove_size > removal_size:
                        self.points = [p for k, p in enumerate(self.points) if k not in removal_indices]
                    else:
                        self.points = [p for k, p in enumerate(self.points) if k in removal_indices]

                    size = len(self.points)
                    break

    max_distance = 12

    t1 = 0.125 / 6
    t2 = 2.875 / 6
    t3 = 2.875 / 6
    t4 = 0.125 / 6

    def add_missing_points(self):
        snake_size = len(self.points)
        for i in range(0, snake_size):
            first_point = self.points[(i + snake_size - 1) % snake_size]
            second_point = self.points[i]
            third_point = self.points[(i + 1) % snake_size]
            fourth_point = self.points[(i + 2) % snake_size]

            if Snake.distance(second_point, third_point) > self.max_distance:
                point = first_point * self.t1 + \
                        second_point * self.t2 + \
                        third_point * self.t3 + \
                        fourth_point * self.t4

                point = np.floor(point + .5).astype('int')
                self.points.insert(i + 1, point)
                snake_size += 1

    thickness = 1
    lines_color = (0, 255, 255)

    def update_frame(self):
        # make copy from main image
        new_frame = self.image.copy()

        points_size = len(self.points)
        # line between neighbour points
        for i in range(0, points_size - 1):
            cv2.line(new_frame, tuple(self.points[i]), tuple(self.points[i + 1]),
                    self.lines_color, self.thickness)

        # line between first and last point
        cv2.line(new_frame, tuple(self.points[0]), tuple(self.points[points_size - 1]),
                self.lines_color, self.thickness)

        return new_frame

    @staticmethod
    def distance(pt1, pt2):
        return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

    def iterate_using_viterbi(self):
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


class ClickHandler:
    image = None
    POINTS_SIZE = 0

    def __init__(self, image):
        self.image = image
        cv2.putText(self.image, 'Close to start', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 1)
        cv2.imshow('Snakes', image)

        h, w, _ = self.image.shape
        self.counter = 0
        self.points = []

    def get_points(self):
        return self.points

    def click_event(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, y)
            point = np.array([x, y])
            cv2.circle(self.image, (x, y), 5, (0, 0, 0), 10)
            cv2.imshow('Snakes', self.image)
            self.points.append(point)


def main():
    # read image
    file_to_load = "tasbih.jpg"
    image = cv2.imread(file_to_load, cv2.IMREAD_COLOR)

    # minimize image
    # image = cv2.pyrDown(image)
    copy = image.copy()

    # instantiate click handler
    mouse_handler = ClickHandler(image)

    # set click handler click event method
    cv2.setMouseCallback('Snakes', mouse_handler.click_event)
    cv2.waitKey(0)

    # instantiate snake object
    snake = Snake(copy, mouse_handler.get_points(), average_factor=.9)

    # frame array to store frames
    frame_array = []

    while True:
        # update frame / first time get initial frame based on initial values
        new_frame = snake.update_frame()

        # append current frame to frame array
        frame_array.append(new_frame)

        # show current frame
        cv2.imshow('Snake is running ...', new_frame)
        h, w, _ = new_frame.shape

        # iteration
        snake.iterate_using_viterbi()

        # 5ms delay
        key = cv2.waitKey(5)

        # if key = ESC break loop
        if key == 27:
            break

    # instantiate video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('contour.mp4', fourcc, 15, (w, h))

    for i in range(len(frame_array)):
        out.write(frame_array[i])

    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
