import sys
import cv2
import imp
from PyQt5 import QtCore, QtWidgets
import os
import MainWindow
imp.reload(MainWindow)
from MainWindow import Ui_MainWindow
import numpy as np
import pdb
envpath = '/home/x/.conda/envs/ML/lib/python3.9/site-packages/cv2/qt/plugins/platforms'
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = envpath


class ACMWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ACMWindow, self).__init__()
        self.setupUi(self)
        self.selectImageButton.clicked.connect(self.on_click_select_image)
        self.img = None

    def on_click_select_image(self):
        image_path = QtWidgets.QFileDialog.getOpenFileName(None, '选取文件', './', "(*.jpeg);;(*.png);;(*.jpg)")
        self.imageTitleLabel.setText(image_path[0])
        self.imageTitleLabel.show()

        self.img = cv2.imread(image_path[0])
        cv2.imshow('img', self.img)
        self.Snake()

    def Snake(self):
        wl = 1.
        we = 1.
        wt = 1.

        Gaussian_kernel_size = (3, 3)
        Gaussian_sigma = 0.1

        height, width = self.img.shape[0], self.img.shape[1]
        grayImage = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # 计算外部力 E_line,E_edge,
        # 计算 E_line，就是经过高斯平滑后的图像
        pdb.set_trace()
        E_line = cv2.GaussianBlur(grayImage, Gaussian_kernel_size, Gaussian_sigma)

        # 计算 E_edge 利用Sobel算子来获取图像的梯度
        gradx = cv2.Sobel(grayImage, cv2.CV_16S, 1, 0)
        grady = cv2.Sobel(grayImage, cv2.CV_16S, 0, 1)

        E_edge = -np.sqrt(gradx ** 2 + grady ** 2)

        # 计算 E_term 端点能量，
        m1 = np.array([-1, 1])
        m2 = np.array([[-1], [1]])
        m3 = np.array([1, -2, 1])
        m4 = np.array([[1], [-2], [1]])
        m5 = np.array([[1, -1], [-1, 1]])

        cx = cv2.filter2D(grayImage, -1, m1)
        cy = cv2.filter2D(grayImage, -1, m2)
        cxx = cv2.filter2D(grayImage, -1, m3)
        cyy = cv2.filter2D(grayImage, -1, m4)
        cxy = cv2.filter2D(grayImage, -1, m5)

        E_term = (cyy * cx ** 2 - 2 * cxy * cx * cy + cxx * cy ** 2) / (cx ** 2 + cy ** 2)

        # 计算总体的外部能量
        E_ext = (wl * E_line + we * E_edge - wt * E_term)


if __name__ == '__main__':
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    window = ACMWindow()
    window.show()
    sys.exit(app.exec_())