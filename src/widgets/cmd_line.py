import curses
from stf import *
import os


class CommandLine():
    def __init__(self, window):
        self.x = 0
        self.y = 0
        self.window = window
        self.cmd_string = ""
        self.active_index = 0
        self.window.nodelay(1)
        self.window.keypad(1)


    def set_coords(self, x, y):
        self.x = x
        self.y = y
        return x, y


    def clear(self):
        self.cmd_string = ""
        for i in range(self.window.getmaxyx()[1]):
            self.cmd_string += " "
        self.render()
        self.cmd_string = ""


    def send_key(self, key):
        if key == 27:
            self.clear()
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            cmd = self.cmd_string
            self.clear()
            return cmd
        elif key == 127:
            self.cmd_string = self.cmd_string[:-1]
            self.render()
        else:
            self.cmd_string += chr(key)
            self.render()


    def render(self):
        self.window.move(self.y,self.x)
        rows, cols = self.window.getmaxyx()
        txt = pad(self.cmd_string, cols-1, ' ')
        self.window.addstr(f"/{txt}")
        curses.panel.update_panels()
        curses.doupdate()
