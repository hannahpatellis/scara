## This is the main ScARA Panel application. Execute this to run the application
## This includes the UI and handling of commands from the Server
## Written by Hannah A. Patellis - hannahap.com - @hannahpatellis

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow)
from PyQt5.QtCore import QProcess
import os
from threading import Timer
import time
import json

dir_path = os.path.dirname(os.path.realpath(__file__))

class Ui_MainWindow(QMainWindow):

    global scenes
    global clients
    global currentRoom
    global currentSceneList
    currentSceneList = dict()

    def __init__(self):
        QMainWindow.__init__(self)

        self.setupUi(self)

    ## Establish user interface
    def setupUi(self, MainWindow):
        ## Initial setup
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 320)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("color:#FFF;\n"
                                 "background:none;")
        self.master_window = QtWidgets.QWidget(MainWindow)
        self.master_window.setObjectName("master_window")
        ## Top bar
        self.topbar = QtWidgets.QWidget(self.master_window)
        self.topbar.setGeometry(QtCore.QRect(0, 0, 480, 51))
        self.topbar.setStyleSheet("background:#1c1c1c;")
        self.topbar.setObjectName("topbar")
        self.time = QtWidgets.QLabel(self.topbar)
        self.time.setGeometry(QtCore.QRect(10, 8, 321, 23))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(17)
        font.setWeight(60)
        self.time.setFont(font)
        self.time.setStyleSheet("color:white;\n"
                                "background:none;")
        self.time.setObjectName("time")
        self.date = QtWidgets.QLabel(self.topbar)
        self.date.setGeometry(QtCore.QRect(10, 28, 261, 18))
        self.date.setStyleSheet("color:white;\n"
                                "background:none;")
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(12)
        font.setWeight(60)
        self.date.setFont(font)
        self.date.setObjectName("date")
        self.micbox = QtWidgets.QWidget(self.topbar)
        self.micbox.setGeometry(QtCore.QRect(430, 0, 51, 51))
        self.micbox.setStyleSheet("background:#424242;")
        self.micbox.setObjectName("micbox")
        self.mic = QtWidgets.QLabel(self.micbox)
        self.mic.setGeometry(QtCore.QRect(16, 5, 21, 41))
        self.mic.setText("")
        self.mic.setPixmap(QtGui.QPixmap(dir_path+"/static/mic.png"))
        self.mic.setObjectName("mic")
        self.mic.mouseReleaseEvent = self.micClick
        ## Tabs
        self.tabs = QtWidgets.QTabWidget(self.master_window)
        self.tabs.setGeometry(QtCore.QRect(-1, 49, 482, 271))
        self.tabs.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabs.setAutoFillBackground(False)
        self.tabs.setStyleSheet("QTabWidget::pane {\n"
                                "    margin:0px;\n"
                                "    padding:0px;\n"
                                "}\n"
                                "QTabWidget::tab-bar {\n"
                                "    alignment: center;\n"
                                "}\n"
                                "QTabBar::tab {\n"
                                "    border-top: 2px solid white;\n"
                                "    border-bottom: 2px solid white;\n"
                                "    border-right: 2px solid white;\n"
                                "    padding: 0px;\n"
                                "    margin-top:0px;\n"
                                "    margin-left:0px;\n"
                                "    margin-bottom:0px;\n"
                                "}\n"
                                "QTabBar::tab::first {\n"
                                "    padding: 0px;\n"
                                "    margin-bottom:0px;\n"
                                "    margin-left:0px;\n"
                                "}\n"
                                "QTabBar::tab::last {\n"
                                "    border-right:none;\n"
                                "    padding: 0px;\n"
                                "    margin-bottom:0px;\n"
                                "    margin-left:0px;\n"
                                "}\n"
                                "QTabBar::tab::selected {\n"
                                "    background:white;\n"
                                "}")
        self.tabs.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabs.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabs.setIconSize(QtCore.QSize(79, 40))
        self.tabs.setElideMode(QtCore.Qt.ElideRight)
        self.tabs.setUsesScrollButtons(False)
        self.tabs.setDocumentMode(False)
        self.tabs.setTabsClosable(False)
        self.tabs.setMovable(False)
        self.tabs.setObjectName("tabs")
        ## Home Tab
        self.home = QtWidgets.QWidget()
        self.home.setStyleSheet(
            "background:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(0, 113, 188, 255), stop:1 rgba(212, 20, 90, 255));")
        self.home.setObjectName("home")
        self.floorplan = QtWidgets.QLabel(self.home)
        self.floorplan.setGeometry(QtCore.QRect(50, 30, 371, 171))
        self.floorplan.setStyleSheet("background:none;")
        self.floorplan.setText("")
        self.floorplan.setPixmap(QtGui.QPixmap(dir_path+"/static/floor.png"))
        self.floorplan.setObjectName("floorplan")
        self.livingroom_trigger = QtWidgets.QLabel(self.home)
        self.livingroom_trigger.setGeometry(QtCore.QRect(90, 128, 32, 33))
        self.livingroom_trigger.setStyleSheet("background:none;")
        self.livingroom_trigger.setText("")
        self.livingroom_trigger.setPixmap(QtGui.QPixmap(dir_path+"/static/touch.png"))
        self.livingroom_trigger.setAlignment(QtCore.Qt.AlignCenter)
        self.livingroom_trigger.setObjectName("livingroom_trigger")
        self.livingroom_trigger.mouseReleaseEvent = self.setRoomLivingRoom
        self.bedroom_trigger = QtWidgets.QLabel(self.home)
        self.bedroom_trigger.setGeometry(QtCore.QRect(164, 86, 32, 33))
        self.bedroom_trigger.setStyleSheet("background:none;")
        self.bedroom_trigger.setText("")
        self.bedroom_trigger.setPixmap(QtGui.QPixmap(dir_path+"/static/touch.png"))
        self.bedroom_trigger.setAlignment(QtCore.Qt.AlignCenter)
        self.bedroom_trigger.setObjectName("bedroom_trigger")
        self.bedroom_trigger.mouseReleaseEvent = self.setRoomBedroom
        self.office_trigger = QtWidgets.QLabel(self.home)
        self.office_trigger.setGeometry(QtCore.QRect(219, 44, 32, 33))
        self.office_trigger.setStyleSheet("background:none;")
        self.office_trigger.setText("")
        self.office_trigger.setPixmap(QtGui.QPixmap(dir_path+"/static/touch.png"))
        self.office_trigger.setAlignment(QtCore.Qt.AlignCenter)
        self.office_trigger.setObjectName("office_trigger")
        self.office_trigger.mouseReleaseEvent = self.setRoomOffice
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(dir_path+"/static/home-lock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(dir_path+"/static/home-lock-alt.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.tabs.addTab(self.home, icon, "")
        ## Scenes Tab
        self.scenes = QtWidgets.QWidget()
        self.scenes.setStyleSheet(
            "background:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(0, 113, 188, 255), stop:1 rgba(212, 20, 90, 255));")
        self.scenes.setObjectName("scenes")
        self.scene_selector = QtWidgets.QScrollArea(self.scenes)
        self.scene_selector.setGeometry(QtCore.QRect(220, 3, 220, 220))
        self.scene_selector.setStyleSheet("background:transparent;border:none")
        self.scene_selector.setWidgetResizable(True)
        self.scene_selector.setObjectName("scene_selector")
        self.scene_selector_widget = QtWidgets.QWidget()
        self.scene_selector_widget.setGeometry(QtCore.QRect(0, 0, 220, 220))
        self.scene_selector_widget.setObjectName("scene_selector_widget")

        self.scene1 = QtWidgets.QLabel(self.scene_selector_widget)
        self.scene1.setGeometry(QtCore.QRect(40, 20, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setWeight(10)
        font.setPointSize(20)
        self.scene1.setFont(font)
        self.scene1.setAlignment(QtCore.Qt.AlignCenter)
        self.scene1.setObjectName("scene1")
        self.scene1.mouseReleaseEvent = lambda event:self.setScene("1")

        self.spacer1 = QtWidgets.QLabel(self.scene_selector_widget)
        self.spacer1.setGeometry(QtCore.QRect(50, 50, 111, 2))
        self.spacer1.setStyleSheet("background:rgba(71, 71, 71, 211);")
        self.spacer1.setText("")
        self.spacer1.setObjectName("spacer1")

        self.scene2 = QtWidgets.QLabel(self.scene_selector_widget)
        self.scene2.setGeometry(QtCore.QRect(40, 60, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setWeight(10)
        font.setPointSize(20)
        self.scene2.setFont(font)
        self.scene2.setAlignment(QtCore.Qt.AlignCenter)
        self.scene2.setObjectName("scene2")
        self.scene2.mouseReleaseEvent = lambda event:self.setScene("2")

        self.spacer2 = QtWidgets.QLabel(self.scene_selector_widget)
        self.spacer2.setGeometry(QtCore.QRect(50, 90, 111, 2))
        self.spacer2.setStyleSheet("background:rgba(71, 71, 71, 211);")
        self.spacer2.setText("")
        self.spacer2.setObjectName("spacer2")

        self.scene3 = QtWidgets.QLabel(self.scene_selector_widget)
        self.scene3.setGeometry(QtCore.QRect(40, 100, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setWeight(10)
        font.setPointSize(20)
        self.scene3.setFont(font)
        self.scene3.setAlignment(QtCore.Qt.AlignCenter)
        self.scene3.setObjectName("scene3")
        self.scene3.mouseReleaseEvent = lambda event:self.setScene("3")

        self.spacer3 = QtWidgets.QLabel(self.scene_selector_widget)
        self.spacer3.setGeometry(QtCore.QRect(50, 130, 111, 2))
        self.spacer3.setStyleSheet("background:rgba(71, 71, 71, 211);")
        self.spacer3.setText("")
        self.spacer3.setObjectName("spacer3")

        self.scene4 = QtWidgets.QLabel(self.scene_selector_widget)
        self.scene4.setGeometry(QtCore.QRect(40, 140, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setWeight(10)
        font.setPointSize(20)
        self.scene4.setFont(font)
        self.scene4.setAlignment(QtCore.Qt.AlignCenter)
        self.scene4.setObjectName("scene4")
        self.scene4.mouseReleaseEvent = lambda event:self.setScene("4")

        self.spacer4 = QtWidgets.QLabel(self.scene_selector_widget)
        self.spacer4.setGeometry(QtCore.QRect(50, 170, 111, 2))
        self.spacer4.setStyleSheet("background:rgba(71, 71, 71, 211);")
        self.spacer4.setText("")
        self.spacer4.setObjectName("spacer4")

        self.scene5 = QtWidgets.QLabel(self.scene_selector_widget)
        self.scene5.setGeometry(QtCore.QRect(40, 180, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setWeight(10)
        font.setPointSize(20)
        self.scene5.setFont(font)
        self.scene5.setAlignment(QtCore.Qt.AlignCenter)
        self.scene5.setObjectName("scene5")
        self.scene5.mouseReleaseEvent = lambda event:self.setScene("5")

        self.scene6 = QtWidgets.QLabel(self.scene_selector_widget)
        self.scene6.setGeometry(QtCore.QRect(40, 220, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setWeight(10)
        font.setPointSize(20)
        self.scene6.setFont(font)
        self.scene6.setAlignment(QtCore.Qt.AlignCenter)
        self.scene6.setObjectName("scene6")
        self.scene6.mouseReleaseEvent = lambda event:self.setScene("6")

        self.scene_selector.setWidget(self.scene_selector_widget)
        self.inside_temp_scenes_label = QtWidgets.QLabel(self.scenes)
        self.inside_temp_scenes_label.setGeometry(QtCore.QRect(80, 80, 73, 21))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(18)
        font.setWeight(10)
        self.inside_temp_scenes_label.setFont(font)
        self.inside_temp_scenes_label.setStyleSheet("background:none;")
        self.inside_temp_scenes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.inside_temp_scenes_label.setObjectName("inside_temp_scenes_label")
        self.outside_temp_scenes = QtWidgets.QLabel(self.scenes)
        self.outside_temp_scenes.setGeometry(QtCore.QRect(60, 118, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(39)
        font.setWeight(10)
        self.outside_temp_scenes.setFont(font)
        self.outside_temp_scenes.setStyleSheet("background:none;")
        self.outside_temp_scenes.setAlignment(QtCore.Qt.AlignCenter)
        self.outside_temp_scenes.setObjectName("outside_temp_scenes")
        self.inside_temp_scenes = QtWidgets.QLabel(self.scenes)
        self.inside_temp_scenes.setGeometry(QtCore.QRect(60, 35, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(39)
        font.setWeight(10)
        self.inside_temp_scenes.setFont(font)
        self.inside_temp_scenes.setStyleSheet("background:none;")
        self.inside_temp_scenes.setTextFormat(QtCore.Qt.PlainText)
        self.inside_temp_scenes.setAlignment(QtCore.Qt.AlignCenter)
        self.inside_temp_scenes.setObjectName("inside_temp_scenes")
        self.outside_temp_scenes_label = QtWidgets.QLabel(self.scenes)
        self.outside_temp_scenes_label.setGeometry(QtCore.QRect(80, 160, 73, 21))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(18)
        font.setWeight(10)
        self.outside_temp_scenes_label.setFont(font)
        self.outside_temp_scenes_label.setStyleSheet("background:none;")
        self.outside_temp_scenes_label.setAlignment(QtCore.Qt.AlignCenter)
        self.outside_temp_scenes_label.setObjectName("outside_temp_scenes_label")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(dir_path+"/static/scenes.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(dir_path+"/static/scenes-alt.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.tabs.addTab(self.scenes, icon1, "")
        ## Temp Tab
        self.temp = QtWidgets.QWidget()
        self.temp.setStyleSheet(
            "background:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(0, 113, 188, 255), stop:1 rgba(212, 20, 90, 255));")
        self.temp.setObjectName("temp")
        self.outside_temp_temp = QtWidgets.QLabel(self.temp)
        self.outside_temp_temp.setGeometry(QtCore.QRect(60, 118, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(39)
        font.setWeight(10)
        self.outside_temp_temp.setFont(font)
        self.outside_temp_temp.setStyleSheet("background:none;")
        self.outside_temp_temp.setAlignment(QtCore.Qt.AlignCenter)
        self.outside_temp_temp.setObjectName("outside_temp_temp")
        self.inside_temp_temp_label = QtWidgets.QLabel(self.temp)
        self.inside_temp_temp_label.setGeometry(QtCore.QRect(80, 80, 73, 21))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(18)
        font.setWeight(10)
        self.inside_temp_temp_label.setFont(font)
        self.inside_temp_temp_label.setStyleSheet("background:none;")
        self.inside_temp_temp_label.setAlignment(QtCore.Qt.AlignCenter)
        self.inside_temp_temp_label.setObjectName("inside_temp_temp_label")
        self.inside_temp_temp = QtWidgets.QLabel(self.temp)
        self.inside_temp_temp.setGeometry(QtCore.QRect(60, 35, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(39)
        font.setWeight(10)
        self.inside_temp_temp.setFont(font)
        self.inside_temp_temp.setStyleSheet("background:none;")
        self.inside_temp_temp.setAlignment(QtCore.Qt.AlignCenter)
        self.inside_temp_temp.setObjectName("inside_temp_temp")
        self.outside_temp_temp_label = QtWidgets.QLabel(self.temp)
        self.outside_temp_temp_label.setGeometry(QtCore.QRect(80, 160, 73, 21))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(18)
        font.setWeight(10)
        self.outside_temp_temp_label.setFont(font)
        self.outside_temp_temp_label.setStyleSheet("background:none;")
        self.outside_temp_temp_label.setAlignment(QtCore.Qt.AlignCenter)
        self.outside_temp_temp_label.setObjectName("outside_temp_temp_label")
        self.set_temp = QtWidgets.QLabel(self.temp)
        self.set_temp.setGeometry(QtCore.QRect(280, 65, 100, 100))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(30)
        font.setWeight(60)
        self.set_temp.setFont(font)
        self.set_temp.setStyleSheet("background:none;\n"
                                    "border:4px solid #29abe2;")
        self.set_temp.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.set_temp.setLineWidth(4)
        self.set_temp.setAlignment(QtCore.Qt.AlignCenter)
        self.set_temp.setObjectName("set_temp")
        self.temp_mode = QtWidgets.QWidget(self.temp)
        self.temp_mode.setGeometry(QtCore.QRect(280, 170, 100, 10))
        self.temp_mode.setStyleSheet("background:#c1272d;")
        self.temp_mode.setObjectName("temp_mode")
        self.arrow_down = QtWidgets.QLabel(self.temp)
        self.arrow_down.setGeometry(QtCore.QRect(230, 95, 27, 36))
        self.arrow_down.setStyleSheet("background:none;")
        self.arrow_down.setText("")
        self.arrow_down.setPixmap(QtGui.QPixmap(dir_path+"/static/down_arrow.png"))
        self.arrow_down.setObjectName("arrow_down")
        self.arrow_up = QtWidgets.QLabel(self.temp)
        self.arrow_up.setGeometry(QtCore.QRect(400, 95, 27, 36))
        self.arrow_up.setStyleSheet("background:none;")
        self.arrow_up.setText("")
        self.arrow_up.setPixmap(QtGui.QPixmap(dir_path+"/static/up_arrow.png"))
        self.arrow_up.setObjectName("arrow_up")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(dir_path+"/static/temp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap(dir_path+"/static/temp-alt.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.tabs.addTab(self.temp, icon2, "")
        ## Security Tab
        self.sec = QtWidgets.QWidget()
        self.sec.setStyleSheet(
            "background:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(0, 113, 188, 255), stop:1 rgba(212, 20, 90, 255));")
        self.sec.setObjectName("sec")
        self.dev = QtWidgets.QLabel(self.sec)
        self.dev.setGeometry(QtCore.QRect(100, 170, 280, 20))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(12)
        font.setWeight(60)
        self.dev.setFont(font)
        self.dev.setStyleSheet("background:none;\n"
                               "color:#FFF;\n"
                               "")
        self.dev.setAlignment(QtCore.Qt.AlignCenter)
        self.dev.setObjectName("dev")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(dir_path+"/static/cam.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(dir_path+"/static/cam-alt.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.tabs.addTab(self.sec, icon3, "")
        ## Network Tab
        self.network = QtWidgets.QWidget()
        self.network.setStyleSheet(
            "background:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(0, 113, 188, 255), stop:1 rgba(212, 20, 90, 255));")
        self.network.setObjectName("network")
        self.devices_label = QtWidgets.QLabel(self.network)
        self.devices_label.setGeometry(QtCore.QRect(30, 15, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(18)
        font.setWeight(60)
        self.devices_label.setFont(font)
        self.devices_label.setStyleSheet("background:none;\n"
                                         "color:#FFF;")
        self.devices_label.setObjectName("devices_label")
        self.devices = QtWidgets.QLabel(self.network)
        self.devices.setGeometry(QtCore.QRect(30, 45, 221, 180))
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue LT Com,HelveticaNeueLT Com 45 Lt")
        font.setPointSize(9)
        font.setWeight(60)
        self.devices.setFont(font)
        self.devices.setStyleSheet("background:none;\n"
                                   "color:#FFF;")
        self.devices.setObjectName("devices")
        self.hannahstatus = QtWidgets.QLabel(self.network)
        self.hannahstatus.setGeometry(QtCore.QRect(310, 80, 141, 51))
        self.hannahstatus.setStyleSheet("background:none;\n"
                                        "")
        self.hannahstatus.setText("")
        self.hannahstatus.setPixmap(QtGui.QPixmap(dir_path + "/static/hannah-away.png"))
        self.hannahstatus.setObjectName("hannahstatus")
        self.angelicastatus = QtWidgets.QLabel(self.network)
        self.angelicastatus.setGeometry(QtCore.QRect(310, 140, 141, 51))
        self.angelicastatus.setStyleSheet("background:none;\n"
                                          "")
        self.angelicastatus.setText("")
        self.angelicastatus.setPixmap(QtGui.QPixmap(dir_path+"/static/angelica-away.png"))
        self.angelicastatus.setObjectName("angelicastatus")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(dir_path+"/static/network.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(dir_path+"/static/network-alt.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.tabs.addTab(self.network, icon4, "")
        ## Final Generations
        self.background = QtWidgets.QWidget(self.master_window)
        self.background.setGeometry(QtCore.QRect(0, 0, 480, 320))
        self.background.setStyleSheet("background:#000;")
        self.background.setObjectName("background")
        self.background.raise_()
        self.topbar.raise_()
        self.tabs.raise_()
        MainWindow.setCentralWidget(self.master_window)
        ## Adds initial values to the UI
        self.retranslateUi(MainWindow)
        ## Starts the date and time timer
        self.setDateTime(MainWindow)
        ## Starts the date and time timer
        self.listenToServer(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ScARA Panel"))
        self.time.setText(_translate("MainWindow", "Hello!"))
        self.date.setText(_translate("MainWindow", "Getting updates now..."))
        ## Scene Tab
        self.scene1.setText(_translate("MainWindow", "--"))
        self.scene2.setText(_translate("MainWindow", "--"))
        self.scene3.setText(_translate("MainWindow", "--"))
        self.scene4.setText(_translate("MainWindow", "--"))
        self.scene5.setText(_translate("MainWindow", "--"))
        self.scene6.setText(_translate("MainWindow", "--"))
        self.inside_temp_scenes_label.setText(_translate("MainWindow", "inside"))
        self.outside_temp_scenes.setText(_translate("MainWindow", "--°F"))
        self.inside_temp_scenes.setText(_translate("MainWindow", "--°F"))
        self.outside_temp_scenes_label.setText(_translate("MainWindow", "outside"))
        ## Temp Tab
        self.outside_temp_temp.setText(_translate("MainWindow", "--°F"))
        self.inside_temp_temp_label.setText(_translate("MainWindow", "inside"))
        self.inside_temp_temp.setText(_translate("MainWindow", "--°F"))
        self.outside_temp_temp_label.setText(_translate("MainWindow", "outside"))
        self.set_temp.setText(_translate("MainWindow", "--°F"))
        ## Security Tab
        self.dev.setText(_translate("MainWindow", "This section is still being developed"))
        ## Network Tab
        self.devices.setText(_translate("MainWindow", "Getting devices"))
        self.devices_label.setText(_translate("MainWindow", "Connected devices"))

    def micClick(self, MainWindow):
        self.t.cancel()
        self.ws.kill()
        sys.exit(0)

    ## Set the room, retranslate the scene list, go to scenes
    def setRoomOffice(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.resetSceneList(MainWindow)
        global currentRoom
        currentRoom = "Office"
        currentRecord = 0
        for x in scenes:
            if x['name'].find(currentRoom) == 0:
                currentRecord += 1
                if currentRecord == 1:
                    self.scene1.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[1] = x['id']
                elif currentRecord == 2:
                    self.scene2.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[2] = x['id']
                elif currentRecord == 3:
                    self.scene3.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[3] = x['id']
                elif currentRecord == 4:
                    self.scene4.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[4] = x['id']
                elif currentRecord == 5:
                    self.scene5.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[5] = x['id']
                elif currentRecord == 6:
                    self.scene6.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[6] = x['id']
        self.tabs.setCurrentIndex(0)

    def setRoomLivingRoom(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.resetSceneList(MainWindow)
        global currentRoom
        currentRoom = "Living Room"
        currentRecord = 0
        for x in scenes:
            if x['name'].find(currentRoom) == 0:
                currentRecord += 1
                if currentRecord == 1:
                    self.scene1.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[1] = x['id']
                elif currentRecord == 2:
                    self.scene2.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[2] = x['id']
                elif currentRecord == 3:
                    self.scene3.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[3] = x['id']
                elif currentRecord == 4:
                    self.scene4.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[4] = x['id']
                elif currentRecord == 5:
                    self.scene5.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[5] = x['id']
                elif currentRecord == 6:
                    self.scene6.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[6] = x['id']
        self.tabs.setCurrentIndex(0)

    def setRoomBedroom(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.resetSceneList(MainWindow)
        global currentRoom
        currentRoom = "Bedroom"
        currentRecord = 0
        for x in scenes:
            if x['name'].find(currentRoom) == 0:
                currentRecord += 1
                if currentRecord == 1:
                    self.scene1.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[1] = x['id']
                elif currentRecord == 2:
                    self.scene2.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[2] = x['id']
                elif currentRecord == 3:
                    self.scene3.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[3] = x['id']
                elif currentRecord == 4:
                    self.scene4.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[4] = x['id']
                elif currentRecord == 5:
                    self.scene5.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[5] = x['id']
                elif currentRecord == 6:
                    self.scene6.setText(_translate("MainWindow", x['name'][len(currentRoom) + 1:]))
                    currentSceneList[6] = x['id']
        self.tabs.setCurrentIndex(0)

    def resetSceneList(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.scene1.setText(_translate("MainWindow", ""))
        self.scene2.setText(_translate("MainWindow", ""))
        self.scene3.setText(_translate("MainWindow", ""))
        self.scene4.setText(_translate("MainWindow", ""))
        self.scene5.setText(_translate("MainWindow", ""))
        self.scene6.setText(_translate("MainWindow", ""))
        currentSceneList[1] = 0
        currentSceneList[2] = 0
        currentSceneList[3] = 0
        currentSceneList[4] = 0
        currentSceneList[5] = 0
        currentSceneList[6] = 0

    def setScene(self, scene):
        sceneID = currentSceneList[int(scene)]
        from websocket import create_connection
        ws = create_connection("ws://YOURALMONDROUTER:7681/root/YOURALMONDPASSWORD")
        ws.send('{"CommandType":"ActivateScene","MobileInternalIndex":"setScene'+sceneID+'","Scenes":{"ID":"'+sceneID+'"}}')
        result = ws.recv()
        ws.close()

    ## Sets the date and time ever 60 seconds
    def setDateTime(self, MainWindow):
        currentTime = time.strftime("%I:%M%p")
        currentDate = time.strftime("%A, %d %B %Y")
        _translate = QtCore.QCoreApplication.translate
        self.time.setText(_translate("MainWindow", "Hello! It is " + currentTime))
        self.date.setText(_translate("MainWindow", "" + currentDate))
        self.t = Timer(60, self.setDateTime, args=[MainWindow])
        self.t.start()

    ## Establishes a QProcess to listen to the server
    def listenToServer(self, MainWindow):
        self.ws = QtCore.QProcess(self)
        self.ws.start("python3 -u /home/pi/scara_panel/ws.py")
        self.ws.readyReadStandardOutput.connect(self.processServer)

    ## Processes messages from the server and translates accordingly
    def processServer(self):
        income = str(self.ws.readAllStandardOutput())
        _translate = QtCore.QCoreApplication.translate
        if income.find("almondSceneList") == 2:
            data = income[17:]
            data = data[:len(data)-3]
            data = data.replace("\\", "")
            global scenes
            scenes = json.loads(data)
        elif income.find("almondClientList") == 2:
            data = income[18:]
            data = data[:len(data) - 3]
            data = data.replace("\\", "")
            global clients
            clients = json.loads(data)
            clientsStr = ""
            for x in clients:
                clientsStr += x['name']+" ("+x['ip']+")\n"
            self.devices.setText(_translate("MainWindow", clientsStr))
            self.angelicastatus.setPixmap(QtGui.QPixmap(dir_path + "/static/angelica-away.png"))
            self.hannahstatus.setPixmap(QtGui.QPixmap(dir_path + "/static/hannah-away.png"))
            for x in clients:
                if x['ip'] == "10.10.10.15":
                    self.angelicastatus.setPixmap(QtGui.QPixmap(dir_path + "/static/angelica-home.png"))
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(dir_path + "/static/home-love.png"), QtGui.QIcon.Normal,
                                   QtGui.QIcon.Off)
                    icon.addPixmap(QtGui.QPixmap(dir_path + "/static/home-love-alt.png"), QtGui.QIcon.Normal,
                                   QtGui.QIcon.On)
                    self.tabs.addTab(self.home, icon, "")
                if x['ip'] == "10.10.10.14":
                    self.hannahstatus.setPixmap(QtGui.QPixmap(dir_path + "/static/hannah-home.png"))
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(dir_path + "/static/home-love.png"), QtGui.QIcon.Normal,
                                   QtGui.QIcon.Off)
                    icon.addPixmap(QtGui.QPixmap(dir_path + "/static/home-love-alt.png"), QtGui.QIcon.Normal,
                                   QtGui.QIcon.On)
                    self.tabs.addTab(self.home, icon, "")

        elif income.find("weather") == 2:
            data = income[9:]
            data = data[:2]
            self.outside_temp_temp.setText(_translate("MainWindow", data+"°F"))
            self.outside_temp_scenes.setText(_translate("MainWindow", data+"°F"))

def main():
    app = QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(app.exec_())

## Execute
if __name__ == '__main__':
    main()