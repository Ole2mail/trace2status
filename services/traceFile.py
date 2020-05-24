# traceFile.py is a file access abstraction
# GNU LESSER GENERAL PUBLIC LICENSE
# Copyright (C) 2020 Oleg Kokorin

import time
# import binascii


class traceFile():

    fHandle = None
    delay = None

    def open(self, name, delay=1):
        self.delay = float(delay)
        self.fHandle = open(name, "r", errors='replace')
        return

    def go(self):
        time.sleep(self.delay)
        try:
            ser_bytes = self.fHandle.readline()
            inp = str(ser_bytes)
            return(inp)
            # return(ser_bytes)
        except Exception as e:
            print("readline exception:", e)
        return ("")
