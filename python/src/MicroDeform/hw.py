#!/usr/bin/env python3

import logging
import threading
import queue
import time

from contextlib import contextmanager

import serial
from serial.tools.list_ports import comports

import concurrent.futures
class Future(concurrent.futures.Future):
    def callback(self, fn):
        self.add_done_callback( lambda f: fn(f.result()) )

import re
num = r"([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)"

class DummySerial:
    def write(self, data):
        pass

    def read_until(self, sep):
        return b""


class Device:
    linesep = "\n"
    args = (0,)
    kwargs = {}
    timeout = 0.1
    wait = 0

    def __init__(self, dummy=False):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.run)
        
        self.info = self.logger.info

        self.dummy = dummy
        if dummy:
            self.device = f"DUMMY_{self.__class__.__name__}"
        else:
            self.device = next( info.device for info in sorted(comports()) if (info.vid, info.pid) == self.usb_id )

    @contextmanager
    def open(self):
        self.info("open %s", self.device)
        if self.dummy:
            yield DummySerial()
        else: 
            with serial.Serial(self.device, *self.args, **self.kwargs, timeout=self.timeout) as ser:
                time.sleep(self.wait)
                yield ser

    def run(self):
        with self.open() as ser:
            while True:
                cmd, read, future = self.queue.get()
                if cmd == "STOP":
                    self.info("STOP")
                    break

                if not future.set_running_or_notify_cancel():
                    continue

                out = (cmd + self.linesep).encode()
                self.info("-> %s", out)
                ser.write(out)
                
                if read:
                    result = ser.read_until(self.linesep)
                    self.info("<- %s", result)
                    result = result.decode()
                else:
                    result = None
                
                future.set_result(result)

    def cmd(self, cmd, *args, read=None):
        cmd = cmd.format(*args)
        if read is None:
            read = "?" in cmd
        future = Future()
        self.queue.put( (cmd, read, future) )
        return future

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.queue.put( ("STOP", None, None) )
        self.thread.join()


class XY(Device):
    usb_id = (0x0403, 0x6015)
    args = (38400, 8, 'N', 1)
    linesep = "\n\r"

    def __exit__(self, *args):
        self.cmd("0 MOT", 0)
        super().__exit__(*args)

    def stop(self, ax):
        self.cmd("{} STP", ax)

    def move(sefl, ax, vel, dst): # relative
        self.cmd("{} VEL {}", ax, vel/1000)
        self.cmd("{} REL {}", ax, dst/1000)

    def pos(self, cb):
        def f(s):
            m = re.match(f"#{num},{num}\n\r#{num},{num}", s)
            cb( float(m[1])*1000, float(m[3])*1000 )

        self.cmd("0 POS?").callback((lambda s: f("#11.111111,0.0\n\r#12.222222,0.0")) if self.dummy else f)

    def err(self, cb):
        self.cmd("0 ERR?").callback(cb)


class Piezo(Device):
    usb_id = (0x0403, 0x6010)
    args = (460800, 8, 'N', 1)
    kwargs = dict(rtscts=True)

    def stop(self):
        self.cmd("STP")

    def move(self, vel, dst): # absolute
        self.cmd("VEL 1 {}", vel)
        self.cmd("MOV 1 {}", dst)

    def pos(self, cb):
        def f(s):
            m = re.match(f"1={num}", s)
            cb( float(m[1]) )

        self.cmd("POS?").callback((lambda s: f("1=14.444444")) if self.dummy else f)

    def volt(self, cb):
        def f(s):
            m = re.match(f"2={num}", s)
            cb( float(m[1]) )

        self.cmd("VOL? 2").callback((lambda s: f("2=9.999999")) if self.dummy else f)


    def err(self, cb):
        def f(s):
            m = re.match(r"(\d+)", s)
            cb( int(m[1]) )

        self.cmd("ERR?").callback((lambda s: f("0")) if self.dummy else f)




class Z(Device):
    usb_id = (0x2341, 0x003d)
    args = (115200, 8, 'N', 1)
    wait = 0.3

    # 0 - 1 step
    # 1 - 1/2 step
    # 2 - 1/16 step
    # 3 - 1/8 step
    ustep_table = [1, 2, 16, 8]
    ustep_setting = 2
    ustep = ustep_table[ustep_setting]
    step_size = 2.5/ustep

    def __enter__(self):
        super().__enter__()
        self.cmd("?").callback(print)
        self.cmd("ustep {}", self.ustep_setting)
        return self

    def stop(self):
        self.cmd("rel 0")

    def move(self, vel, dst): # relative
        self.cmd("vel {}", int(round(vel/self.step_size)))
        self.cmd("rel {}", int(round(dst/self.step_size)))

    def pos(self, cb):
        def f(s):
            m = re.match(r"pos ([+-]?\d+) target ([+-]?\d+) vel (\d+) lim1 ([01]) lim2 ([01])", s)
            z = int(m[1])*self.step_size
            lim = int(m[4]) or int(m[5])
            cb(z, lim)

        self.cmd("?").callback((lambda s: f("pos 85333 target 85333 vel 500 lim1 1 lim2 0")) if self.dummy else f)


import numpy as np
pos = 0
class ADC(Device):
    usb_id = (0x2341, 0x003e)
    timeout = None

    def __init__(self, callback=None, N=2048, dummy=False):
        super().__init__(dummy)
        self.rate = 20000
        self.N = N
        self.callback = callback

    def run(self):
        with self.open() as ser:
            while True:
                try:
                    cmd, read, future  = self.queue.get_nowait()
                except queue.Empty:
                    cmd = None

                if cmd == "STOP":
                    self.info("STOP")
                    break

                if self.dummy:
                    global pos
                    time.sleep(self.N/20000)
                    x = np.arange(pos, pos+self.N)*2*np.pi/200000
                    pos += self.N
                    data = 10 * np.transpose([ np.sin(x), np.cos(x), -np.sin(x), -np.cos(x) ]) + np.random.normal(0, 0.1, size=(self.N, 4))
                else:
                    data = ser.read(self.N*4*4)
                    data = np.frombuffer(data, dtype=np.int32).reshape(self.N, 4)*10/0x1ffff

                self.info("-> data")

                if self.callback:
                    self.callback(data)

                if cmd == "data?" and future.set_running_or_notify_cancel():
                    future.set_result(data)


if __name__ == "__main__":
#    Device.dummy = True

    logging.basicConfig(level=logging.INFO)
    if 1:
        with Z() as z:
            print( z.cmd("?").result() )

    if 1:
        with XY() as xy:
            print( xy.cmd("0 VER?").result() )
            print( xy.cmd("0 ERR?").result() )
            print( xy.cmd("0 MOT?").result() )
            print( xy.cmd("0 REZ?").result() )

            print( xy.cmd("0 AMX?").result() )
            print( xy.cmd("0 ACC?").result() )
            print( xy.cmd("0 DEC?").result() )
            print( xy.cmd("0 JAC?").result() )

            print( xy.cmd("0 VMX?").result() )
            print( xy.cmd("0 VEL?").result() )

    if 0:
        with ADC(print) as adc:
            time.sleep(1)
    
    if 0:
        with Piezo() as piezo:
            print( piezo.cmd("*IDN?").result() )
            #piezo.cmd("SVO 1 1")
            #piezo.cmd("MVR 1 0.01")
            print( piezo.cmd("ERR?").result() )
           
            #print( piezo.cmd("ACC?").result() )
            #print( piezo.cmd("VEL?").result() )
            #print( piezo.cmd("MOV?").result() )
            #print( piezo.cmd("ONT?").result() )
            #print( piezo.cmd("POS?").result() )
            print( piezo.cmd("SVO?").result() )
            #print( piezo.cmd("TAD?").result() )
            print("="*10) 
            print( piezo.cmd("TMN?").result() )
            print( piezo.cmd("TMX?").result() )
            print("Range Limit min:", piezo.cmd("SPA? 1 0x07000000").result() )
            print("Range Limit max:", piezo.cmd("SPA? 1 0x07000001").result() )
            print("="*10) 
            print( piezo.cmd("SPA? 2 0x0a000003").result() ) # 2 = "current position of axis"
            print( piezo.cmd("SPA? 2 0x0a000004").result() ) # 1 = output axis 
            print("Position Report Scaling:", piezo.cmd("SPA? 1 0x07001005").result() )
            print("Position Report Offset:", piezo.cmd("SPA? 1 0x07001006").result() )
            print("="*10) 

            #print( piezo.cmd("SPA? 1 0x07000500").result() )
            #print( piezo.cmd("SPA? 1 0x07000501").result() )

            #print( piezo.cmd("SPA? 2 0x0a000010").result() )
            #print( piezo.cmd("SPA? 2 0x0a000020").result() )

            print("pos:", piezo.cmd("POS?").result() )
            print("vol:", piezo.cmd("VOL? 2").result() )

