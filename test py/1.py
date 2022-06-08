from image_similarity_function import *
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from fileinput import filename
import sys
import PyQt5
import click
import cv2 as cv
from cv2 import QT_CHECKBOX
import numpy as np
from matplotlib import image, pyplot as plt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from pyrsistent import PTypeError
from scipy.misc import electrocardiogram
from scipy import ndimage

refPT=[] 
cropping = False
refPTx=[0,0,0,0]
refPTy=[0,0,0,0]
num=0
class Window(QMainWindow):
    def __init__(self,parent=None): #視窗建立
        super().__init__(parent)
        self.setWindowTitle("4a830212_opencv_homework")
        self.resize(1000,800)
        self.intUI()
        self._createActions() 
        self._createMenuBar() #選單分類
        self._connectActions()
        global refPTx,refPTy,num

    def intUI(self):#設定介面ui
        self.picturelabel = QLabel('picture',self)
        self.picturelabel.move(100,100)
        self.picturelabel.setGeometry(QRect(0, 0, 600, 400))

        self.picturelabe2 = QLabel('IeHmAction',self)
        self.picturelabe2.move(100,100)
        self.picturelabe2.setGeometry(QRect(300,100, 600, 400))

        self.picturelabe3 = QLabel('Thresholding',self)
        self.picturelabe3.move(100,100)
        self.picturelabe3.setGeometry(QRect(0, 350, 600, 400))

        self.picturelabe4 = QLabel('filter',self)
        self.picturelabe4.move(100,100)
        self.picturelabe4.setGeometry(QRect(300, 280, 600, 400))

        self.sld=QSlider(Qt.Horizontal,self)
        self.sld.setGeometry(50,600,150,50)
        self.sld.setMinimum(0)
        self.sld.setMaximum(255)
        self.sld.setTickPosition(QSlider.TicksRight)

        self.sldvaluelabel=QLabel("0",self)
        self.sldvaluelabel.move(100,100)
        self.sldvaluelabel.setGeometry(QRect(25, 600, 50, 50))

        self.sld1=QSlider(Qt.Horizontal,self)
        self.sld1.setGeometry(250,600,200,50)
        self.sld1.setMinimum(-360)
        self.sld1.setMaximum(360)
        self.sld1.setTickPosition(QSlider.TicksRight)

        self.sldvaluelabel1=QLabel("0",self)
        self.sldvaluelabel1.move(100,100)
        self.sldvaluelabel1.setGeometry(QRect(225, 600, 50, 50))

        self.Txvaluelabel1=QLabel("Tx:",self)
        self.Txvaluelabel1.move(20, 20)
        self.Txvaluelabel1.setGeometry(QRect(220, 670, 50, 25))

        self.Txtextbox = QLineEdit(self)
        self.Txtextbox.move(20, 20)
        self.Txtextbox.setGeometry(250,670,50,25)

        self.Tyvaluelabel1=QLabel("Ty:",self)
        self.Tyvaluelabel1.move(20, 20)
        self.Tyvaluelabel1.setGeometry(QRect(220, 700, 50, 25))

        self.Tytextbox = QLineEdit(self)
        self.Tytextbox.move(20, 20)
        self.Tytextbox.setGeometry(250,700,50,25)

        self.Sizevaluelabel1=QLabel("圖片縮放:",self)
        self.Sizevaluelabel1.move(20, 20)
        self.Sizevaluelabel1.setGeometry(QRect(25, 700, 50, 25))

        self.Sizextextbox = QLineEdit(self)
        self.Sizextextbox.move(20, 20)
        self.Sizextextbox.setGeometry(90,700,50,25)

        self.Sizeytextbox = QLineEdit(self)
        self.Sizeytextbox.move(20, 20)
        self.Sizeytextbox.setGeometry(150,700,50,25)

        self.affineluelabel1=QLabel("仿射位子\n上X下Y",self)
        self.affineluelabel1.move(20, 20)
        self.affineluelabel1.setGeometry(QRect(350, 670, 100, 50))

        self.affinex1textbox = QLineEdit(self)
        self.affinex1textbox.move(20, 20)
        self.affinex1textbox.setGeometry(400,670,50,25)

        self.affiney1textbox = QLineEdit(self)
        self.affiney1textbox.move(20, 20)
        self.affiney1textbox.setGeometry(400,700,50,25)

        self.affinex2textbox = QLineEdit(self)
        self.affinex2textbox.move(20, 20)
        self.affinex2textbox.setGeometry(460,670,50,25)

        self.affiney2textbox = QLineEdit(self)
        self.affiney2textbox.move(20, 20)
        self.affiney2textbox.setGeometry(460,700,50,25)

        self.affinex3textbox = QLineEdit(self)
        self.affinex3textbox.move(20, 20)
        self.affinex3textbox.setGeometry(520,670,50,25)

        self.affiney3textbox = QLineEdit(self)
        self.affiney3textbox.move(20, 20)
        self.affiney3textbox.setGeometry(520,700,50,25)

        layout = QGridLayout(self)
        layout.addWidget(self.picturelabel, 0, 0, 4, 4)
        layout.addWidget(self.picturelabe2, 0, 0, 4, 4)
        layout.addWidget(self.picturelabe3, 0, 0, 4, 4)

    def _createActions(self):#選單基礎設定
        self.OpenImageAction=QAction(self)
        self.OpenImageAction.setText("&開啟圖片\n(Open_Image)")
        self.ROIAction=QAction("&ROI",self)
        self.IeHmAction=QAction("&圖片直方圖(Image histogram)",self)
        self.grayAction=QAction("&Gray",self)
        self.hsvAction=QAction("&Hsv",self)
        #self.rgbAction=QAction("&Rgb",self)
        self.bgrAction=QAction("&Bgr",self)
        self.ThgAction=QAction("&Thresholding",self)
        self.HmEnAction=QAction("&Histogram Equalization",self)
        self.InfoAction=QAction("&影像資訊(Info)",self)
        self.FHAction=QAction("&垂直翻轉(Horizontal)",self)
        self.FVAction=QAction("&水平翻轉(Vertically)",self)
        self.FLAction=QAction("&向左翻轉(Left)",self)
        self.FRAction=QAction("&向右翻轉(Right)",self)
        self.ATAction=QAction("&仿射轉換(Affine)",self)
        self.MFAction=QAction("&均值濾波(Mean Filtering)",self)
        self.GFAction=QAction("&高斯濾波(Gaussian Filtering)",self)
        self.MBAction=QAction("&中值濾波(MedianBlur)",self)
        self.BFAction=QAction("&雙邊濾波(Bilateral filter)",self)
        #self.LPFAction=QAction("&低通濾波(Low-Pass Filter)",self)
        #self.HPFAction=QAction("&高通濾波(High-Pass Filter)",self)
        self.AGNFAction=QAction("&增加高斯噪點(Add gaussian noise)",self)
        self.SFAction=QAction("&索伯算子(Sobel filter)",self)
        self.LFAction=QAction("&拉普拉斯算子(Laplacian filter)",self)
        self.AFAction=QAction("&平均濾波器(Averaging filter)",self)
        self.ReloadAction=QAction("&重新載入(Reload)",self)
        self.TLAction=QAction("&平移(TransLation)",self)
        self.EDIction=QAction("&邊緣檢測(Edge Detection Image)",self)
        self.EIction=QAction("&影像浮雕(Emboss Image)",self)
        self.RIction=QAction("&Result Image",self)
        self.CSction=QAction("&改變大小",self)
        self.PTction=QAction("&透視投影轉換(Perspective Transform)",self)

    def _createMenuBar(self): #選單設定
        menuBar=self.menuBar()
        fileMenu=QMenu("&檔案(File)",self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.OpenImageAction)
        fileMenu.addAction(self.ReloadAction)
        fileMenu.addAction(self.InfoAction)

        SettingMenu=menuBar.addMenu("&設定(Setting)")#母選單
        SettingMenu.addAction(self.ROIAction)
        SettingMenu.addAction(self.IeHmAction)
        IeHmActionMenu=SettingMenu.addMenu("&色彩空間(IeHmAction)")#子選單
        IeHmActionMenu.addAction(self.grayAction)
        IeHmActionMenu.addAction(self.hsvAction)
        IeHmActionMenu.addAction(self.bgrAction)
        #IeHmActionMenu.addAction(self.rgbAction)
        RotateActionMenu=SettingMenu.addMenu("&旋轉(Rotate)")#旋轉選單
        RotateActionMenu.addAction(self.FHAction)#水平
        RotateActionMenu.addAction(self.FVAction)#垂直
        RotateActionMenu.addAction(self.FLAction)#翻轉90度
        RotateActionMenu.addAction(self.FRAction)#翻轉270度
        SettingMenu.addAction(self.TLAction)#平移
        SettingMenu.addAction(self.ATAction)#仿射轉換
        SettingMenu.addAction(self.CSction)
        SettingMenu.addAction(self.PTction)
     

        ImageMenu=menuBar.addMenu("&Image Processing")
        ImageMenu.addAction(self.ThgAction)
        ImageMenu.addAction(self.HmEnAction)
        FilteringActionMenu=ImageMenu.addMenu("&濾波(Filtering)")
        #FilteringActionMenu.addAction(self.LPFAction)
        #FilteringActionMenu.addAction(self.HPFAction)
        FilteringActionMenu.addAction(self.MFAction)
        FilteringActionMenu.addAction(self.GFAction)
        FilteringActionMenu.addAction(self.MBAction)
        FilteringActionMenu.addAction(self.BFAction)
        FilteringActionMenu.addAction(self.AGNFAction)
        FilteringActionMenu.addAction(self.SFAction)
        FilteringActionMenu.addAction(self.LFAction)
        FilteringActionMenu.addAction(self.AFAction)
        FilteringActionMenu.addAction(self.EIction)
        FilteringActionMenu.addAction(self.EDIction)
        FilteringActionMenu.addAction(self.RIction)

    def _connectActions(self):#按鍵觸發
        self.OpenImageAction.triggered.connect(self.openSlot)
        self.InfoAction.triggered.connect(self.pictureinfo)
        self.ReloadAction.triggered.connect(self.showImage)
        self.ROIAction.triggered.connect(self.Roi_control)
        self.IeHmAction.triggered.connect(self.Histogram)
        self.grayAction.triggered.connect(self.Gray_control)
        self.hsvAction.triggered.connect(self.Hsv_control)
        #self.rgbAction.triggered.connect(self.Rgb_control)
        self.bgrAction.triggered.connect(self.Bgr_control)
        self.ThgAction.triggered.connect(self.Thresholdingcontrol)
        self.HmEnAction.triggered.connect(self.Histogram_Equalization_control)
        self.sld.valueChanged[int].connect(self.changeValue)
        self.sld1.valueChanged[int].connect(self.changeRotaValue)
        self.FHAction.triggered.connect(self.pictureFHflip)
        self.FVAction.triggered.connect(self.pictureFVflip)
        self.FRAction.triggered.connect(self.pictureFRflip)
        self.FLAction.triggered.connect(self.pictureFLflip)
        self.TLAction.triggered.connect(self.PictureTranslation)
        #self.LPFAction.triggered.connect(self.Low_Pass_Filter)
        #self.HPFAction.triggered.connect(self.High_Pass_Filter)
        self.MFAction.triggered.connect(self.Mean_Filtering)
        self.GFAction.triggered.connect(self.Gaussia_Filtering)
        self.MBAction.triggered.connect(self.MedianBlur)
        self.BFAction.triggered.connect(self.Bilateral_filter)
        self.AGNFAction.triggered.connect(self.add_gaussian_noise)
        self.SFAction.triggered.connect(self.sobel_filter)
        self.LFAction.triggered.connect(self.laplacian_filter)
        self.AFAction.triggered.connect(self.averaging_filter)
        self.ATAction.triggered.connect(self.AffineTransform)
        self.EIction.triggered.connect(self.Emboss_Image)
        self.EDIction.triggered.connect(self.Edge_Detection_Image)
        self.CSction.triggered.connect(self.changesize)
        self.PTction.triggered.connect(self.Perspective_transform) 

    def openSlot(self): #載入的圖片
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Image', 'Image', '*.png *.jpg *.bmp')
        if filename is '':
            return
        self.img = cv.imread(filename, -1)
        self.img_path=filename
        if self.img.size == 1:
            return
        self.showImage()

    def showImage(self): #顯示載入的圖片
        height, width, Channel = self.img.shape
        bytesPerline = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.picturelabel.setPixmap(QPixmap.fromImage(self.qImg))
        self.picturelabe3.setPixmap(QPixmap.fromImage(self.qImg))
        
    def Roi_control(self): #ROI
        img = cv.imread(self.img_path)
        roi = cv.selectROI(windowName="ROI", img=img, showCrosshair=False, fromCenter=False)
        x, y, w, h = roi
        cv.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2)
        img_roi = img[int(y):int(y+h), int(x):int(x+w)]
        cv.imshow("roi", img)
        cv.imshow("roi_sel", img_roi)
        cv.waitKey(0)

    def Histogram(self): #影像直方圖
        img = cv.imread(self.img_path)
        plt.hist(img.ravel(), 256, [0, 256])
        plt.show()

    def Gray_control(self): #Gray
        gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        height, width = gray.shape
        bytesPerline = 1 * width
        self.qImg = QImage(gray, width, height, bytesPerline, QImage.Format_Grayscale8).rgbSwapped()
        self.picturelabe2.setPixmap(QPixmap.fromImage(self.qImg))
        self.picturelabe2.resize(self.qImg.size())
    
    # def Rgb_control(self): #Rgb
    #     rgb = cv.cvtColor(self.img, cv.COLOR_BGR2RGB)
    #     height, width, channel = rgb.shape
    #     bytesPerline = 3 * width
    #     self.qImg = QImage(rgb, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
    #     self.picturelabe2.setPixmap(QPixmap.fromImage(self.qImg))
    #     self.picturelabe2.resize(self.qImg.size())

    def Bgr_control(self): #Bgr
        bgr = cv.cvtColor(self.img, cv.COLOR_RGB2BGR)
        height, width, channel = bgr.shape
        bytesPerline = 3 * width
        self.qImg = QImage(bgr, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.picturelabe2.setPixmap(QPixmap.fromImage(self.qImg))
        self.picturelabe2.resize(self.qImg.size())

    def Hsv_control(self): #Hsv
        hsv = cv.cvtColor(self.img, cv.COLOR_BGR2HSV)
        height, width, channel = hsv.shape
        bytesPerline = 3 * width
        self.qImg = QImage(hsv, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.picturelabe2.setPixmap(QPixmap.fromImage(self.qImg))
        self.picturelabe2.resize(self.qImg.size())

    def Thresholdingcontrol(self):
        self.sldvaluelabel.setText(str(self.sld.value()))
        gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        ret, result = cv.threshold(gray, self.sld.value(), 255, cv.THRESH_BINARY)
        height, width = result.shape
        bytesPerline = 1 * width
        self.qimg = QImage(result, width, height, bytesPerline, QImage.Format_Grayscale8).rgbSwapped()
        self.picturelabe3.setPixmap(QPixmap.fromImage(self.qimg))
        self.picturelabe3.resize(self.qimg.size())
    
    def Histogram_Equalization_control (self):
        img = cv.imread(self.img_path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        cv.imshow('Original Image', gray)
        img_eq = cv.equalizeHist(gray)
        cv.imshow('Equalized Image', img_eq)
        plt.hist(gray.ravel(), 256, [0, 256])
        plt.hist(img_eq.ravel(), 256, [0, 256])
        plt.show()

    def changeValue(self,value):
        sender=self.sender()
        if sender==self.sld:
            self.sld.setValue(value)
        else:
            self.sld.setValue(value)
        self.sldvaluelabel.setText(str(value))
        self.Thresholdingcontrol()

    def changeRotaValue(self,value):
        sender=self.sender()
        if sender==self.sld:
            self.sld1.setValue(value)
        else:
            self.sld1.setValue(value)
        self.sldvaluelabel1.setText(str(value))
        self.PictureRotaControl()

    def pictureinfo(self):#圖片資訊
        img = cv.imread(self.img_path)
        size=img.shape
        QMessageBox.information(self,"Picture_info",str(size)+"\n(高度,寬度,像素)")

    def PictureRotaControl(self):#角度調整
        self.sldvaluelabel1.setText(str(self.sld1.value()))
        img = cv.imread(self.img_path)
        height, width, channel = img.shape
        center = (width // 2, height // 2)
        Pictureflip=cv.getRotationMatrix2D(center,self.sld1.value(),1.0)
        Pictureflip = cv.warpAffine(img, Pictureflip, (width, height))
        bytesPerline = 3 * width
        Pictureflip = QImage(Pictureflip.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.picturelabel.setPixmap(QPixmap.fromImage(Pictureflip))

    def pictureFHflip(self): #垂直翻轉
        img = cv.imread(self.img_path)
        Pictureflip = cv.flip(img, 0)
        height, width, channel = img.shape
        bytesPerline = 3 * width
        Pictureflip = QImage(Pictureflip.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.picturelabel.setPixmap(QPixmap.fromImage(Pictureflip))

    def pictureFVflip(self): #水平翻轉
        img = cv.imread(self.img_path)
        Pictureflip = cv.flip(img, 1)
        height, width, channel = img.shape
        bytesPerline = 3 * width
        Pictureflip = QImage(Pictureflip.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.picturelabel.setPixmap(QPixmap.fromImage(Pictureflip))

    def pictureFLflip(self): #左翻翻轉
        img = cv.imread(self.img_path)
        height, width, channel = img.shape
        center = (width // 2, height // 2)
        Pictureflip=cv.getRotationMatrix2D(center,-90,1.0)
        Pictureflip = cv.warpAffine(img, Pictureflip, (width, height))
        bytesPerline = 3 * width
        Pictureflip = QImage(Pictureflip.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.picturelabel.setPixmap(QPixmap.fromImage(Pictureflip))
         
    def pictureFRflip(self): #右翻翻轉
        img = cv.imread(self.img_path)
        height, width, channel = img.shape
        center = (width // 2, height // 2)
        Pictureflip = cv.getRotationMatrix2D(center,90,1.0)
        Pictureflip = cv.warpAffine(img, Pictureflip, (width, height))
        bytesPerline = 3 * width
        Pictureflip = QImage(Pictureflip.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.picturelabel.setPixmap(QPixmap.fromImage(Pictureflip))

    def PictureTranslation(self):#平移
        img = cv.imread(self.img_path)
        rows, cols = img.shape[:2]
        affine = np.float32([[1, 0, int(self.Txtextbox.text())], [0, 1, int(self.Tytextbox.text())]])
        dst = cv.warpAffine(img, affine, (cols, rows))
        cv.imshow("original", img)
        cv.imshow("Translation", dst)
    
    # def Low_Pass_Filter(self):
    #     img = cv.imread(self.img_path)
    #     #self.showpicturea(g_hpf,img)

    # def High_Pass_Filter(self):
    #     img = cv.imread(self.img_path,cv.COLOR_BGR2GRAY)
    #     img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #     GBlur=cv.GaussianBlur(img_gray,(5,5),0)
    #     g_hpf=img_gray-GBlur
    #     self.showpicturea(g_hpf,img)

    def Mean_Filtering(self):#均值濾波 blur() boxFilter()
        img = cv.imread(self.img_path,cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_Mean=cv.blur(img_gray,(5,5))
        self.showpicturea(img_Mean,img)
        
    def Gaussia_Filtering(self):#高斯濾波
        img = cv.imread(self.img_path,cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_Gaussia=cv.GaussianBlur(img_gray,(11,11),-1)
        self.showpicturea(img_Gaussia,img)
    
    def MedianBlur(self):#中值濾波
        img = cv.imread(self.img_path,cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_median = cv.medianBlur(img_gray, 7)
        self.showpicturea(img_median,img)
    
    def Bilateral_filter(self):
        img = cv.imread(self.img_path,cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_Gaussia=cv.GaussianBlur(img_gray,(5,5),9)
        img_Bilateral=cv.bilateralFilter(img_Gaussia,10,10,10)
        self.showpicturea(img_Bilateral,img)

    def add_gaussian_noise(self):#增加高斯噪點
        img = cv.imread(self.img_path,cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = img / 255
        mean = 0
        sigma = 0.2
        noise = np.random.normal(mean, sigma, img.shape)
        img_gaussian = img + noise
        img_gaussian = np.clip(img_gaussian, 0, 1)
        img_gaussian = np.uint8(img_gaussian * 255)
        noise = np.uint8(noise * 255)
        cv.imshow('Gaussian noise', noise)
        cv.imshow('noised image', img_gaussian)
        #median_filter(img_gaussian)
        img_result = cv.fastNlMeansDenoising(img_gaussian, None, 10, 10, 7)
        cv.imshow('fast denoise', img_result)

    def Emboss_Image(self): #影像浮雕
        img = cv.imread(self.img_path,cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        kernel = np.array([[-2, -1, 0],[-1, 1, 1],[0, 1, 2]])
        img_result = cv.filter2D(img_gray, -1, kernel)
        self.showpicturea(img_result,img)

    def Edge_Detection_Image(self): #邊緣檢測
        img = cv.imread(self.img_path,cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        kernel = np.array([[-1, -1, -1],[-1, 8, -1],[-1, -1, -1]])
        img_result = cv.filter2D(img_gray, -1, kernel)
        self.showpicturea(img_result,img)

    def Result_Image(self):
        img = cv.imread(self.img_path,cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        kernel = np.ones((7, 7), np.float32) / 49
        img_result = cv.filter2D(img_gray, -1, kernel)
        self.showpicturea(img_result,img)

    def sobel_filter(self):#索伯算子
        img = cv.imread(self.img_path,cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        x = cv.Sobel(img_gray, cv.CV_16S, 1, 0)
        y = cv.Sobel(img_gray, cv.CV_16S, 0, 1)
        abs_x = cv.convertScaleAbs(x)
        abs_y = cv.convertScaleAbs(y)
        img_sobel = cv.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
        cv.imshow('x-direction gradient image', abs_x)
        cv.imshow('y-direction gradient image', abs_y)
        cv.imshow('sobel image', img_sobel)

    def averaging_filter(self):#平均濾波器
        img = cv.imread(self.img_path,cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img_averaging = cv.blur(img_gray, (5, 5))
        self.showpicturea(img_averaging,img)

    def laplacian_filter(self):#拉普拉斯算子
        img = cv.imread(self.img_path,cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray_lap = cv.Laplacian(img_gray, cv.CV_16S, ksize=5)
        img_laplacian = cv.convertScaleAbs(gray_lap)
        self.showpicturea(img_laplacian,img)

    def showpicturea(self,img,or_img):
        height, width, channel = or_img.shape
        bytesPerline = 1 * width
        img = QImage(img.data, width, height, bytesPerline, QImage.Format_Grayscale8).rgbSwapped()
        self.picturelabe4.setPixmap(QPixmap.fromImage(img))

    def changesize(self):
        img = cv.imread(self.img_path)
        rows, cols, ch = img.shape
        img_res = cv.resize(img, None, fx=(float(self.Sizextextbox.text())), fy=(float(self.Sizeytextbox.text())), interpolation=cv.INTER_CUBIC)
        cv.imshow('resize image', img_res)

    def AffineTransform(self):
        img = cv.imread(self.img_path,cv.COLOR_BGR2GRAY)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        rows, cols, ch = img.shape
        pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
        pts2 = np.float32([[int(self.affinex1textbox.text()), int(self.affiney1textbox.text())], [int(self.affinex2textbox.text()), int(self.affiney2textbox.text())], [int(self.affinex3textbox.text()), int(self.affiney3textbox.text())]])
        M = cv.getAffineTransform(pts1, pts2)
        img_aff = cv.warpAffine(img, M, (cols, rows))
        cv.imshow('affine image', img_aff)

    def OnMouseAction(self,event,x,y,flags,param):
        global refPT,cropping,num
        refPT=[(x,y)]
        if event==cv.EVENT_LBUTTONDOWN:
            refPT.append((x, y))
            if num<4:
                refPTx[num]=x
                refPTy[num]=y
            print(str(refPT)+str(num)+' '+str(refPTx[num])+" "+str(refPTy[num]))
            num=num+1
            cropping = True  
        elif event == cv.EVENT_LBUTTONUP:
            cropping = False
            

    def Perspective_transform(self):
        img = cv.imread(self.img_path)
        height, width, channel = img.shape
        cv.namedWindow("Perspective")
        cv.setMouseCallback("Perspective", self.OnMouseAction)
        while True:
            cv.imshow("Perspective",img)
            key = cv.waitKey(1) & 0xFF
            if key==ord("c"):
                break
            
        pts1=np.float32([[refPTx[0],refPTy[0]],[refPTx[1],refPTy[1]],[refPTx[2],refPTy[2]],[refPTx[3],refPTy[3]]])
        pts2=np.float32([[0,0],[300,0],[300,300],[0,300]])
        M=cv.getPerspectiveTransform(pts1,pts2)
        dst=cv.warpPerspective(img,M,(300,300))
        cv.imshow('Perspective',dst)
        # i=0
        # while i<4:
        #     refPTx[i]=0
        #     refPTy[i]=0

# 融合相似度阈值
threshold1=0.85
# 最终相似度较高判断阈值
threshold2=0.98


# 融合函数计算图片相似度
def calc_image_similarity(img1_path,img2_path):
    """
    :param img1_path: filepath+filename
    :param img2_path: filepath+filename
    :return: 图片最终相似度
    """

    similary_ORB=float(ORB_img_similarity(img1_path,img2_path))
    similary_phash=float(phash_img_similarity(img1_path,img2_path))
    similary_hist=float(calc_similar_by_path(img1_path, img2_path))
    # 如果三种算法的相似度最大的那个大于0.85，则相似度取最大，否则，取最小。
    max_three_similarity=max(similary_ORB,similary_phash,similary_hist)
    min_three_similarity=min(similary_ORB,similary_phash,similary_hist)
    if max_three_similarity>threshold1:
        result=max_three_similarity
    else:
        result=min_three_similarity

    return round(result,3)

def opendir():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    print(file_path)

if __name__ == '__main__':
    # 搜索图片路径和文件名
    img1_path='F:/img_spam/data/train/unqrcode/10064003003550210800320010011888.jpg'
    
    # 搜索文件夹
    filepath='F:/img_spam/data/train/unqrcode/'
    
    # 相似图片存放路径
    newfilepath='F:/img_spam/4/第九组/'
    
    for parent, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            # print(filepath+filename)
            img2_path=filepath+filename
            kk=calc_image_similarity(img1_path,img2_path)
    
            try:
                if kk>=threshold2:
                    print(img2_path,kk)
                    shutil.copy(img2_path,newfilepath)
            except Exception as e:
                # print(e)
                pass        

    app=QApplication(sys.argv)
    win=Window()
    win.show()
    sys.exit(app.exec_())        
