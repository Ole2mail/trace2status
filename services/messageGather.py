# tracePort.py is a repeated messages gatherer abstraction
# GNU LESSER GENERAL PUBLIC LICENSE
# Copyright (C) 2020 Oleg Kokorin


class messageGather():

    # is a <key> : <various messages> template
    repeatable = {}
    # the key is in use for quantity/position/color assignment
    placed = {}
    # the lenght of the status message key
    keyLength = None
    # apply number of calls sorting based
    sorting = False
    # max elements fit for status window
    maxElements = 1

    statQuantOffset = 0
    statPosOffset = 1
    statColOffset = 2

    def init(self, maxElements=1, keyLength=3, sorting=False):
        # print("creating gathering storages")
        self.keyLength = keyLength
        self.sorting = sorting
        self.maxElements = maxElements

    def nextViable(self):
        if len(self.placed) == 0:
            return 0
        nextX = 0
        for each in self.placed:
            position = self.placed[each]
            if position[self.statPosOffset] >= nextX:
                nextX = position[self.statPosOffset] + 1
        return nextX

    def sortUp(self, popupCandidate):
        # for each in reversed(self.placed):
        for each in self.placed:
            # print("popup:", popupCandidate, "each:", each)
            if each == popupCandidate:
                continue
            testingElement = self.placed[each]
            popupElement = self.placed[popupCandidate]
            if testingElement[self.statQuantOffset] == 1:
                testingElement[self.statPosOffset], \
                    popupElement[self.statPosOffset] = \
                    popupElement[self.statPosOffset], \
                    testingElement[self.statPosOffset]
                break

    def locate(self, msg):
        foundPlace = None

        msg = msg.strip('\n')
        msg = msg.strip('\r')

        # key lenght based search pattern discovery synthes
        pattern = msg[:self.keyLength]

        # pattern based message comparison and location discovery
        if foundPlace is None:
            for each in self.repeatable:
                if pattern == each:
                    try:
                        foundPlace = self.placed[each]
                        # sorting and swapping indicators
                        if self.sorting and \
                                len(self.placed) > self.maxElements:
                            self.sortUp(each)
                        # increasing call counter
                        foundPlace[self.statQuantOffset] += 1
                        # flip/flopping color indication
                        foundPlace[self.statColOffset] = \
                            foundPlace[self.statColOffset] % 2 + 1
                    except:
                        nextX = self.nextViable()
                        self.placed[pattern] = [1, nextX, 1]
                        foundPlace = self.placed[pattern]

                    self.repeatable[each].append(msg) if msg not in \
                        self.repeatable[each] else self.repeatable[each]

        if foundPlace is None:
            # first time message appeared in the log
            self.repeatable[pattern] = [msg]
            nextX = self.nextViable()
            self.placed[pattern] = [1, nextX, 1]
            foundPlace = self.placed[pattern]

        # print("complete placed:", self.placed)
        return foundPlace
