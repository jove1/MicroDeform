#!/usr/bin/env python3

import sys
import logging

# Z
# range:      ~4300 steps  nominal 10mm
# resolution: 2.5um/step
# max speed:  [2000um/s] 1000steps/s  nominal >5mm/s
# accel:      [inf]
# XY
# range:      nominal 12mm
# resolution: 1nm
# max speed:  [2mm/s] nominal 2/10 mm/s
# accel:              default 5 mm/s2
# FZ
# range:      30um
# max speed:  [5um/s]
# accel:      default

from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog, QMainWindow
from PySide6.QtCore import Signal, Qt, QSignalBlocker
from PySide6.QtGui import QPalette

def setValueNoSignal(obj, value):
    with QSignalBlocker(obj):
        obj.setValue(value)

def setColor(obj, role, color=None):
    palette = QPalette()
    if color:
        palette.setColor(role, color)
    obj.setPalette(palette)


class Window(QMainWindow):
    adc_data = Signal(object)
    xy_pos = Signal(float, float)
    xy_err = Signal(str)
    z_pos = Signal(float, int)
    fz_pos = Signal(float)
    fz_volt = Signal(float)
    fz_err = Signal(int)
    #fz_status = Signal(str)

    def __init__(self, md):
        super(Window, self).__init__()
        self.md = md
        self.adc_data.connect( md.adc_data )
        self.xy_pos.connect( md.xy_pos )
        self.xy_err.connect( md.xy_err )
        self.z_pos.connect( md.z_pos )
        self.fz_pos.connect( md.fz_pos )
        self.fz_volt.connect( md.fz_volt )
        self.fz_err.connect( md.fz_err )
        #self.fz_status.connect( md.fz_status )
        self.logger = logging.getLogger(self.__class__.__name__)

    def keyPressEvent(self, ev):
        if ev.isAutoRepeat():
            return
        self.logger.info("keyPressEvent(%s)", ev)

        key = ev.key()
        if key == Qt.Key_Escape:       self.md.AllStop()

        mod = ev.modifiers()
        if (mod & Qt.ShiftModifier) or \
           (mod & Qt.KeypadModifier):
            if key == Qt.Key_Left:     self.md.XMinus()
            if key == Qt.Key_Right:    self.md.XPlus()

            if key == Qt.Key_Down:     self.md.YMinus()
            if key == Qt.Key_Up:       self.md.YPlus()

            if key == Qt.Key_PageDown: self.md.ZMinus()
            if key == Qt.Key_PageUp:   self.md.ZPlus()

            if key == Qt.Key_End:      self.md.FZMinus()
            if key == Qt.Key_Home:     self.md.FZPlus()

    def keyReleaseEvent(self, ev):
        if ev.isAutoRepeat():
            return

        key = ev.key()
        if key == Qt.Key_Left:         self.md.XStop()
        if key == Qt.Key_Right:        self.md.XStop()

        if key == Qt.Key_Down:         self.md.YStop()
        if key == Qt.Key_Up:           self.md.YStop()

        if key == Qt.Key_PageDown:     self.md.ZStop()
        if key == Qt.Key_PageUp:       self.md.ZStop()

        if key == Qt.Key_Home:         self.md.FZStop()
        if key == Qt.Key_End:          self.md.FZStop()

    def focusOutEvent(self, ev):
        self.md.XStop()
        self.md.YStop()
        self.md.ZStop()
        self.md.FZStop()

    def closeEvent(self, arg):
        QApplication.quit()

    def timerEvent(self, ev):
        self.md.Tick()


import numpy as np
class History:
    def __init__(self, maxlen=2048):
        self.maxlen = maxlen
        self.clear()

    def clear(self):
        self.pos = 0
        self.x = []
        self.y1 = []
        self.y2 = []

    def trim(self):
        if self.maxlen:
            self.x = self.x[-self.maxlen:]
            self.y1 = self.y1[-self.maxlen:]
            self.y2 = self.y2[-self.maxlen:]

    def update(self, y1, y2):
        n = len(y1)
        x = np.arange(self.pos, self.pos+n)
        self.pos += n
        self.x.extend(x)
        self.y1.extend(y1)
        self.y2.extend(y2)
        self.trim()


import pyqtgraph as pg
def twinx_plot(pw, llabel, rlabel):
    # adapted from https://github.com/pyqtgraph/pyqtgraph/blob/master/pyqtgraph/examples/MultiplePlotAxes.py
    p1 = pw.plotItem
    p2 = pg.ViewBox()

    p1.scene().addItem(p2)
    p2.setXLink(p1)

    ax = p1.getAxis('left')
    ax.setPen((0,2))
    ax.setTextPen((0,2))
    ax.setLabel(llabel)

    p1.showAxis('right')
    ax = p1.getAxis('right')
    ax.linkToView(p2)
    ax.setPen((1,2))
    ax.setTextPen((1,2))
    ax.setLabel(rlabel)

    l1, = p1.plot([], [], pen=(0,2)),
    l2 = pg.PlotDataItem([], [], pen=(1,2))
    p2.addItem(l2)

    def update():
        p2.setGeometry(p1.vb.sceneBoundingRect())
        p2.linkedViewChanged(p1.vb, p2.XAxis)
    update()
    p1.vb.sigResized.connect(update)

    return (l1, l2)


from . import hw
from .main_window import Ui_MainWindow
from .piezo_errors import errors as fz_errors

class MicroDeform:
    def __init__(self):
        self.cycle_time = 50e-6 # SPA? 1 0x0E000200
        self.wave_memory = 8192 # SPA? 1 0x13000004

        self.calib_position = lambda x: x/0.66666666 + 15 # um/V, nominal calibration
        self.calib_load = 3.434329*9.806 # mN/V
        self.calib_spring = 13.94  # mN/um

        self.load_hi = 6
        self.load_lo = -6

        self.window = Window(self)

        try:
            self.xy = hw.XY()
        except:
            self.xy = hw.XY(dummy=True)
        try:
            self.z = hw.Z()
        except:
            self.z = hw.Z(dummy=True)
        try:
            self.fz = hw.Piezo()
        except:
            self.fz = hw.Piezo(dummy=True)
        try:
            self.adc = hw.ADC(self.window.adc_data.emit)
        except:
            self.adc = hw.ADC(self.window.adc_data.emit, dummy=True)


        self.ui = ui = Ui_MainWindow()
        ui.setupUi(self.window)

        setColor(self.ui.Stop, QPalette.Button, Qt.red)
        setColor(self.ui.Record, QPalette.Button, Qt.darkGreen)

        self.ui.ZSpeed.setMinimum(self.z.step_size)
        self.ui.ZSpeed.setMaximum(1000*self.z.step_size)

        ui.Length.valueChanged.connect( lambda val: setValueNoSignal(ui.LoadStepNorm, self.LoadStep/self.Length) )
        ui.Length.valueChanged.connect( lambda val: setValueNoSignal(ui.LoadSpeedNorm, self.LoadSpeed/self.Length) )
        ui.Length.valueChanged.connect( lambda val: setValueNoSignal(ui.UnloadStepNorm, self.UnloadStep/self.Length) )
        ui.Length.valueChanged.connect( lambda val: setValueNoSignal(ui.UnloadSpeedNorm, self.UnloadSpeed/self.Length) )

        ui.LoadStep.valueChanged.connect( lambda val: setValueNoSignal(ui.LoadStepNorm, self.LoadStep/self.Length) )
        ui.LoadSpeed.valueChanged.connect( lambda val: setValueNoSignal(ui.LoadSpeedNorm, self.LoadSpeed/self.Length) )
        ui.UnloadStep.valueChanged.connect( lambda val: setValueNoSignal(ui.UnloadStepNorm, self.UnloadStep/self.Length) )
        ui.UnloadSpeed.valueChanged.connect( lambda val: setValueNoSignal(ui.UnloadSpeedNorm, self.UnloadSpeed/self.Length) )

        ui.LoadStepNorm.valueChanged.connect( lambda val: setValueNoSignal(ui.LoadStep, self.LoadStepNorm*self.Length) )
        ui.LoadSpeedNorm.valueChanged.connect( lambda val: setValueNoSignal(ui.LoadSpeed, self.LoadSpeedNorm*self.Length) )
        ui.UnloadStepNorm.valueChanged.connect( lambda val: setValueNoSignal(ui.UnloadStep, self.UnloadStepNorm*self.Length) )
        ui.UnloadSpeedNorm.valueChanged.connect( lambda val: setValueNoSignal(ui.UnloadSpeed, self.UnloadSpeedNorm*self.Length) )

        logActions = [ui.LogXY, ui.LogZ, ui.LogFineZ, ui.LogADC, ui.LogKeyboard]
        ui.LogAll.triggered.connect( lambda checked: [a.setChecked(True) for a in logActions] )
        ui.LogNone.triggered.connect( lambda checked: [a.setChecked(False) for a in logActions] )
        ui.LogXY.toggled.connect( lambda checked: self.xy.logger.setLevel(logging.DEBUG if checked else logging.WARNING) )
        ui.LogZ.toggled.connect( lambda checked: self.z.logger.setLevel(logging.DEBUG if checked else logging.WARNING) )
        ui.LogFineZ.toggled.connect( lambda checked: self.fz.logger.setLevel(logging.DEBUG if checked else logging.WARNING) )
        ui.LogADC.toggled.connect( lambda checked: self.adc.logger.setLevel(logging.DEBUG if checked else logging.WARNING) )
        ui.LogKeyboard.toggled.connect( lambda checked: self.window.logger.setLevel(logging.DEBUG if checked else logging.WARNING) )

        queryActions = [ui.QueryXYposition, ui.QueryXYerror, ui.QueryZposition, ui.QueryFineZposition, ui.QueryFineZvoltage, ui.QueryFineZerror]
        ui.QueryAll.triggered.connect( lambda checked: [a.setChecked(True) for a in queryActions] )
        ui.QueryNone.triggered.connect( lambda checked: [a.setChecked(False) for a in queryActions] )

        ui.QueryXYposition.toggled.connect( lambda checked: [ui.XPos.setText("? μm"), ui.YPos.setText("? μm")] if not checked else None )
        ui.QueryZposition.toggled.connect( lambda checked: ui.ZPos.setText("? μm") if not checked else None )
        ui.QueryFineZposition.toggled.connect( lambda checked: [ui.FZPos.setText("? μm"), ui.PosAbs2.setText("? μm")] if not checked else None )
        ui.QueryFineZvoltage.toggled.connect( lambda checked: ui.PosRaw2.setText("? V") if not checked else None )

        #
        # Plot
        #
        self.history = History(10000)

        self.monitor_lines = twinx_plot(ui.plotMonitor, "Raw Pos. [V]", "Raw Load [V]")
        self.history_lines = twinx_plot(ui.plotHistory, "Position [μm]", "Load [mN]")

        ui.plotXY.plot([], [], pen=(0,2), title="XY")
        ui.plotXY.plot([], [], symbolBrush=None, symbolPen=(1,2), symbol="o" )
        self.xy_lines = ui.plotXY.listDataItems()

        ui.PlotClear.clicked.connect( lambda checked: self.history.clear() )

        #
        # Buttons
        #
        self.fh = None
        ui.Record.clicked.connect( self.Record )

        self.last_pos = 0
        self.last_load = 0
        self.zero_pos = 0
        self.zero_load = 0
        ui.LoadZero.clicked.connect( lambda : setattr(self, "zero_load", self.last_load))
        ui.PosZero.clicked.connect( lambda : setattr(self, "zero_pos", self.last_pos))

        ui.Load.clicked.connect(   lambda : [ self.fz.cmd("VEL 1 {}", self.LoadSpeed),   self.fz.cmd("MVR 1 {}", self.LoadStep if ui.Compression.isChecked() else -self.LoadStep) ])
        ui.Unload.clicked.connect( lambda : [ self.fz.cmd("VEL 1 {}", self.UnloadSpeed), self.fz.cmd("MVR 1 {}", -self.UnloadStep if ui.Compression.isChecked() else self.UnloadStep) ])
        ui.LoadWaitUnload.clicked.connect( self.LoadWaitUnload )

        ui.Stop.clicked.connect(     self.AllStop )

        self.Xmoving = False
        self.Ymoving = False
        self.Zmoving = False
        self.FZmoving = False

        ui.XMinus.pressed.connect(   self.XMinus  )
        ui.XPlus.pressed.connect (   self.XPlus   )
        ui.YMinus.pressed.connect(   self.YMinus  )
        ui.YPlus.pressed.connect (   self.YPlus   )
        ui.ZMinus.pressed.connect(   self.ZMinus  )
        ui.ZPlus.pressed.connect (   self.ZPlus   )
        ui.FZMinus.pressed.connect(  self.FZMinus )
        ui.FZPlus.pressed.connect (  self.FZPlus  )

        ui.XMinus.released.connect(  self.XStop   )
        ui.XPlus.released.connect (  self.XStop   )
        ui.YMinus.released.connect(  self.YStop   )
        ui.YPlus.released.connect (  self.YStop   )
        ui.ZMinus.released.connect(  self.ZStop   )
        ui.ZPlus.released.connect (  self.ZStop   )
        ui.FZMinus.released.connect( self.FZStop  )
        ui.FZPlus.released.connect ( self.FZStop  )

        self.msgbox = QMessageBox(QMessageBox.Warning, "Error", "", parent=self.window)
        self.msgbox.setWindowModality(Qt.NonModal)

        self.window.setFocus()
        self.window.show()
        self.window.startTimer(500)

        if any([self.xy.dummy, self.z.dummy, self.adc.dummy, self.fz.dummy]):
            self.msgbox.setWindowTitle("Error")
            self.msgbox.setText("Some devices could not be found:\n"
                    f"XY: {self.xy.device}\n"
                    f"Z: {self.z.device}\n"
                    f"FineZ: {self.fz.device}\n"
                    f"ADC: {self.adc.device}\n"
                    )
            self.msgbox.show()


    def __getattr__(self, name):
        return getattr(self.ui, name).value()


    def Tick(self):
        if self.ui.QueryXYposition.isChecked():
            self.xy.pos( self.window.xy_pos.emit )
        if self.ui.QueryXYerror.isChecked():
            self.xy.err( self.window.xy_err.emit )
        if self.ui.QueryZposition.isChecked():
            self.z.pos( self.window.z_pos.emit )
        if self.ui.QueryFineZposition.isChecked():
            self.fz.pos( self.window.fz_pos.emit )
        if self.ui.QueryFineZvoltage.isChecked():
            self.fz.volt( self.window.fz_volt.emit )
        if self.ui.QueryFineZerror.isChecked():
            self.fz.err( self.window.fz_err.emit )

        #self.fz.cmd("WGO?").callback( self.window.fz_status.emit )


    def XPlus(self):   self.xy.move(1, self.XSpeed, +12000); self.Xmoving = True
    def XMinus(self):  self.xy.move(1, self.XSpeed, -12000); self.Xmoving = True
    def XStop(self):
        if self.Xmoving:
            self.xy.stop(1)
            self.Xmoving = False

    def YPlus(self):   self.xy.move(2, self.YSpeed, +12000); self.Ymoving = True
    def YMinus(self):  self.xy.move(2, self.YSpeed, -12000); self.Ymoving = True
    def YStop(self):
        if self.Ymoving:
            self.xy.stop(2)
            self.Ymoving = False

    def ZPlus(self):   self.z.move(self.ZSpeed, +12500); self.Zmoving = True
    def ZMinus(self):  self.z.move(self.ZSpeed, -12500); self.Zmoving = True
    def ZStop(self):
        if self.Zmoving:
            self.z.stop()
            self.Zmoving = False

    def FZPlus(self):  self.fz.move(self.FZSpeed, 30); self.FZmoving = True
    def FZMinus(self): self.fz.move(self.FZSpeed, 0); self.FZmoving = True
    def FZStop(self):
        if self.FZmoving:
            self.fz.stop()
            self.FZmoving = False

    def AllStop(self):
        self.z.stop()
        self.xy.cmd("0 STP")
        #self.xy.cmd("0 EST") # emergency stop
        self.fz.stop()

    def Record(self):
        if self.fh:
            self.fh.close()
            self.fh = None
            self.ui.Record.setText("Record")
            self.ui.FileName.setText("")
            setColor(self.ui.Record, QPalette.Button, Qt.darkGreen)
        else:
            fname, _ = QFileDialog.getSaveFileName(self.window, "Save data", filter="Data files (*.dat)")
            if not fname:
                return
            with open(fname+".txt", "w") as fh:
                fh.write(f"""{{
'area': {self.Area},
'length': {self.Length},
'zero_pos': {self.zero_pos},
'zero_load': {self.zero_load},
'calib_spring': {self.calib_spring},
'calib_load': {self.calib_load},
}}""")
            self.fh = open(fname, "wb")
            self.ui.Record.setText("Stop")
            self.ui.FileName.setText(fname)
            setColor(self.ui.Record, QPalette.Button, Qt.red)


    def LoadWaitUnload(self):
        t1 = abs(self.LoadStep/self.LoadSpeed)
        t2 = self.Wait
        t3 = abs(self.UnloadStep/self.UnloadSpeed)
        rate = int( (t1+t2+t3)/self.cycle_time/self.wave_memory*1.1 )
        l1 = int(t1/self.cycle_time/rate)
        l2 = int(t2/self.cycle_time/rate)
        l3 = int(t3/self.cycle_time/rate)
        if self.ui.Compression.isChecked():
            self.fz.cmd("WAV 1 X LIN {} {} {} {} 0 0", l1+l2, self.LoadStep, 0, l1)
            self.fz.cmd("WAV 1 & LIN {} {} {} {} 0 0", l3, -self.UnloadStep, self.LoadStep, l3)
        else:
            self.fz.cmd("WAV 1 X LIN {} {} {} {} 0 0", l1+l2, -self.LoadStep, 0, l1)
            self.fz.cmd("WAV 1 & LIN {} {} {} {} 0 0", l3, self.UnloadStep, -self.LoadStep, l3)
        self.fz.cmd("WTR 1 {} 1", rate) # straight line interpolation
        self.fz.cmd("WSL 1 1") # 1st wave table
        self.fz.cmd("WGC 1 1") # 1 cycle
        offset = float(self.fz.cmd("POS?").result()[2:])
        self.fz.cmd("WOS 1 {}", offset) # offset
        self.fz.cmd("WGO 1 257") # start, final position is the endpoint

    def xy_pos(self, x, y):
        self.ui.XPos.setText(f"{x: .3f} μm")
        self.ui.YPos.setText(f"{y: .3f} μm")

    def xy_err(self, s):
        if s:
            self.msgbox.setWindowTitle("XY Error")
            self.msgbox.setText(s)
            self.msgbox.show()

    def z_pos(self, z, lim):
        self.ui.ZPos.setText(f"{z: .3f} μm")
        setColor(self.ui.ZPos, QPalette.WindowText, Qt.red if lim else None)

    def fz_pos(self, v):
        self.ui.FZPos.setText(f"{v: .3f} μm")
        self.ui.PosAbs2.setText(f"{v: .6f} μm")

    def fz_volt(self, v):
        self.ui.PosRaw2.setText(f"{v: .6f} V")

    def fz_err(self, err):
        if err not in (0, 10):
            self.msgbox.setWindowTitle("Fine Z Error")
            self.msgbox.setText(f"Error {err}: {fz_errors[err]}")
            self.msgbox.show()

    #def fz_status(self, s):
    #    if not s: return
    #    running = int(s[6:])
    #    if not running and self.was_running:
    #        QMessageBox.information(window, "Done", "Done.")
    #    self.was_running = running

    def adc_data(self, data):
        #
        # Raw values [V]
        #

        pos, load = data[:,0], data[:,1]

        x = np.arange(len(data))
        self.monitor_lines[0].setData(x, data[:,0])
        self.monitor_lines[1].setData(x, data[:,1])

        pos_m, pos_s = pos.mean(), pos.std()
        load_m, load_s = load.mean(), load.std()

        self.ui.PosRaw.setText(f"{pos_m: .6f}\n±{pos_s:.6f} V")
        self.ui.LoadRaw.setText(f"{load_m: .6f}\n±{load_s:.6f} V")

        self.ui.PosBar.setValue( (pos_m+10)/20*1000 )
        self.ui.LoadBar.setValue( (load_m+10)/20*1000 )
        self.ui.PosBar.setFormat(f"{pos_m: .1f} V")
        self.ui.LoadBar.setFormat(f"{load_m: .1f} V")

        setColor(self.ui.LoadBar, QPalette.Highlight, Qt.darkGreen if self.load_lo < load_m < self.load_hi else Qt.red)

        #
        # Calibrated values [um], [mN]
        #

        pos = self.calib_position(pos)
        load = self.calib_load * load

        if self.fh:
            self.fh.write(np.column_stack([pos,load]))

        load_m, load_s = load.mean(), load.std()
        pos_m, pos_s = pos.mean(), pos.std()

        self.ui.PosAbs.setText(f"{pos_m: .6f}\n±{pos_s:.6f} μm")
        self.ui.LoadAbs.setText(f"{load_m: .3f}\n±{load_s:.3f} mN")

        self.last_pos = pos_m
        self.last_load = load_m

        self.history.update([pos_m], [load_m])
        h = self.History
        time = np.array(self.history.x[-h:]) * self.adc.N / self.adc.rate
        pos = np.array(self.history.y1[-h:])
        load = np.array(self.history.y2[-h:])

        #
        # Zero, compression/tension flip and normalization [um/um], [MPa]
        #

        pos_m -= self.zero_pos
        pos -= self.zero_pos
        load_m -= self.zero_load
        load -= self.zero_load
        if self.ui.Compression.isChecked():
            load_m *= -1
            load *= -1
        else:
            pos_m *= -1
            pos *= -1

        self.ui.PosRel.setText(f"{pos_m: .6f} μm")
        self.ui.LoadRel.setText(f"{load_m: .3f} mN")

        self.ui.PosNorm.setText(f"{pos_m/self.Length: .6f} μm/μm")
        self.ui.LoadNorm.setText(f"{load_m/self.Area*1000: .3f} MPa")


        idx = self.ui.PlotType.currentIndex()
        if idx in (1, 3):
            pos -= load/self.calib_spring

        if idx in (0, 1):
            self.ui.stackedWidget.setCurrentIndex(0)
            self.history_lines[0].setData(time, pos)
            self.history_lines[1].setData(time, load)

        elif idx in (2, 3):
            self.ui.stackedWidget.setCurrentIndex(1)
            self.xy_lines[0].setData(pos, load)
            self.xy_lines[1].setData(pos[-1:], load[-1:])



def main():
    logging.basicConfig()
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    md = MicroDeform()

    with md.xy as xy, md.z as z, md.fz as fz, md.adc as adc:

        xy.logger.setLevel(logging.DEBUG if md.ui.LogXY.isChecked() else logging.WARNING)
        z.logger.setLevel(logging.DEBUG if md.ui.LogZ.isChecked() else logging.WARNING)
        fz.logger.setLevel(logging.DEBUG if md.ui.LogFineZ.isChecked() else logging.WARNING)
        adc.logger.setLevel(logging.DEBUG if md.ui.LogADC.isChecked() else logging.WARNING)
        md.window.logger.setLevel(logging.DEBUG if md.ui.LogKeyboard.isChecked() else logging.WARNING)


        xy_ver = xy.cmd("0 VER ?").result()
        print(xy_ver)
        if not xy.dummy:
            assert xy_ver == "#MMC-110_v1E.95\n\r#MMC-110_v1E.95\r\n\r", xy_ver
        xy.cmd("0 ACC 5")
        xy.cmd("0 DEC 5")
        xy.cmd("0 MOT 1")

        fz.cmd("*IDN?").callback(print)
        fz.cmd("SVO 1 1") # servo on
        fz.cmd("CCL 1 advanced")
        fz.cmd("SPA 2 0x0A000003 2")   # Select Output Type: 2 = "current position of axis"
        fz.cmd("SPA 2 0x0A000004 1")   # Select Output Index: axis identifier is 1
        # 0-30 μm -> 0-6 V
        #fz.cmd("SPA 1 0x07001005 0.2") # Position Report Scaling
        #fz.cmd("SPA 1 0x07001006 0")   # Position Report Offset
        # 0-30 μm -> -10-10 V
        fz.cmd("SPA 1 0x07001005 0.66666666") # Position Report Scaling
        fz.cmd("SPA 1 0x07001006 -15")   # Position Report Offset
        #fz.cmd("SPA 1 0x07000500 1") Axis matrix
        #fz.cmd("SPA 1 0x07000501 0")

        return app.exec()

if __name__ == "__main__":
    sys.exit(main())
