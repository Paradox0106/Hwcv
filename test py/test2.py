import sys
from PyQt5.QtWidgets import (QApplication, QMessageBox)
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox)
import os
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     QMessageBox.warning(None, 'my messagebox', 'hello world')


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Button example')
        self.setGeometry(50, 50, 200, 150)

        self.mybutton = QPushButton('Button', self)
        self.mybutton.move(60, 50)
        self.mybutton.clicked.connect(self.onButtonClick)

    def onButtonClick(self):
        reply = QMessageBox.warning(self, 'my messagebox', 'hello world',
            QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
        if reply == QMessageBox.Ok:
            print('Ok clicked.')
            self.mybutton.setText("Ok clicked.")
        else:
            print('Close clicked.')
            self.mybutton.setText("Close clicked.")
    
def delsimilarimg():
        reply=QMessageBox.warning(None, 'my messagebox', 'hello world',QMessageBox.Ok | QMessageBox.Close)
        if reply==QMessageBox.Ok:
            # path = 'D:/python/result/cat1.jpg'
            # os.remove(path)
            print("fuck u")


if __name__ == '__main__':
    delsimilarimg()
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())