# encoding: utf-8

import urllib.error
import urllib.request
from urllib.parse import urlparse

from bs4 import BeautifulSoup


def get_domain(url):
    parsed_uri = urlparse(url=url)
    return f'{parsed_uri.scheme}://{parsed_uri.netloc}/'


def get_page(url):
    """Scrapes a URL and returns the HTML source.

    Args:
        url (string): Fully qualified URL of a page.

    Returns:
        soup (string): HTML source of scraped page.
    """
    response = urllib.request.urlopen(url)
    return BeautifulSoup(response,
                         'html.parser',
                         from_encoding=response.info().get_param('charset'))


def get_og_title(soup):
    og_titles = soup.findAll("meta", property="og:title")
    return og_titles[0]["content"] if og_titles else None


def get_og_image_url(soup):
    og_urls = soup.findAll("meta", property="og:image")
    return og_urls[0]["content"] if og_urls else None

# TODO: url to binary image
def get_favicon(soup, domain):
    fallback_url = domain + '/favicon.ico'

    icon_link = soup.find("link", rel="shortcut icon")
    if icon_link is None:
        icon_link = soup.find("link", rel="icon")

    if icon_link is None:
        return fallback_url

    favicon_url = icon_link["href"]
    if 'http' not in favicon_url:
        return domain + favicon_url
    return favicon_url
