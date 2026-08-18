import cv2
import numpy as np
import math
import scipy.ndimage as nd


class Snake_base(object):
    def __init__(self, image, primitive_points):
        self.height, self.width = image.shape[0], image.shape[1]

        self.image = image
        self.gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        self.points = primitive_points

        self.min_distance = 5  # Snake两个点之间的最小距离
        self.max_distance = 12  # Snake两个点之间的最大距离

        self.remove_overlapping_points()
        self.add_missing_points()
        self.snake_length = 0

    # 计算两个点之间的距离
    @staticmethod
    def distance(pt1, pt2):
        return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

    # 计算Snake的长度
    def calculate_snake_length(self):
        size = len(self.points)
        return np.sum([Snake_base.distance(self.points[i], self.points[(i + 1) % size]) for i in range(0, size)])

    # 如果两个点距离过近则看作是重叠的点，去除重叠在一起的点
    def remove_overlapping_points(self):
        size = len(self.points)
        i = 0
        while i < size:
            j = (i + 1) % size
            if i == j:
                continue

            curr = self.points[i]
            end = self.points[j]

            dist = Snake_base.distance(curr, end)

            if dist < self.min_distance:
                removal_indices = [j]
                removal_size = 1

                non_remove_size = size - removal_size
                if non_remove_size > removal_size:
                    self.points = [p for k, p in enumerate(self.points) if k not in removal_indices]
                else:
                    self.points = [p for k, p in enumerate(self.points) if k in removal_indices]

                size = len(self.points)
            i += 1

    # def remove_overlapping_points(self):
    #     size = len(self.points)
    #     for i in range(0, size):
    #         for j in range(size-1, i + 1, -1):
    #             if i == j:
    #                 continue
    #
    #             curr = self.points[i]
    #             end = self.points[j]
    #
    #             dist = Snake_base.distance(curr, end)
    #
    #             if dist < self.min_distance:
    #                 if i != 0 and j != size-1:
    #                     removal_indices = range(i+1, j)
    #                     removal_size = len(removal_indices)
    #                 else:
    #                     removal_indices = [j]
    #                     removal_size = 1
    #
    #                 non_remove_size = size - removal_size
    #                 if non_remove_size > removal_size:
    #                     self.points = [p for k, p in enumerate(self.points) if k not in removal_indices]
    #                 else:
    #                     self.points = [p for k, p in enumerate(self.points) if k in removal_indices]
    #
    #                 size = len(self.points)
    #                 break

    # 如果两点距离比较大，则在中间插入新的点
    def add_missing_points(self):
        snake_size = len(self.points)
        for i in range(0, snake_size):
            first_point = self.points[(i + snake_size - 1) % snake_size]
            second_point = self.points[i]
            third_point = self.points[(i + 1) % snake_size]
            fourth_point = self.points[(i + 2) % snake_size]

            if Snake_base.distance(second_point, third_point) > self.max_distance:
                point = first_point * 0.125 / 6 + \
                        second_point * 2.875 / 6 + \
                        third_point * 2.875 / 6 + \
                        fourth_point * 0.125 / 6
                point = np.floor(point + 0.5).astype('int')
                self.points.insert(i + 1, point)
                snake_size += 1

    def update_frame(self):
        # make copy from main image
        new_frame = self.image.copy()

        points_size = len(self.points)
        # line between neighbour points
        for i in range(0, points_size - 1):
            cv2.line(new_frame, tuple(self.points[i]), tuple(self.points[i + 1]),
                    color=(255, 140, 0), thickness=2)

        # line between first and last point
        cv2.line(new_frame, tuple(self.points[0]), tuple(self.points[points_size - 1]),
                color=(255, 140, 0), thickness=2)

        return new_frame

    def step(self):
        pass

