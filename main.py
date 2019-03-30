# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 20:39:58 2019

@author: 肖映泰
"""

from weather_info import Weather
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QLabel, QTextEdit, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QLineEdit


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = '国内城市温度信息查询程序'
        self.left = 200
        self.top = 200
        self.width = 900
        self.height = 550

        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # create label
        self.label = QLabel("请输入城市名", self)
        self.label.move(10, 10)
        
        # create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(10, 40)
        self.textbox.resize(180, 40)

        # create a button in the window
        self.button = QPushButton('查询', self)
        self.button.move(10, 100)
        self.button.resize(50, 40)
        
        # create a label and a text to show temperature information
        self.label_temp = QLabel("温度信息", self)
        self.label_temp.move(450, 10)
        
        self.txt_temp = QTextEdit('', self)
        self.txt_temp.move(450, 40)
        self.txt_temp.resize(250, 40)
        
        # create two labels to show 24 hours temperature information
        self.label_day = QLabel("最近 24 hours 温度曲线", self)
        self.label_day.move(10, 150)
        
        self.lb_pic_day = QLabel(self)
        self.lb_pic_day.setGeometry(10, 200, 400, 300)
        
        # create two labels to show 6 days temperature information
        self.label_week = QLabel("未来 6 days 温度曲线", self)
        self.label_week.move(450, 150)
        
        self.lb_pic_week = QLabel(self)
        self.lb_pic_week.setGeometry(450, 200, 400, 300)
        
        self.clean = QPushButton("清除", self)
        self.clean.move(100, 100)
        self.clean.resize(50, 40)
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.clean.clicked.connect(self.on_clear)

    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        weather = Weather(textboxValue)
        if weather.data['error_code'] == 0:
            # get the temperature for the time being
            info_now = weather.data_now
            self.txt_temp.setText(textboxValue + "当前温度为"
                                  + ": " + info_now['now_temperature'])
            
            # get the temperature distribution in 24 hours
            weather.day_temp()
            pix_day = QPixmap('day_temp.png')
            self.lb_pic_day.setPixmap(pix_day)
            self.lb_pic_day.setScaledContents(True)
            
            # get the temperature distribution in 7 days
            weather.week_temp()
            pix_week = QPixmap('week_temp.png')
            self.lb_pic_week.setPixmap(pix_week)
            self.lb_pic_week.setScaledContents(True)
        
        # if the search was not successful
        else:
            QMessageBox.question(self, "Error", weather.data['reason']+"，请重试",
                                 QMessageBox.Ok, QMessageBox.Ok)
            self.on_clear()
        # delete the text in the textbox
        self.textbox.setText('')
        
    @pyqtSlot()
    def on_clear(self):
        self.txt_temp.setText('')
        self.lb_pic_day.setPixmap(QPixmap(''))
        self.lb_pic_week.setPixmap(QPixmap(''))
        self.textbox.setText('')
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    app.exit(app.exec_())
