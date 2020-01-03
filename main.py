#!/bin/python3
from requests import get, RequestException
from contextlib import closing
from bs4 import BeautifulSoup as soup
import inquirer
import os


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
    print
    """
    print(e)

def get_query():
    inp = input("Enter search term: ")
    inp = inp.replace(" ", "%20")
    return inp


if __name__ == "__main__":
    query = get_query()
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

    # Prompt to choose torrent
    print('Choose a torrent to download')
    questions = [
            inquirer.List('title',
                '==> ',
                [show['title'] for show in shows],
                carousel=True
                )
            ]

    title = inquirer.prompt(questions)['title']
    link = list(filter(lambda show: show['title'] == title, shows))[0]['link']
    raw_html = simple_get(f'https://katcr.to/{link}')
    html = soup(raw_html, 'html.parser')
    link = html.find('a', attrs={
        'class': 'kaGiantButton',
        'title': 'Magnet link'
    }).get('href')
    os.system(f'xdg-open {link}')
