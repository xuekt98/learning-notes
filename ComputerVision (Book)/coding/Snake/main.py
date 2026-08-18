import cv2
import numpy as np
import math
import scipy.ndimage as nd

from Snake_GVF import Snake_GVF
from Snake_classical import Snake_classical


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
            point = np.array([x, y])
            cv2.circle(self.image, (x, y), 1, (128, 128, 128), 10)
            cv2.imshow('Snakes', self.image)
            self.points.append(point)


def main():
    # read image
    file_to_load = "temp/tasbih.jpg"
    # file_to_load = "temp/2.bmp"
    image = cv2.imread(file_to_load, cv2.IMREAD_COLOR)

    # minimize image
    image = cv2.pyrDown(image)
    copy = image.copy()

    # instantiate click handler
    mouse_handler = ClickHandler(image)

    # set click handler click event method
    cv2.setMouseCallback('Snakes', mouse_handler.click_event)
    cv2.waitKey(0)

    # instantiate snake object
    # snake = Snake_GVF(copy, mouse_handler.get_points())
    snake = Snake_classical(copy, mouse_handler.get_points())
    # snake = Snake_classical_2(copy, mouse_handler.get_points())

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
        snake.step()

        # 5ms delay
        key = cv2.waitKey(100)

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
