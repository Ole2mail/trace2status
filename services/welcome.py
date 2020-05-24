# welcome.py is a user interactive services file
# GNU LESSER GENERAL PUBLIC LICENSE
# Copyright (C) 2020 Oleg Kokorin


keyLenght = "--key"
sortOrder = "--sort"
specialOptions = [keyLenght, sortOrder]

portName = "--port"
portSpeed = "--speed"
portBased = [portName, portSpeed]

fileName = "--file"
pauseDelay = "--delay"
fileBased = [fileName, pauseDelay]

helpLong = "--help"
helpShort = "-h"
helpNeeded = [helpLong, helpShort]
options = helpNeeded + portBased + fileBased + specialOptions
optArgs = portBased + fileBased + [keyLenght]


class welcome():

    # short help method
    def short(self):
        print("\n\
            welcome to trace2status application\n\
            \n\
            use following options:\n\
            \n\
            --help for advanced help on options\n\
            --port <port name> for serial port name\n\
            --speed <speed value> for serial port speed\n\
            --file <file name> for log file name\n\
            --delay <delay value> for time in seconds between trace messages\n\
            --key <key lenght> for message unique identification\n\
            --sort for messages to be sorted frequency based\n\
            ")

    def long(self):
        print("\n\
            for serial port based traces provide --port\
             and --speed arguments together\n\
            \n\
            port name example: /dev/ttyUSB1\n\
            speed example: 115200\n\
            \n\
            for file based trace simulation provide --file\
             and --delay arguments together\n\
            \n\
            file name example: /var/log/modemPortGPS.log\n\
            delay example (1 second pause between trace lines): 1\n\
            \n\
            some special settings are - key and sort\n\
            \n\
            key specify message prefix lenght used to\
             identify if message is unique\n\
            all messages will be converted to status \
            display items based on lenght of the key\n\
            sort specify if status items has to be sorted\
             based on display frequency\n\
            it will popup most frequently displayed status items on top\n\
            \n\
            warning: number of status items displayed depends on the\
             vertical line numbers\n\
            ")

    executionPathName = ""
    helpSuggested = False
    keyLengthAssigned = 3
    sortOrderRequested = False
    portNameAssigned = ""
    portSpeedAssigned = 0
    fileNameAssigned = ""
    pauseDelayAssigned = 0
    portBasedAction = False
    fileBasedAction = False

    def showSettings(self):
        print("")
        print("execPathFile", self.executionPathName)
        print(helpLong, self.helpSuggested)
        print(portName, self.portNameAssigned)
        print(portSpeed, self.portSpeedAssigned)
        print(fileName, self.fileNameAssigned)
        print(pauseDelay, self.pauseDelayAssigned)
        print("portBasedAction", self.portBasedAction)
        print("fileBasedAction", self.fileBasedAction)
        print(keyLenght, self.keyLengthAssigned)
        print(sortOrder, self.sortOrderRequested)
        print("")
        # end of settings display

    # command line arguments parser
    def parseCMD(self, argList=[], *args):

        portBasedAction = 0
        fileBasedAction = 0
        excludeArg = False

        for index, opt in enumerate(argList):

            # saving application execution path
            if index == 0:
                self.executionPathName = opt
                continue

            # excluding already consumed arg
            if excludeArg:
                excludeArg = False
                continue

            nextOpt = argList[(index+1)] if (index+1) < len(argList) else ""

            # return if help is requested
            if set([opt]).issubset(set(helpNeeded)):
                self.helpSuggested = True
                return

            # filtering only port based options
            if set([opt]).issubset(set(portBased)):
                portBasedAction += 1
                if fileBasedAction:
                    print(portBased, "options conflicts with", fileBased)
                    self.helpSuggested = True
                    return

            # filtering only file based options
            if set([opt]).issubset(set(fileBased)):
                fileBasedAction += 1
                if portBasedAction:
                    print(fileBased, "options conflicts with", portBased)
                    self.helpSuggested = True
                    return

            # retrieving all option required settings
            if set([nextOpt]).issubset(set(optArgs)) and len(nextOpt) == 0:
                print("option", opt, "is missing an argument")
                self.helpSuggested = True
                return

            if set([opt]).issubset(set([sortOrder])):
                self.sortOrderRequested = True
                excludeArg = False
            if set([opt]).issubset(set([portName])):
                self.portNameAssigned = nextOpt
                excludeArg = True
            if set([opt]).issubset(set([portSpeed])):
                self.portSpeedAssigned = nextOpt
                excludeArg = True
            if set([opt]).issubset(set([fileName])):
                self.fileNameAssigned = nextOpt
                excludeArg = True
            if set([opt]).issubset(set([pauseDelay])):
                self.pauseDelayAssigned = nextOpt
                excludeArg = True
            if set([opt]).issubset(set([keyLenght])):
                self.keyLengthAssigned = nextOpt
                excludeArg = True
            if portBasedAction:
                self.portBasedAction = True
            if fileBasedAction:
                self.fileBasedAction = True

        # end of command line arguments parsing
