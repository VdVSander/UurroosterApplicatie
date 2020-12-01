import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, Qt
from uurroosterLib import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(751, 353)
        font = QtGui.QFont()
        font.setPointSize(18)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget.setObjectName("centralwidget")
        self.btnAlarm = QtWidgets.QPushButton(self.centralwidget)
        self.btnAlarm.setGeometry(QtCore.QRect(480, 260, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.btnAlarm.setFont(font)
        self.btnAlarm.setObjectName("btnAlarm")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 20, 726, 222))
        self.widget.setObjectName("widget")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblDatum = QtWidgets.QLabel(self.widget)
        self.lblDatum.setObjectName("lblDatum")
        self.horizontalLayout.addWidget(self.lblDatum)
        self.lblDatumVal = QtWidgets.QLabel(self.widget)
        self.lblDatumVal.setObjectName("lblDatumVal")
        self.horizontalLayout.addWidget(self.lblDatumVal)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblCourse = QtWidgets.QLabel(self.widget)
        self.lblCourse.setObjectName("lblCourse")
        self.horizontalLayout_2.addWidget(self.lblCourse)
        self.lblCourseVal = QtWidgets.QLabel(self.widget)
        self.lblCourseVal.setObjectName("lblCourseVal")
        self.horizontalLayout_2.addWidget(self.lblCourseVal)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lblLocation = QtWidgets.QLabel(self.widget)
        self.lblLocation.setObjectName("lblLocation")
        self.horizontalLayout_3.addWidget(self.lblLocation)
        self.lblLocationVal = QtWidgets.QLabel(self.widget)
        self.lblLocationVal.setObjectName("lblLocationVal")
        self.horizontalLayout_3.addWidget(self.lblLocationVal)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lblNextCourseVal = QtWidgets.QLabel(self.widget)
        self.lblNextCourseVal.setObjectName("lblNextCourseVal")
        self.horizontalLayout_4.addWidget(self.lblNextCourseVal)
        self.lblNextCourse = QtWidgets.QLabel(self.widget)
        self.lblNextCourse.setObjectName("lblNextCourse")
        self.horizontalLayout_4.addWidget(self.lblNextCourse)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lblTimeTil = QtWidgets.QLabel(self.widget)
        self.lblTimeTil.setObjectName("lblTimeTil")
        self.horizontalLayout_5.addWidget(self.lblTimeTil)
        self.lblTimeTilVal = QtWidgets.QLabel(self.widget)
        self.lblTimeTilVal.setObjectName("lblTimeTilVal")
        self.horizontalLayout_5.addWidget(self.lblTimeTilVal)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lblTime = QtWidgets.QLabel(self.widget)
        self.lblTime.setObjectName("lblTime")
        self.horizontalLayout_6.addWidget(self.lblTime, 0, QtCore.Qt.AlignTop)
        self.lblTimeVal = QtWidgets.QLabel(self.widget)
        self.lblTimeVal.setObjectName("lblTimeVal")
        self.horizontalLayout_6.addWidget(self.lblTimeVal, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.courses = self.update_courses()
        self.update_time(self.courses)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def update_courses(self):
        number_of_events = 2
        events = load_events(number_of_events)
        courses = get_courses(events)
        curr_time = datetime.datetime.now()

        if (curr_time > courses[0].start_time) and (curr_time < courses[0].end_time):
            self.lblCourseVal.setText(courses[0].name)
            self.lblCourseVal.adjustSize()
            self.lblNextCourse.setText(courses[1].name)
            self.lblNextCourse.adjustSize()
        else:
            self.lblCourseVal.setText("No active course")
            self.lblCourseVal.adjustSize()
            self.lblNextCourse.setText(courses[0].name)
            self.lblNextCourse.adjustSize()
        if (courses[1].location == ""):
            self.lblLocationVal.setText("No location")
            self.lblLocationVal.adjustSize()
        else:
            self.lblLocationVal.setText(courses[1].location)
            self.lblLocationVal.adjustSize()
        return courses

    def update_time(self, courses):
        curr_time = datetime.datetime.now()
        if (curr_time > courses[0].start_time) and (curr_time < courses[0].end_time):
            tdelta = calculate_time_delta(courses[1].start_time)
        else:
            tdelta = calculate_time_delta(courses[0].start_time)

        if tdelta.days == 0:
            if tdelta.hours == 0:
                if tdelta.minutes == 0:
                    display = str(tdelta.seconds) + " seconds"
                else:
                    display = str(tdelta.minutes) + ":" + str(tdelta.seconds)
            else:
                display = str(tdelta.hours) + ":" + str(tdelta.minutes) + ":" + str(tdelta.seconds)
        else:
            display = str(tdelta.days) + " d " + str(tdelta.hours) + " h " + str(tdelta.minutes) + " m " + str(
                tdelta.seconds) + " s"
        curr_date = datetime.datetime.strftime(curr_time, "%d/%m/%Y")
        self.lblDatumVal.setText(curr_date)
        self.lblDatumVal.adjustSize()
        self.lblTimeTilVal.setText(display)
        self.lblTimeTilVal.adjustSize()

    def update(self):
        curr_time = datetime.datetime.now()
        #If the previous course has ended or first new active course has started
        if (curr_time >= self.courses[0].end_time) or (curr_time >= self.courses[0].start_time):
            self.courses = self.update_courses()
        self.update_time(self.courses)
        curr_time = QTime.currentTime()
        self.lblTimeVal.setText(curr_time.toString('hh:mm:ss'))
        self.lblTimeVal.adjustSize()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Uurrooster Tool"))
        self.btnAlarm.setText(_translate("MainWindow", "Zet mijn wekker"))
        self.lblDatum.setText(_translate("MainWindow", "Datum:"))
        self.lblDatumVal.setText(_translate("MainWindow", "xx/xx/xxxx"))
        self.lblCourse.setText(_translate("MainWindow", "Actieve les:"))
        self.lblCourseVal.setText(_translate("MainWindow", "Test Lab"))
        self.lblLocation.setText(_translate("MainWindow", "Locatie:"))
        self.lblLocationVal.setText(_translate("MainWindow", "Test lokaal"))
        self.lblNextCourseVal.setText(_translate("MainWindow", "Volgende les:"))
        self.lblNextCourse.setText(_translate("MainWindow", "Test Lab session 2"))
        self.lblTimeTil.setText(_translate("MainWindow", "Tijd tot volgende les:"))
        self.lblTimeTilVal.setText(_translate("MainWindow", "xx dagen xx:xx:xx"))
        self.lblTime.setText(_translate("MainWindow", "Tijd:"))
        self.lblTimeVal.setText(_translate("MainWindow", "xx:xx:xx"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
