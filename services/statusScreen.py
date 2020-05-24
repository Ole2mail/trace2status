# statusScreen.py is a terminal screen/window output abstraction
# GNU LESSER GENERAL PUBLIC LICENSE
# Copyright (C) 2020 Oleg Kokorin

import curses


class statusScreen():

    screen = None
    currentColor = 1
    pairColorInverted = 1
    pairColorNormal = 2
    currentX = 0
    maxX = 1
    statusWindow = None
    scrollWindow = None

    def open(self):

        self.screen = curses.initscr()

        # color definition section
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(self.pairColorInverted, curses.COLOR_RED,
                         curses.COLOR_WHITE)
        curses.init_pair(self.pairColorNormal, curses.COLOR_WHITE,
                         curses.COLOR_RED)

        rows, cols = self.screen.getmaxyx()
        self.maxX = rows

        try:
            # self.scrollWindow = curses.newwin(0, 0, rows - 1, cols // 2)
            self.scrollWindow = curses.newpad(rows - 1, cols // 2)
            # Return a new window, whose left-upper corner is at
            # (begin_y, begin_x), and whose height/width is nlines/ncols.
            # curses.newwin(nlines, ncols, begin_y, begin_x)
            self.statusWindow = curses.newwin(rows, cols // 2, 0,
                                              cols // 2 + 1)
        except Exception as e:
            print("window creation e:", e)

        # regular log window require scrolling capability
        self.scrollWindow.scrollok(True)

        print("Screen initialized.")
        # self.screen.refresh()

    def test(self):

        # Update the buffer, adding text at different locations
        self.scrollWindow.addstr("test")

        # Changes go in to the screen buffer and only get
        # displayed after calling `refresh()` to update
        # self.screen.refresh()
        rows, cols = self.screen.getmaxyx()
        self.scrollWindow.refresh(0, 0, 0, 0, rows - 1, cols // 2)

        self.statusWindow.addstr(0, 0, "test", curses.color_pair(1))
        self.statusWindow.addstr(0, cols // 2 - len("test"), "test",
                                 curses.color_pair(1))

        # self.screen.refresh()
        self.statusWindow.refresh()
        curses.napms(3000)

    def show(self, msg, x=0, y=0):
        try:
            self.statusWindow.addstr(self.currentX, y, msg,
                                     curses.color_pair(
                                        (self.currentColor % 2) + 1))
            # self.screen.addstr(self.currentX, y, msg)
        except Exception as e:
            print("screen addstr failed:", e)
        self.screen.refresh()
        self.currentColor += 1
        self.currentX += 1
        rows, cols = self.screen.getmaxyx()
        if self.currentX > rows-2:
            self.currentX = 1

    def showLocated(self, msg, x, color):

        rows, cols = self.screen.getmaxyx()
        self.scrollWindow.addstr(msg)
        self.scrollWindow.refresh(0, 0, 0, 0, rows - 1, cols // 2)

        if x > rows - 2:
            x = rows - 2
        try:
            self.statusWindow.addstr(x, 0, msg, curses.color_pair(color))
        except Exception as e:
            print("screen addstr failed:", e, "at row:", x)

        self.statusWindow.refresh()
        # self.screen.refresh()

    # static method terminal cleanup on exit
    def close():
        curses.endwin()
