import curses
from stf import *
import os


class Menu():
    def __init__(self, window, items):
        self.x = 0
        self.y = 0
        self.window = window
        self.items = items
        self.active_index = 0
        self.window.nodelay(1)
        self.window.keypad(1)


    def set_coords(self, x, y):
        self.x = x
        self.y = y
        return x, y


    def set_items(self, items):
        self.items = items
        self.render()


    def cycle(self, _dir):
        if _dir > 0:
            if self.active_index == len(self.items)-1:
                self.active_index = 0
            else:
                self.active_index += 1
        else:
            if self.active_index == 0:
                self.active_index = len(self.items)-1
            else:
                self.active_index -= 1
        self.render()

    def send_key(self, key):
        global running
        if key > 0:
            # down arrow or j
            if key == 258 or chr(key) == 'j':
                self.cycle(1)
            # up arrow or k
            if key == 259 or chr(key) == 'k':
                self.cycle(-1)
            # select enter or l
            if key == curses.KEY_ENTER or key == 10 or key == 13 or chr(key) == 'l':
                return self.active_index


    def render(self):
        y, x = self.window.getyx()
        rows, cols = self.window.getmaxyx()
        self.window.move(self.y,self.x)
        for item in self.items:
            if item == self.items[self.active_index]:
                item = pad(item, cols - 1, " ")
                self.window.addstr(' ' + item, curses.color_pair(1) + curses.A_BOLD)
            else:
                item = pad(item, cols - 1, " ")
                self.window.addstr(' ' + item)
        curses.panel.update_panels()
        curses.doupdate()
