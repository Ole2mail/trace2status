# actual trace to status application start file
# GNU LESSER GENERAL PUBLIC LICENSE
# Copyright (C) 2020 Oleg Kokorin

import sys
import signal

from services.welcome import welcome
from services.traceFile import traceFile
from services.tracePort import tracePort
from services.statusScreen import statusScreen
from services.messageGather import messageGather

usingNCURSES = True


def signal_handler(signal, frame):
    if usingNCURSES:
        statusScreen.close()
    print("\nprogram exiting on CTRL+C")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    hello = welcome()

    if len(sys.argv) < 2:
        hello.short()
    else:
        hello.parseCMD(sys.argv)
        if hello.helpSuggested:
            hello.short()
            hello.long()
            sys.exit(0)

    # temporary settinds indication
    hello.showSettings()

    if hello.fileBasedAction:
        trace = traceFile()
        trace.open(hello.fileNameAssigned, hello.pauseDelayAssigned)

    if hello.portBasedAction:
        trace = tracePort()
        trace.open(hello.portNameAssigned, hello.portSpeedAssigned)

    if usingNCURSES:
        status = statusScreen()
        status.open()
        # status.test()

    placer = messageGather()
    placer.init(status.maxX, int(hello.keyLengthAssigned),
                hello.sortOrderRequested)

    try:
        while True:
            msg = trace.go()
            count, x, color = placer.locate(msg)
            if usingNCURSES:
                status.showLocated(msg, x, color)
            else:
                print(msg)
    except KeyboardInterrupt:
        pass

    if usingNCURSES:
        statusScreen.close()
    sys.exit(0)


if __name__ == '__main__':
    main()
