import curses


class Form():
    global render
    def __init__(self, x, y, height, width):
        self.win = curses.newwin(height, width, y, x)
        self.panel = curses.panel.new_panel(self.win)
        self.height = height
        self.width = width
        self.widgets = list()
        self.active_widget = None
        self.win.keypad(1)


    def add_widget(self, wid, x, y):
        if x < 0:
            x = self.width+x
        if y < 0:
            y = self.height+y
        self.widgets.append(wid)
        self.widgets[len(self.widgets)-1].set_coords(x, y)
        self.update()


    def set_active_widget(self, index):
        self.active_widget = index
        return self.active_widget


    def update(self):
        self.widgets[self.active_widget].render()


    def listen(self):
        curses.noecho()
        key = self.win.getch()
        if key > 0:
            return key, self.widgets[self.active_widget].send_key(key)
        return key, None
        #  self.update()

    def set_title(self, title, char=u'\u2500'):
        rows, cols = self.win.getmaxyx()
        self.win.move(1, 0)
        self.win.addstr(char)
        self.win.addstr(title)
        for _ in range(1, cols-len(title)):
            self.win.addstr(char)
        self.win.addstr('\n')


    def render(self):
        for widget in self.widgets:
            widget.render()
