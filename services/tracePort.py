# tracePort.py is a serial port access abstraction
# GNU LESSER GENERAL PUBLIC LICENSE
# Copyright (C) 2020 Oleg Kokorin

import serial
import binascii


class tracePort():

    fHandle = None

    def open(self, name, speed, timeout=1):
        try:
            self.fHandle = serial.Serial(port=name, baudrate=int(speed),
                                         timeout=timeout)
        except serial.SerialException as e:
            print("serial exception:", e)
        except TypeError as e:
            print("type exception:", e)
        return

    def go(self):
        try:
            ser_bytes = self.fHandle.readline()
            # ncurses require decode into utf-8
            try:
                inp = ser_bytes.decode('utf-8')
                # inp = str(ser_bytes)
            except UnicodeDecodeError:
                # incoming data contain non-text chars
                inp = "HEX: "+str(binascii.b2a_hex(ser_bytes))
            return(inp)
            # return(ser_bytes)
        except Exception as e:
            print("exception:", e)
        return ("")
