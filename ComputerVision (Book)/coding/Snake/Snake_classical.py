import pdb

import cv2
import numpy as np
import math
import scipy.ndimage as nd
from skimage.util import img_as_float
from skimage.filters import sobel, gaussian
from scipy.interpolate import RectBivariateSpline

from Snake_base import Snake_base


class Snake_classical(Snake_base):
    def __init__(self, image, primitive_points, alpha=0.1, beta=3, gamma=100, wl=0., we=5., wt=0.):
        Snake_base.__init__(self, image, primitive_points)

        self.wl = wl
        self.we = we
        self.wt = wt
        self.alpha = alpha
        self.beta = beta
        self.gamma = 100
        self.kappa = gamma

        self.blurImage = img_as_float(self.gray)
        self.blurImage = gaussian(self.blurImage, 2)
        self.E_ext = self.get_external_energy()

    def get_external_energy(self):
        # 计算外部力 E_line, E_edge, E_term
        E_line = self.blurImage
        E_line = (E_line - np.min(E_line)) / (np.max(E_line) - np.min(E_line))
        # cv2.imshow('line', E_line)

        # 计算 E_edge 利用Sobel算子来获取图像的梯度
        E_edge = sobel(self.blurImage)
        E_edge = (E_edge - np.min(E_edge)) / (np.max(E_edge) - np.min(E_edge))
        # cv2.imshow('edge', E_edge.astype(np.float32))

        # 计算 E_term 端点能量，
        m1 = np.array([-1, 1])
        m2 = np.array([[-1], [1]])
        m3 = np.array([1, -2, 1])
        m4 = np.array([[1], [-2], [1]])
        m5 = np.array([[1, -1], [-1, 1]])

        cx = cv2.filter2D(self.blurImage, -1, m1)
        cy = cv2.filter2D(self.blurImage, -1, m2)
        cxx = cv2.filter2D(self.blurImage, -1, m3)
        cyy = cv2.filter2D(self.blurImage, -1, m4)
        cxy = cv2.filter2D(self.blurImage, -1, m5)

        # pdb.set_trace()
        E_term = (cyy * cx ** 2 - 2 * cxy * cx * cy + cxx * cy ** 2) / ((1.e-4 + cx ** 2 + cy ** 2)**1.5)
        E_term = (E_term - np.min(E_term)) / (np.max(E_term) - np.min(E_term))
        # cv2.imshow('term', E_term.astype(np.float32))

        E_ext = self.wl * E_line + self.we * E_edge + self.wt * E_term
        # cv2.imshow('ext', -E_ext)
        return E_ext

    def step(self):
        # 将point的x，y坐标分开存放
        xs = np.arange(len(self.points) + 1)
        ys = np.arange(len(self.points) + 1)
        for i in range(len(self.points)):
            xs[i] = self.points[i][0]
            ys[i] = self.points[i][1]
        xs[-1] = xs[0]
        ys[-1] = ys[0]

        Map = self.E_ext

        # Interpolate for smoothness
        intp_fn = RectBivariateSpline(
            np.arange(Map.shape[1]),
            np.arange(Map.shape[0]),
            Map.T, kx=2, ky=2, s=0
        )

        # Build finite difference matrices
        n = len(xs)
        A = np.roll(np.eye(n), -1, axis=0) + \
            np.roll(np.eye(n), -1, axis=1) - \
            2 * np.eye(n)  # second order derivative, central difference
        B = np.roll(np.eye(n), -2, axis=0) + \
            np.roll(np.eye(n), -2, axis=1) - \
            4 * np.roll(np.eye(n), -1, axis=0) - \
            4 * np.roll(np.eye(n), -1, axis=1) + \
            6 * np.eye(n)  # fourth order derivative, central difference
        Z = -self.alpha * A + self.beta * B
        Zinv = np.linalg.inv(np.eye(n) + self.gamma * Z)

        fx = intp_fn(xs, ys, dx=1, grid=False)
        fy = intp_fn(xs, ys, dy=1, grid=False)

        xn = np.dot(Zinv, xs + self.gamma * fx)
        yn = np.dot(Zinv, ys + self.gamma * fy)

        dx = self.kappa * np.tanh(xn - xs)
        dy = self.kappa * np.tanh(yn - ys)

        xs += dx.astype(np.int64)
        ys += dy.astype(np.int64)

        new_snake = []
        for i in range(len(xs) - 1):
            new_snake.append(np.array([xs[i], ys[i]]))

        # set new snakes point to points parameter of snake class
        self.points = new_snake
        self.remove_overlapping_points()
        self.add_missing_points()




