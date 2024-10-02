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

import re
num = r"([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)"

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
    xy_pos = Signal(str)
    xy_err = Signal(str)
    z_pos = Signal(str)
    fz_pos = Signal(str)
    fz_volt = Signal(str)
    fz_err = Signal(str)
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

    def keyPressEvent(self, ev):
        if ev.isAutoRepeat():
            return

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

            if key == Qt.Key_Home:     self.md.FZMinus()
            if key == Qt.Key_End:      self.md.FZPlus()

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

        self.position_calib = lambda x: x/0.66666666 + 15 # nominal calibration
        self.load_calib = lambda x: x*3.434329*9.806 # mN

        self.load_hi = 6
        self.load_lo = -6

        self.z_ustep = 16
        self.z_step_size = 2.5/self.z_ustep

        self.window = Window(self)
        self.ui = ui = Ui_MainWindow()
        ui.setupUi(self.window)

        setColor(self.ui.Stop, QPalette.Button, Qt.red)
        setColor(self.ui.Record, QPalette.Button, Qt.darkGreen)

        self.ui.ZSpeed.setMinimum(self.z_step_size)
        self.ui.ZSpeed.setMaximum(1000*self.z_step_size)

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

        logActions = [ui.LogXY, ui.LogZ, ui.LogFineZ, ui.LogADC]
        ui.LogAll.triggered.connect( lambda checked: [a.setChecked(True) for a in logActions] )
        ui.LogNone.triggered.connect( lambda checked: [a.setChecked(False) for a in logActions] )
        ui.LogXY.toggled.connect( lambda checked: self.xy.logger.setLevel(logging.DEBUG if checked else logging.WARNING) )
        ui.LogZ.toggled.connect( lambda checked: self.z.logger.setLevel(logging.DEBUG if checked else logging.WARNING) )
        ui.LogFineZ.toggled.connect( lambda checked: self.fz.logger.setLevel(logging.DEBUG if checked else logging.WARNING) )
        ui.LogADC.toggled.connect( lambda checked: self.adc.logger.setLevel(logging.DEBUG if checked else logging.WARNING) )

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

        self.monitor_lines = twinx_plot(ui.plotMonitor, "Position", "Load")
        self.history_lines = twinx_plot(ui.plotHistory, "Position", "Load")

        ui.plotXY.plot([], [], pen=(0,2), title="XY")
        ui.plotXY.plot([], [], symbolBrush=None, symbolPen=(1,2), symbol="o" )
        self.xy_lines = ui.plotXY.listDataItems()

        ui.PlotTime.toggled.connect( lambda checked: ui.stackedWidget.setCurrentIndex(0) if checked else None)
        ui.PlotXY.toggled.connect( lambda checked: ui.stackedWidget.setCurrentIndex(1) if checked else None)
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
            self.xy.cmd("0 POS ?").callback( self.window.xy_pos.emit )
        if self.ui.QueryXYerror.isChecked():
            self.xy.cmd("0 ERR ?").callback( self.window.xy_err.emit )
        if self.ui.QueryZposition.isChecked():
            self.z.cmd("?").callback( self.window.z_pos.emit )
        if self.ui.QueryFineZposition.isChecked():
            self.fz.cmd("POS?").callback( self.window.fz_pos.emit )
        if self.ui.QueryFineZvoltage.isChecked():
            self.fz.cmd("VOL? 2").callback( self.window.fz_volt.emit )
        if self.ui.QueryFineZerror.isChecked():
            self.fz.cmd("ERR?").callback( self.window.fz_err.emit )

        #self.fz.cmd("WGO?").callback( self.window.fz_status.emit )


    def XPlus(self):   self.xy.cmd("1 VEL {}", self.XSpeed/1000); self.xy.cmd("1 MVR 12"); self.Xmoving = True
    def XMinus(self):  self.xy.cmd("1 VEL {}", self.XSpeed/1000); self.xy.cmd("1 MVR -12"); self.Xmoving = True
    def XStop(self):
        if self.Xmoving:
            self.xy.cmd("1 STP")
            self.Xmoving = False

    def YPlus(self):   self.xy.cmd("2 VEL {}", self.YSpeed/1000); self.xy.cmd("2 MVR 12"); self.Ymoving = True
    def YMinus(self):  self.xy.cmd("2 VEL {}", self.YSpeed/1000); self.xy.cmd("2 MVR -12"); self.Ymoving = True
    def YStop(self):
        if self.Ymoving:
            self.xy.cmd("2 STP")
            self.Ymoving = False

    def ZPlus(self):   self.z.cmd("vel {}", int(round(self.ZSpeed/self.z_step_size)) ); self.z.cmd("rel {}", 5000*self.z_ustep); self.Zmoving = True
    def ZMinus(self):  self.z.cmd("vel {}", int(round(self.ZSpeed/self.z_step_size)) ); self.z.cmd("rel {}", -5000*self.z_ustep); self.Zmoving = True
    def ZStop(self):
        if self.Zmoving:
            self.z.cmd("rel 0")
            self.Zmoving = False

    def FZPlus(self):  self.fz.cmd("VEL 1 {}", self.FZSpeed); self.fz.cmd("MOV 1 30"); self.FZmoving = True
    def FZMinus(self): self.fz.cmd("VEL 1 {}", self.FZSpeed); self.fz.cmd("MOV 1 0"); self.FZmoving = True
    def FZStop(self):
        if self.FZmoving:
            self.fz.cmd("STP")
            self.FZmoving = False

    def AllStop(self):
        self.z.cmd("rel 0")
        self.xy.cmd("0 STP")
        #self.xy.cmd("0 EST") # emergency stop
        self.fz.cmd("STP")

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

    def xy_pos(self, s):
        m = re.match(f"#{num},{num}\n\r#{num},{num}", s)
        x, y = float(m[1])*1000, float(m[3])*1000
        self.ui.XPos.setText(f"{x:.3f} μm")
        self.ui.YPos.setText(f"{y:.3f} μm")

    def xy_err(self, s):
        if s:
            self.msgbox.setWindowTitle("XY Error")
            self.msgbox.setText(s)
            self.msgbox.show()

    def z_pos(self, s):
        m = re.match(r"pos ([+-]?\d+) target ([+-]?\d+) vel (\d+) lim1 ([01]) lim2 ([01])", s)
        z = int(m[1])*self.z_step_size
        lim = int(m[4]) or int(m[5])
        self.ui.ZPos.setText(f"{z:.1f} μm")
        setColor(self.ui.ZPos, QPalette.WindowText, Qt.red if lim else None)

    def fz_pos(self, s):
        m = re.match(f"1={num}", s)
        v = float(m[1])
        self.ui.PosAbs2.setText(f"{v} μm")
        self.ui.FZPos.setText(f"{v:.3f} μm")

    def fz_volt(self, s):
        m = re.match(f"2={num}", s)
        v = float(m[1])
        self.ui.PosRaw2.setText(f"{v} V")

    def fz_err(self, s):
        m = re.match(r"(\d+)", s)
        err = int(m[1])
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
        m = data.mean(axis=0)
        s = data.std(axis=0)
        self.ui.PosRaw.setText(f"{m[0]: .6f}\n±{s[0]:.6f} V")
        self.ui.LoadRaw.setText(f"{m[1]: .6f}\n±{s[1]:.6f} V")

        v = np.round((m+10)/20*1000)
        self.ui.PosBar.setValue(v[0])
        self.ui.LoadBar.setValue(v[1])
        self.ui.PosBar.setFormat(f"{m[0]: .1f} V")
        self.ui.LoadBar.setFormat(f"{m[1]: .1f} V")

        setColor(self.ui.LoadBar, QPalette.Highlight, Qt.darkGreen if self.load_lo < m[1] < self.load_hi else Qt.red)

        data[:,0] = self.position_calib(data[:,0])
        data[:,1] = self.load_calib(data[:,1])

        if self.fh:
            self.fh.write(data)

        m = data.mean(axis=0)
        s = data.std(axis=0)
        pos, load = m[0], m[1]

        self.ui.PosAbs.setText(f"{pos: .6f}\n±{s[0]:.6f} μm")
        self.ui.LoadAbs.setText(f"{load: .3f}\n±{s[1]:.3f} mN")

        self.last_pos = pos
        self.last_load = load

        pos -= self.zero_pos
        load -= self.zero_load
        if self.ui.Compression.isChecked():
            load *= -1
        else:
            pos *= -1


        self.ui.PosRel.setText(f"{pos: .6f} μm")
        self.ui.LoadRel.setText(f"{load: .3f} mN")

        self.ui.PosNorm.setText(f"{pos/self.Length: .6f} μm/μm")
        self.ui.LoadNorm.setText(f"{load/self.Area*1000: .3f} MPa")

        x = np.arange(len(data))
        self.monitor_lines[0].setData(x, data[:,0])
        self.monitor_lines[1].setData(x, data[:,1])

        self.history.update([pos], [load])
        x = np.array(self.history.x) * self.adc.N / self.adc.rate
        self.history_lines[0].setData(x, self.history.y1)
        self.history_lines[1].setData(x, self.history.y2)

        self.xy_lines[0].setData(self.history.y1, self.history.y2)
        self.xy_lines[1].setData(self.history.y1[-1:], self.history.y2[-1:])




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

        z.cmd("ustep {}", {1:0, 2:1, 8:3, 16:2}[md.z_ustep] )
        # 0 - 1 step
        # 1 - 1/2 step
        # 2 - 1/16 step
        # 3 - 1/8 step
        z.cmd("?").callback(print)

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
