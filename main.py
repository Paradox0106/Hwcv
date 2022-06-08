
import imp
import string

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
from PIL import ImageQt
from PyQt5 import QtCore, QtWidgets

from image_similarity_function import *
# 融合相似度閥值
threshold1=0.85
# 判斷值
threshold2=0.98
# global_filepath=''
# global_newfilepath=''
# global_imagepath=''

global_filepath='D:/python/test'
global_newfilepath='D:/python/result'
global_imagepath='D:/python/cat.jpg'

similar_img_list=[]
similar_img_thval=[]

class Window(QMainWindow):

    def __init__(self,parent=None): 
        super().__init__(parent)
        self.setWindowTitle("opencvhw")
        self.resize(1280,1024)
        self.initUI()
        self.threshold_value()
    def initUI(self):
        btn_open = QPushButton('openimage', self)
        btn_open.move(500, 950)
        btn_open.clicked.connect(self.openimg)

        btn_opendir = QPushButton('opendir', self)
        btn_opendir.move(600, 950)
        btn_opendir.clicked.connect(self.opendir)

        btn_opennewdir = QPushButton('opennewdir', self)
        btn_opennewdir.move(700, 950)
        btn_opennewdir.clicked.connect(self.opennewdir)

        btn_search = QPushButton('search', self)
        btn_search.move(800, 950)
        btn_search.clicked.connect(imgsearch)

        btn_search = QPushButton('imgcompare', self)
        btn_search.move(900, 950)
        btn_search.clicked.connect(imgcompare)

        #img
        self.picturelabel = QLabel('1',self)
        self.picturelabel.setGeometry(QRect(0, 0, 600, 400))

        #similar img
        global similarimg
        similarimg = QLabel('2',self)
        similarimg.setGeometry(QRect(425, 0, 600, 400))

        
        self.dirlabel=QLabel("dir path:"+global_newfilepath,self)
        self.dirlabel.setGeometry(QRect(600, 850, 500, 25))

        self.newdirlabel=QLabel("save dir path:"+global_newfilepath,self)
        self.newdirlabel.setGeometry(QRect(600, 900, 500, 25))
        
        global currimg
        currimg=QLabel("search:",self)
        currimg.setGeometry(QRect(800, 900, 500, 25))



    def threshold_value(self):
        self.currvaluelabel=QLabel("threshold value:",self)
        self.currvaluelabel.setGeometry(QRect(125, 900, 100, 25))

        global currvaluelabelmix
        currvaluelabelmix=QLabel("0.85",self)
        currvaluelabelmix.setGeometry(QRect(225, 900, 50, 25))

        global currvaluelabeljudg
        currvaluelabeljudg=QLabel("0.98",self)
        currvaluelabeljudg.setGeometry(QRect(275, 900, 50, 25))
        
        self.valuelabel1=QLabel("change threshold value:",self)
        self.valuelabel1.setGeometry(QRect(125, 950, 125, 25))

        #value for mix
        self.threshold_value_mix = QLineEdit("0.85",self)
        self.threshold_value_mix.setGeometry(250,950,50,25)
        #value for judgment
        self.threshold_value_judgment = QLineEdit("0.98",self)
        self.threshold_value_judgment.setGeometry(305,950,50,25)

        btn_chg_val = QPushButton('change threshold value', self)
        btn_chg_val.setGeometry(250,985,150,30)
        btn_chg_val.clicked.connect(self.change_threshold_value)

    def change_threshold_value(self):
        global threshold1
        global threshold2
        threshold1=float(self.threshold_value_mix.text())
        threshold2=float(self.threshold_value_judgment.text())
        currvaluelabelmix.setText(str(threshold1))
        currvaluelabeljudg.setText(str(threshold2))


    def opendir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None,"選取資料夾") # 起始路徑
        #self.fileT.setText(directory)
        self.dirlabel.setText("dir path:"+directory)
        global global_filepath
        global_filepath=directory
        print(type(directory))
        print(global_filepath)
        

    

    def opennewdir(self):
        print("global_filepath:"+global_filepath)
        directory = QtWidgets.QFileDialog.getExistingDirectory(None,"選取資料夾") # 起始路徑
        global global_newfilepath
        global_newfilepath=directory
        self.newdirlabel.setText("save dir path:"+global_newfilepath)
        print(directory)
        print(global_newfilepath)

    def openimg(self): #載入的圖片
                                                        #標題 圖片預設名稱 圖片類型
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Image', 'Image', '*.png *.jpg *.bmp')
        if filename is '':
            return
        self.img = cv.imread(filename, -1)
        self.img_path=filename
        global global_imagepath
        global_imagepath=filename

        if self.img.size == 1:
            return
        self.showImage()    
    def showImage(self): #顯示載入的圖片
        height, width, Channel = self.img.shape
        bytesPerline = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerline, QImage.Format.Format_RGB888).rgbSwapped()
        self.picturelabel.setPixmap(QPixmap.fromImage(self.qImg))
   
    
    
    
     
    """
    :param img1_path: filepath+filename
    :param img2_path: filepath+filename
    :return: 圖片最終相似度
    """
def calc_image_similarity(img1_path,img2_path):
    

    similary_ORB=float(ORB_img_similarity(img1_path,img2_path))
    similary_phash=float(phash_img_similarity(img1_path,img2_path))
    similary_hist=float(calc_similar_by_path(img1_path, img2_path))
    # 如果三種算法中 相似度最大的>所設定閥值 則取最大 否則取最小
    max_three_similarity=max(similary_ORB,similary_phash,similary_hist)
    min_three_similarity=min(similary_ORB,similary_phash,similary_hist)
    if max_three_similarity>threshold1:
        result=max_three_similarity
    else:
        result=min_three_similarity

    return round(result,3)
    

def imgsearch():
    img1_path=global_imagepath
    
    filepath=global_filepath
    
    newfilepath=global_newfilepath

    for _,_,filenames in os.walk(filepath):
        for filename in filenames:
            #print(filepath+filename)
            img2_path=filepath+"/"+filename
            kk=calc_image_similarity(img1_path,img2_path)
            
            try:
                if kk>=threshold2:
                    print(img2_path,kk)
                    shutil.copy(img2_path,newfilepath)
            except Exception as e:
                print(e)
                pass
    try:
        txtresult=open(newfilepath+'/result.txt','w')
        print(txtresult.write('{}'.format("result img:")))
        print(txtresult.write('{}'.format(similar_img_list)))
        print(txtresult.write('{}'.format("\nimg similar rate:")))
        print(txtresult.write('{}'.format(similar_img_thval)))
        QMessageBox.information(None,'Result','Result txt in:'+newfilepath)
        txtresult.close()
    except Exception as e:
        print(e)        
def imgcompare():
    img1_path=global_imagepath
    filepath=global_filepath
    newfilepath=global_newfilepath
    global similar_img_list,similar_img_thval

    for _,_,filenames in os.walk(filepath):
        for filename in filenames:
            img2_path=filepath+"/"+filename
            kk=calc_image_similarity(img1_path,img2_path)
            
            try:
                currimg.setText("search:"+img2_path)
                if kk >= 0.01:
                    similar_img_list.append(img2_path)
                    similar_img_thval.append(kk)
                if kk>=threshold2:
                    print(img2_path,kk)
                    open_similar_img(img2_path)
                    delsimilarimg(img2_path,kk)


                    

                
            except Exception as e:
                print(e)
                pass
    try:
        txtresult=open(newfilepath+'/result.txt','w')
        print(txtresult.write('{}'.format("result img:")))
        print(txtresult.write('{}'.format(similar_img_list)))
        print(txtresult.write('{}'.format("\nimg similar rate:")))
        print(txtresult.write('{}'.format(similar_img_thval)))
        QMessageBox.information(None,'Result','Result txt in:'+newfilepath)
        txtresult.close()
    except Exception as e:
        print(e)

    
    similar_img_list=[]
    similar_img_thval=[]

def delsimilarimg(img2_path,kk):
    reply=QMessageBox.warning(None, 'Similar image', 'Do u want to del similar img '+img2_path+" ?",QMessageBox.Ok | QMessageBox.Close)
    global similar_img_list
    global similar_img_thval
    if reply == QMessageBox.Ok:
        path = img2_path
        os.remove(path)
        QMessageBox.warning(None, 'Remove', 'Remove '+img2_path)
    elif reply == QMessageBox.Close:
        pass
        




def open_similar_img(similarimg_name):
    filename = similarimg_name
    if filename is '':
        return
    img = cv.imread(filename, -1)
    img_path=filename
    global global_imagepath
    global_imagepath=filename
    if img.size == 1:
        return  
        
    height, width,Channel  = img.shape
    bytesPerline = 3 * width
    qImg = QImage(img.data, width, height, bytesPerline, QImage.Format.Format_RGB888).rgbSwapped()
    similarimg.setPixmap(QPixmap.fromImage(qImg))


if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=Window()
    win.show()
    sys.exit(app.exec_())        
    