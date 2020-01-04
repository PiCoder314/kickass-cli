from requests import get, RequestException
from contextlib import closing
from bs4 import BeautifulSoup as soup
import curses
import curses.panel
from widgets import menu, form, cmd_line
from stf import *
import os

ROWS = COLS = None
stdscr = None
running = True
MODE = 0
MENU = 0
CMD = 1


def init_screen():
    global ROWS, COLS, stdscr
    stdscr = curses.initscr()
    ROWS, COLS = stdscr.getmaxyx()
    curses.cbreak()


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)



def quit():
    global running
    running = False
    stdscr.clear()
    title_window.clear()
    space.win.clear()
    curses.curs_set(1)
    curses.endwin()



def mainloop():
    global stdscr, ROWS, COLS, MODE
    while running:
        stdscr.clear()
        curses.noecho()
        curses.curs_set(0)
        key, response = space.listen()
        if key < 0:
            continue

        # Menu Mode
        if MODE == MENU:
            if key == ord('q'):
                quit()
            elif key == ord('/'):
                space.set_active_widget(1)
                MODE = CMD
                curses.curs_set(1)
            elif (key == curses.KEY_ENTER or key == 10 or key == 13):
                link = shows[response]['link']
                raw_html = simple_get(f'https://katcr.to/{link}')
                html = soup(raw_html, 'html.parser')
                link = html.find('a', attrs={
                    'class': 'kaGiantButton',
                    'title': 'Magnet link'
                }).get('href')
                os.system(f"xdg-open '{link}'")

        # Command Mode
        if MODE == CMD:
            if key == 27:
                MODE = MENU
                curses.curs_set(0)
                space.set_active_widget(0)
            elif (key == curses.KEY_ENTER or key == 10 or key == 13):
                query = response
                shows = get_torrents(query)
                MODE = MENU
                curses.curs_set(0)
                space.set_active_widget(0)


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    print error
    """
    print(e)


def get_torrents(query):
    raw_html = simple_get(f'https://katcr.to/usearch/{query}/')
    html = soup(raw_html, 'html.parser')
    links = html.find_all('a', attrs={
        'class': 'cellMainLink'
    })
    shows = []
    for i, a in enumerate(links):
        shows.append({})
        shows[i]['title'] = a.text.replace('\n', '').strip()
        shows[i]['link'] = a.get('href')
    space.widgets[MENU].set_items([show['title'] for show in shows])
    return shows

if __name__ == "__main__":
    init_screen()
    init_colors()
    title_window = curses.newwin(0, COLS, 0, 0)
    title_window.addstr("""katcr.to\n""", curses.color_pair(2))
    for _ in range(title_window.getmaxyx()[1]):
        title_window.addstr(u'\u2500')
    title_panel = curses.panel.new_panel(title_window)
    space = form.Form(0, 2, ROWS-2, COLS)
    space.set_active_widget(0)
    space.set_title("Movies")
    main_menu = menu.Menu(space.win, ["Press q to quit", "Press / to search a movie", "Press j and k to navigate", "More features coming soon"])
    space.add_widget(main_menu, 0, 1)
    cmdline = cmd_line.CommandLine(space.win)
    space.add_widget(cmdline, 0, -2)
    mainloop()
