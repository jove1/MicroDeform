# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QActionGroup, QBrush, QColor,
    QConicalGradient, QCursor, QFont, QFontDatabase,
    QGradient, QIcon, QImage, QKeySequence,
    QLinearGradient, QPainter, QPalette, QPixmap,
    QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDoubleSpinBox, QGridLayout,
    QGroupBox, QLabel, QLayout, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QRadioButton, QSizePolicy, QStackedWidget,
    QStatusBar, QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setFocusPolicy(Qt.StrongFocus)
        self.LogXY = QAction(MainWindow)
        self.LogXY.setObjectName(u"LogXY")
        self.LogXY.setCheckable(True)
        self.LogZ = QAction(MainWindow)
        self.LogZ.setObjectName(u"LogZ")
        self.LogZ.setCheckable(True)
        self.LogFineZ = QAction(MainWindow)
        self.LogFineZ.setObjectName(u"LogFineZ")
        self.LogFineZ.setCheckable(True)
        self.LogADC = QAction(MainWindow)
        self.LogADC.setObjectName(u"LogADC")
        self.LogADC.setCheckable(True)
        self.LogNone = QAction(MainWindow)
        self.LogNone.setObjectName(u"LogNone")
        self.LogAll = QAction(MainWindow)
        self.LogAll.setObjectName(u"LogAll")
        self.QueryXYposition = QAction(MainWindow)
        self.QueryXYposition.setObjectName(u"QueryXYposition")
        self.QueryXYposition.setCheckable(True)
        self.QueryXYposition.setChecked(True)
        self.QueryXYerror = QAction(MainWindow)
        self.QueryXYerror.setObjectName(u"QueryXYerror")
        self.QueryXYerror.setCheckable(True)
        self.QueryXYerror.setChecked(True)
        self.QueryZposition = QAction(MainWindow)
        self.QueryZposition.setObjectName(u"QueryZposition")
        self.QueryZposition.setCheckable(True)
        self.QueryZposition.setChecked(True)
        self.QueryFineZposition = QAction(MainWindow)
        self.QueryFineZposition.setObjectName(u"QueryFineZposition")
        self.QueryFineZposition.setCheckable(True)
        self.QueryFineZposition.setChecked(True)
        self.QueryFineZvoltage = QAction(MainWindow)
        self.QueryFineZvoltage.setObjectName(u"QueryFineZvoltage")
        self.QueryFineZvoltage.setCheckable(True)
        self.QueryFineZvoltage.setChecked(True)
        self.QueryFineZerror = QAction(MainWindow)
        self.QueryFineZerror.setObjectName(u"QueryFineZerror")
        self.QueryFineZerror.setCheckable(True)
        self.QueryFineZerror.setChecked(True)
        self.QueryAll = QAction(MainWindow)
        self.QueryAll.setObjectName(u"QueryAll")
        self.QueryNone = QAction(MainWindow)
        self.QueryNone.setObjectName(u"QueryNone")
        self.groupTest = QActionGroup(MainWindow)
        self.groupTest.setObjectName(u"groupTest")
        self.actionCompression = QAction(self.groupTest)
        self.actionCompression.setObjectName(u"actionCompression")
        self.actionCompression.setCheckable(True)
        self.actionCompression.setChecked(True)
        self.actionTension = QAction(self.groupTest)
        self.actionTension.setObjectName(u"actionTension")
        self.actionTension.setCheckable(True)
        self.groupPlot = QActionGroup(MainWindow)
        self.groupPlot.setObjectName(u"groupPlot")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_6 = QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gTest = QGroupBox(self.centralwidget)
        self.gTest.setObjectName(u"gTest")
        self.gridLayout_10 = QGridLayout(self.gTest)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.FileName = QLineEdit(self.gTest)
        self.FileName.setObjectName(u"FileName")
        self.FileName.setEnabled(False)

        self.gridLayout_10.addWidget(self.FileName, 0, 1, 1, 1)

        self.label_16 = QLabel(self.gTest)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_16, 0, 0, 1, 1)

        self.Record = QPushButton(self.gTest)
        self.Record.setObjectName(u"Record")

        self.gridLayout_10.addWidget(self.Record, 0, 2, 1, 1)

        self.Compression = QRadioButton(self.gTest)
        self.Compression.setObjectName(u"Compression")
        self.Compression.setChecked(True)

        self.gridLayout_10.addWidget(self.Compression, 1, 0, 1, 3)

        self.Tension = QRadioButton(self.gTest)
        self.Tension.setObjectName(u"Tension")

        self.gridLayout_10.addWidget(self.Tension, 2, 0, 1, 3)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetMinimumSize)
        self.LoadWaitUnload = QPushButton(self.gTest)
        self.LoadWaitUnload.setObjectName(u"LoadWaitUnload")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LoadWaitUnload.sizePolicy().hasHeightForWidth())
        self.LoadWaitUnload.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.LoadWaitUnload, 3, 5, 5, 1)

        self.UnloadSpeed = QDoubleSpinBox(self.gTest)
        self.UnloadSpeed.setObjectName(u"UnloadSpeed")
        self.UnloadSpeed.setDecimals(3)
        self.UnloadSpeed.setMaximum(5.000000000000000)
        self.UnloadSpeed.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.UnloadSpeed.setValue(1.000000000000000)

        self.gridLayout_3.addWidget(self.UnloadSpeed, 7, 2, 1, 1)

        self.label_11 = QLabel(self.gTest)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_11, 3, 1, 1, 1)

        self.label_30 = QLabel(self.gTest)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_30, 6, 1, 1, 1)

        self.label_25 = QLabel(self.gTest)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_25, 4, 1, 1, 1)

        self.LoadStep = QDoubleSpinBox(self.gTest)
        self.LoadStep.setObjectName(u"LoadStep")
        self.LoadStep.setDecimals(3)
        self.LoadStep.setMaximum(30.000000000000000)
        self.LoadStep.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.LoadStep.setValue(10.000000000000000)

        self.gridLayout_3.addWidget(self.LoadStep, 3, 2, 1, 1)

        self.label_9 = QLabel(self.gTest)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_9, 5, 1, 1, 1)

        self.Unload = QPushButton(self.gTest)
        self.Unload.setObjectName(u"Unload")
        sizePolicy.setHeightForWidth(self.Unload.sizePolicy().hasHeightForWidth())
        self.Unload.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.Unload, 6, 4, 2, 1)

        self.Wait = QDoubleSpinBox(self.gTest)
        self.Wait.setObjectName(u"Wait")
        self.Wait.setDecimals(1)
        self.Wait.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.Wait.setValue(5.000000000000000)

        self.gridLayout_3.addWidget(self.Wait, 5, 2, 1, 1)

        self.UnloadStep = QDoubleSpinBox(self.gTest)
        self.UnloadStep.setObjectName(u"UnloadStep")
        self.UnloadStep.setDecimals(3)
        self.UnloadStep.setMaximum(30.000000000000000)
        self.UnloadStep.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.UnloadStep.setValue(10.000000000000000)

        self.gridLayout_3.addWidget(self.UnloadStep, 6, 2, 1, 1)

        self.UnloadStepNorm = QDoubleSpinBox(self.gTest)
        self.UnloadStepNorm.setObjectName(u"UnloadStepNorm")
        self.UnloadStepNorm.setDecimals(3)
        self.UnloadStepNorm.setMaximum(100.000000000000000)
        self.UnloadStepNorm.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.UnloadStepNorm.setValue(1.000000000000000)

        self.gridLayout_3.addWidget(self.UnloadStepNorm, 6, 3, 1, 1)

        self.label_27 = QLabel(self.gTest)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_27, 2, 3, 1, 1)

        self.Load = QPushButton(self.gTest)
        self.Load.setObjectName(u"Load")
        sizePolicy.setHeightForWidth(self.Load.sizePolicy().hasHeightForWidth())
        self.Load.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.Load, 3, 4, 2, 1)

        self.label_28 = QLabel(self.gTest)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_28, 7, 1, 1, 1)

        self.UnloadSpeedNorm = QDoubleSpinBox(self.gTest)
        self.UnloadSpeedNorm.setObjectName(u"UnloadSpeedNorm")
        self.UnloadSpeedNorm.setDecimals(4)
        self.UnloadSpeedNorm.setMaximum(1000.000000000000000)
        self.UnloadSpeedNorm.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.UnloadSpeedNorm.setValue(0.100000000000000)

        self.gridLayout_3.addWidget(self.UnloadSpeedNorm, 7, 3, 1, 1)

        self.LoadStepNorm = QDoubleSpinBox(self.gTest)
        self.LoadStepNorm.setObjectName(u"LoadStepNorm")
        self.LoadStepNorm.setDecimals(3)
        self.LoadStepNorm.setMaximum(100.000000000000000)
        self.LoadStepNorm.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.LoadStepNorm.setValue(1.000000000000000)

        self.gridLayout_3.addWidget(self.LoadStepNorm, 3, 3, 1, 1)

        self.LoadSpeed = QDoubleSpinBox(self.gTest)
        self.LoadSpeed.setObjectName(u"LoadSpeed")
        self.LoadSpeed.setDecimals(3)
        self.LoadSpeed.setMaximum(5.000000000000000)
        self.LoadSpeed.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.LoadSpeed.setValue(0.250000000000000)

        self.gridLayout_3.addWidget(self.LoadSpeed, 4, 2, 1, 1)

        self.LoadSpeedNorm = QDoubleSpinBox(self.gTest)
        self.LoadSpeedNorm.setObjectName(u"LoadSpeedNorm")
        self.LoadSpeedNorm.setDecimals(4)
        self.LoadSpeedNorm.setMaximum(1000.000000000000000)
        self.LoadSpeedNorm.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.LoadSpeedNorm.setValue(0.025000000000000)

        self.gridLayout_3.addWidget(self.LoadSpeedNorm, 4, 3, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_3, 3, 0, 1, 3)


        self.gridLayout.addWidget(self.gTest, 0, 0, 1, 1)

        self.gPlot = QGroupBox(self.centralwidget)
        self.gPlot.setObjectName(u"gPlot")
        self.gridLayout_5 = QGridLayout(self.gPlot)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.PlotTime = QRadioButton(self.gPlot)
        self.PlotTime.setObjectName(u"PlotTime")
        self.PlotTime.setChecked(True)

        self.gridLayout_5.addWidget(self.PlotTime, 0, 0, 1, 1)

        self.PlotXY = QRadioButton(self.gPlot)
        self.PlotXY.setObjectName(u"PlotXY")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.PlotXY.sizePolicy().hasHeightForWidth())
        self.PlotXY.setSizePolicy(sizePolicy1)

        self.gridLayout_5.addWidget(self.PlotXY, 1, 0, 1, 1)

        self.PlotClear = QPushButton(self.gPlot)
        self.PlotClear.setObjectName(u"PlotClear")

        self.gridLayout_5.addWidget(self.PlotClear, 1, 1, 1, 1)

        self.stackedWidget = QStackedWidget(self.gPlot)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.plotHistory = PlotWidget()
        self.plotHistory.setObjectName(u"plotHistory")
        self.stackedWidget.addWidget(self.plotHistory)
        self.plotXY = PlotWidget()
        self.plotXY.setObjectName(u"plotXY")
        self.stackedWidget.addWidget(self.plotXY)

        self.gridLayout_5.addWidget(self.stackedWidget, 3, 0, 1, 2)


        self.gridLayout.addWidget(self.gPlot, 2, 0, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout, 0, 1, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gFine = QGroupBox(self.centralwidget)
        self.gFine.setObjectName(u"gFine")
        self.gridLayout_8 = QGridLayout(self.gFine)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.FZSpeed = QDoubleSpinBox(self.gFine)
        self.FZSpeed.setObjectName(u"FZSpeed")
        self.FZSpeed.setDecimals(2)
        self.FZSpeed.setMaximum(5.000000000000000)
        self.FZSpeed.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.FZSpeed.setValue(1.500000000000000)

        self.gridLayout_8.addWidget(self.FZSpeed, 1, 0, 1, 1)

        self.label_26 = QLabel(self.gFine)
        self.label_26.setObjectName(u"label_26")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy2)

        self.gridLayout_8.addWidget(self.label_26, 0, 0, 1, 1)

        self.FZPos = QLabel(self.gFine)
        self.FZPos.setObjectName(u"FZPos")

        self.gridLayout_8.addWidget(self.FZPos, 1, 3, 1, 1)

        self.FZMinus = QPushButton(self.gFine)
        self.FZMinus.setObjectName(u"FZMinus")

        self.gridLayout_8.addWidget(self.FZMinus, 1, 2, 1, 1)

        self.FZPlus = QPushButton(self.gFine)
        self.FZPlus.setObjectName(u"FZPlus")

        self.gridLayout_8.addWidget(self.FZPlus, 1, 1, 1, 1)


        self.gridLayout_2.addWidget(self.gFine, 1, 0, 1, 1)

        self.Stop = QPushButton(self.centralwidget)
        self.Stop.setObjectName(u"Stop")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.Stop.sizePolicy().hasHeightForWidth())
        self.Stop.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.Stop, 0, 1, 2, 1)

        self.gCoarse = QGroupBox(self.centralwidget)
        self.gCoarse.setObjectName(u"gCoarse")
        self.gridLayout_7 = QGridLayout(self.gCoarse)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.XMinus = QPushButton(self.gCoarse)
        self.XMinus.setObjectName(u"XMinus")

        self.gridLayout_7.addWidget(self.XMinus, 3, 2, 1, 1)

        self.label_4 = QLabel(self.gCoarse)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_7.addWidget(self.label_4, 1, 0, 1, 1)

        self.XPlus = QPushButton(self.gCoarse)
        self.XPlus.setObjectName(u"XPlus")

        self.gridLayout_7.addWidget(self.XPlus, 3, 1, 1, 1)

        self.XSpeed = QDoubleSpinBox(self.gCoarse)
        self.XSpeed.setObjectName(u"XSpeed")
        self.XSpeed.setDecimals(1)
        self.XSpeed.setMaximum(2000.000000000000000)
        self.XSpeed.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.XSpeed.setValue(500.000000000000000)

        self.gridLayout_7.addWidget(self.XSpeed, 3, 0, 1, 1)

        self.ZPlus = QPushButton(self.gCoarse)
        self.ZPlus.setObjectName(u"ZPlus")

        self.gridLayout_7.addWidget(self.ZPlus, 5, 1, 1, 1)

        self.ZSpeed = QDoubleSpinBox(self.gCoarse)
        self.ZSpeed.setObjectName(u"ZSpeed")
        self.ZSpeed.setDecimals(1)
        self.ZSpeed.setMinimum(2.500000000000000)
        self.ZSpeed.setMaximum(2000.000000000000000)
        self.ZSpeed.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.ZSpeed.setValue(500.000000000000000)

        self.gridLayout_7.addWidget(self.ZSpeed, 5, 0, 1, 1)

        self.ZMinus = QPushButton(self.gCoarse)
        self.ZMinus.setObjectName(u"ZMinus")

        self.gridLayout_7.addWidget(self.ZMinus, 5, 2, 1, 1)

        self.ZPos = QLabel(self.gCoarse)
        self.ZPos.setObjectName(u"ZPos")

        self.gridLayout_7.addWidget(self.ZPos, 5, 3, 1, 1)

        self.YPlus = QPushButton(self.gCoarse)
        self.YPlus.setObjectName(u"YPlus")

        self.gridLayout_7.addWidget(self.YPlus, 4, 1, 1, 1)

        self.XPos = QLabel(self.gCoarse)
        self.XPos.setObjectName(u"XPos")

        self.gridLayout_7.addWidget(self.XPos, 3, 3, 1, 1)

        self.YPos = QLabel(self.gCoarse)
        self.YPos.setObjectName(u"YPos")

        self.gridLayout_7.addWidget(self.YPos, 4, 3, 1, 1)

        self.YMinus = QPushButton(self.gCoarse)
        self.YMinus.setObjectName(u"YMinus")

        self.gridLayout_7.addWidget(self.YMinus, 4, 2, 1, 1)

        self.YSpeed = QDoubleSpinBox(self.gCoarse)
        self.YSpeed.setObjectName(u"YSpeed")
        self.YSpeed.setDecimals(1)
        self.YSpeed.setMaximum(2000.000000000000000)
        self.YSpeed.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.YSpeed.setValue(500.000000000000000)

        self.gridLayout_7.addWidget(self.YSpeed, 4, 0, 1, 1)


        self.gridLayout_2.addWidget(self.gCoarse, 0, 0, 1, 1)

        self.gADCMonitor = QGroupBox(self.centralwidget)
        self.gADCMonitor.setObjectName(u"gADCMonitor")
        self.gridLayout_4 = QGridLayout(self.gADCMonitor)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.plotMonitor = PlotWidget(self.gADCMonitor)
        self.plotMonitor.setObjectName(u"plotMonitor")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.plotMonitor.sizePolicy().hasHeightForWidth())
        self.plotMonitor.setSizePolicy(sizePolicy4)

        self.gridLayout_4.addWidget(self.plotMonitor, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.gADCMonitor, 4, 0, 1, 2)

        self.gMeasurement = QGroupBox(self.centralwidget)
        self.gMeasurement.setObjectName(u"gMeasurement")
        self.gridLayout_9 = QGridLayout(self.gMeasurement)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.LoadNorm = QLabel(self.gMeasurement)
        self.LoadNorm.setObjectName(u"LoadNorm")
        self.LoadNorm.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.LoadNorm, 1, 4, 1, 2)

        self.LoadZero = QPushButton(self.gMeasurement)
        self.LoadZero.setObjectName(u"LoadZero")

        self.gridLayout_9.addWidget(self.LoadZero, 2, 3, 1, 1)

        self.LoadAbs = QLabel(self.gMeasurement)
        self.LoadAbs.setObjectName(u"LoadAbs")
        self.LoadAbs.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.LoadAbs, 1, 2, 1, 1)

        self.Area = QDoubleSpinBox(self.gMeasurement)
        self.Area.setObjectName(u"Area")
        self.Area.setDecimals(3)
        self.Area.setMaximum(9999.998999999999796)
        self.Area.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.Area.setValue(100.000000000000000)

        self.gridLayout_9.addWidget(self.Area, 2, 5, 1, 1)

        self.label_17 = QLabel(self.gMeasurement)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.label_17, 0, 2, 1, 1)

        self.label_18 = QLabel(self.gMeasurement)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.label_18, 0, 3, 1, 1)

        self.LoadRaw = QLabel(self.gMeasurement)
        self.LoadRaw.setObjectName(u"LoadRaw")
        self.LoadRaw.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.LoadRaw, 1, 1, 1, 1)

        self.LoadRel = QLabel(self.gMeasurement)
        self.LoadRel.setObjectName(u"LoadRel")
        self.LoadRel.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.LoadRel, 1, 3, 1, 1)

        self.LoadBar = QProgressBar(self.gMeasurement)
        self.LoadBar.setObjectName(u"LoadBar")
        self.LoadBar.setMaximum(1000)

        self.gridLayout_9.addWidget(self.LoadBar, 3, 1, 1, 5)

        self.label_6 = QLabel(self.gMeasurement)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.label_6, 0, 4, 1, 2)

        self.label_19 = QLabel(self.gMeasurement)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_9.addWidget(self.label_19, 2, 4, 1, 1)

        self.label_24 = QLabel(self.gMeasurement)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.label_24, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.gMeasurement, 2, 0, 1, 2)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_11 = QGridLayout(self.groupBox)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.PosRel = QLabel(self.groupBox)
        self.PosRel.setObjectName(u"PosRel")
        self.PosRel.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.PosRel, 1, 3, 1, 1)

        self.label_20 = QLabel(self.groupBox)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_20, 2, 4, 1, 1)

        self.Length = QDoubleSpinBox(self.groupBox)
        self.Length.setObjectName(u"Length")
        self.Length.setDecimals(3)
        self.Length.setMaximum(1000.000000000000000)
        self.Length.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.Length.setValue(10.000000000000000)

        self.gridLayout_11.addWidget(self.Length, 2, 5, 1, 1)

        self.PosRaw2 = QLabel(self.groupBox)
        self.PosRaw2.setObjectName(u"PosRaw2")
        self.PosRaw2.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.PosRaw2, 2, 1, 1, 1)

        self.PosRaw = QLabel(self.groupBox)
        self.PosRaw.setObjectName(u"PosRaw")
        self.PosRaw.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.PosRaw, 1, 1, 1, 1)

        self.PosZero = QPushButton(self.groupBox)
        self.PosZero.setObjectName(u"PosZero")

        self.gridLayout_11.addWidget(self.PosZero, 2, 3, 1, 1)

        self.PosBar = QProgressBar(self.groupBox)
        self.PosBar.setObjectName(u"PosBar")
        self.PosBar.setEnabled(True)
        self.PosBar.setMaximum(1000)
        self.PosBar.setValue(24)

        self.gridLayout_11.addWidget(self.PosBar, 3, 1, 1, 5)

        self.PosAbs2 = QLabel(self.groupBox)
        self.PosAbs2.setObjectName(u"PosAbs2")
        self.PosAbs2.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.PosAbs2, 2, 2, 1, 1)

        self.PosAbs = QLabel(self.groupBox)
        self.PosAbs.setObjectName(u"PosAbs")
        self.PosAbs.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.PosAbs, 1, 2, 1, 1)

        self.PosNorm = QLabel(self.groupBox)
        self.PosNorm.setObjectName(u"PosNorm")
        self.PosNorm.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.PosNorm, 1, 4, 1, 2)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label, 0, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_2, 0, 2, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_3, 0, 3, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout_11.addWidget(self.label_5, 0, 4, 1, 2)


        self.gridLayout_2.addWidget(self.groupBox, 3, 0, 1, 2)


        self.gridLayout_6.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1021, 22))
        self.menuLog = QMenu(self.menubar)
        self.menuLog.setObjectName(u"menuLog")
        self.menuQuery = QMenu(self.menubar)
        self.menuQuery.setObjectName(u"menuQuery")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuLog.menuAction())
        self.menubar.addAction(self.menuQuery.menuAction())
        self.menuLog.addAction(self.LogAll)
        self.menuLog.addAction(self.LogNone)
        self.menuLog.addSeparator()
        self.menuLog.addAction(self.LogXY)
        self.menuLog.addAction(self.LogZ)
        self.menuLog.addAction(self.LogFineZ)
        self.menuLog.addAction(self.LogADC)
        self.menuQuery.addAction(self.QueryAll)
        self.menuQuery.addAction(self.QueryNone)
        self.menuQuery.addSeparator()
        self.menuQuery.addAction(self.QueryXYposition)
        self.menuQuery.addAction(self.QueryXYerror)
        self.menuQuery.addAction(self.QueryZposition)
        self.menuQuery.addAction(self.QueryFineZposition)
        self.menuQuery.addAction(self.QueryFineZvoltage)
        self.menuQuery.addAction(self.QueryFineZerror)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MicroDeform", None))
        self.LogXY.setText(QCoreApplication.translate("MainWindow", u"XY", None))
        self.LogZ.setText(QCoreApplication.translate("MainWindow", u"Z", None))
        self.LogFineZ.setText(QCoreApplication.translate("MainWindow", u"Fine Z", None))
        self.LogADC.setText(QCoreApplication.translate("MainWindow", u"ADC", None))
        self.LogNone.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.LogAll.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.QueryXYposition.setText(QCoreApplication.translate("MainWindow", u"XY position", None))
        self.QueryXYerror.setText(QCoreApplication.translate("MainWindow", u"XY error", None))
        self.QueryZposition.setText(QCoreApplication.translate("MainWindow", u"Z position", None))
        self.QueryFineZposition.setText(QCoreApplication.translate("MainWindow", u"Fine Z position", None))
        self.QueryFineZvoltage.setText(QCoreApplication.translate("MainWindow", u"Fine Z voltage", None))
        self.QueryFineZerror.setText(QCoreApplication.translate("MainWindow", u"Fine Z error", None))
        self.QueryAll.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.QueryNone.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.actionCompression.setText(QCoreApplication.translate("MainWindow", u"Compression", None))
        self.actionTension.setText(QCoreApplication.translate("MainWindow", u"Tension", None))
        self.gTest.setTitle(QCoreApplication.translate("MainWindow", u"Test", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Filename", None))
        self.Record.setText(QCoreApplication.translate("MainWindow", u"Record Data", None))
        self.Compression.setText(QCoreApplication.translate("MainWindow", u"Compression", None))
        self.Tension.setText(QCoreApplication.translate("MainWindow", u"Tension", None))
        self.LoadWaitUnload.setText(QCoreApplication.translate("MainWindow", u"Load\n"
"Wait\n"
"Unload", None))
        self.UnloadSpeed.setSuffix(QCoreApplication.translate("MainWindow", u" \u03bcm/s", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Speed", None))
        self.LoadStep.setSuffix(QCoreApplication.translate("MainWindow", u" \u03bcm", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Wait", None))
        self.Unload.setText(QCoreApplication.translate("MainWindow", u"Unload", None))
        self.Wait.setSuffix(QCoreApplication.translate("MainWindow", u" s", None))
        self.UnloadStep.setSuffix(QCoreApplication.translate("MainWindow", u" \u03bcm", None))
        self.UnloadStepNorm.setSuffix(QCoreApplication.translate("MainWindow", u" \u03bcm/\u03bcm", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Normalized", None))
        self.Load.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Speed", None))
        self.UnloadSpeedNorm.setSuffix(QCoreApplication.translate("MainWindow", u" 1/s", None))
        self.LoadStepNorm.setSuffix(QCoreApplication.translate("MainWindow", u" \u03bcm/\u03bcm", None))
        self.LoadSpeed.setSuffix(QCoreApplication.translate("MainWindow", u" \u03bcm/s", None))
        self.LoadSpeedNorm.setSuffix(QCoreApplication.translate("MainWindow", u" 1/s", None))
        self.gPlot.setTitle(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.PlotTime.setText(QCoreApplication.translate("MainWindow", u"Load(Time); Position(Time)", None))
        self.PlotXY.setText(QCoreApplication.translate("MainWindow", u"Load(Position)", None))
        self.PlotClear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.gFine.setTitle(QCoreApplication.translate("MainWindow", u"Fine movement", None))
        self.FZSpeed.setSuffix(QCoreApplication.translate("MainWindow", u" \u03bcm/s", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Speed", None))
        self.FZPos.setText(QCoreApplication.translate("MainWindow", u"30.000 \u03bcm", None))
        self.FZMinus.setText(QCoreApplication.translate("MainWindow", u"Fine Z-", None))
        self.FZPlus.setText(QCoreApplication.translate("MainWindow", u"Fine Z+", None))
        self.Stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.gCoarse.setTitle(QCoreApplication.translate("MainWindow", u"Coarse movement", None))
        self.XMinus.setText(QCoreApplication.translate("MainWindow", u"X-", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Speed", None))
        self.XPlus.setText(QCoreApplication.translate("MainWindow", u"X+", None))
        self.XSpeed.setSuffix(QCoreApplication.translate("MainWindow", u" \u03bcm/s", None))
        self.ZPlus.setText(QCoreApplication.translate("MainWindow", u"Z+", None))
        self.ZSpeed.setSuffix(QCoreApplication.translate("MainWindow", u" \u03bcm/s", None))
        self.ZMinus.setText(QCoreApplication.translate("MainWindow", u"Z-", None))
        self.ZPos.setText(QCoreApplication.translate("MainWindow", u"\u00b112000.5 \u03bcm", None))
        self.YPlus.setText(QCoreApplication.translate("MainWindow", u"Y+", None))
        self.XPos.setText(QCoreApplication.translate("MainWindow", u"\u00b112000.000 \u03bcm", None))
        self.YPos.setText(QCoreApplication.translate("MainWindow", u"\u00b112000.000 \u03bcm", None))
        self.YMinus.setText(QCoreApplication.translate("MainWindow", u"Y-", None))
        self.YSpeed.setSuffix(QCoreApplication.translate("MainWindow", u" \u03bcm/s", None))
        self.gADCMonitor.setTitle(QCoreApplication.translate("MainWindow", u"ADC Monitor", None))
        self.gMeasurement.setTitle(QCoreApplication.translate("MainWindow", u"Load", None))
        self.LoadNorm.setText(QCoreApplication.translate("MainWindow", u"? GPa", None))
        self.LoadZero.setText(QCoreApplication.translate("MainWindow", u"Rel. Zero", None))
        self.LoadAbs.setText(QCoreApplication.translate("MainWindow", u"? N", None))
        self.Area.setSuffix(QCoreApplication.translate("MainWindow", u" \u03bcm\u00b2", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Absolute", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Relative", None))
        self.LoadRaw.setText(QCoreApplication.translate("MainWindow", u"? V", None))
        self.LoadRel.setText(QCoreApplication.translate("MainWindow", u"? N", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Sample normalized", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Area", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Raw", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Position", None))
        self.PosRel.setText(QCoreApplication.translate("MainWindow", u"?  \u03bcm", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Length", None))
        self.Length.setSuffix(QCoreApplication.translate("MainWindow", u" \u03bcm", None))
        self.PosRaw2.setText(QCoreApplication.translate("MainWindow", u"? V", None))
        self.PosRaw.setText(QCoreApplication.translate("MainWindow", u"? V", None))
        self.PosZero.setText(QCoreApplication.translate("MainWindow", u"Rel. Zero", None))
        self.PosAbs2.setText(QCoreApplication.translate("MainWindow", u"?  \u03bcm", None))
        self.PosAbs.setText(QCoreApplication.translate("MainWindow", u"?  \u03bcm", None))
        self.PosNorm.setText(QCoreApplication.translate("MainWindow", u"?  \u03bcm/\u03bcm", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Raw", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Absolute", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Relative", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Sample normalized", None))
        self.menuLog.setTitle(QCoreApplication.translate("MainWindow", u"Log", None))
        self.menuQuery.setTitle(QCoreApplication.translate("MainWindow", u"Query", None))
    # retranslateUi

