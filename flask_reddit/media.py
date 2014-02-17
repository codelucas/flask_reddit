# -*- coding: utf-8 -*-
"""
All code for scraping images and videos from posted
links go in this file.
"""
import BeautifulSoup
import requests
from urlparse import urlparse, urlunparse, urljoin

img_extensions = ['jpg', 'jpeg', 'gif', 'png', 'bmp']

def make_abs(url, img_src):
    domain = urlparse(url).netloc
    scheme = urlparse(url).scheme
    baseurl = scheme + '://' + domain
    return urljoin(baseurl, img_src)

def clean_url(url):
    frag = urlparse(url)
    frag = frag._replace(query='', fragment='')
    return urlunparse(frag)

def get_top_img(url, timeout=4):
    """
    Nothing fancy here, we merely check if the page author
    set a designated image or if the url itself is an image.

    This method could be mutch better but we are favoring ease
    of installation and simplicity of speed.
    """
    if not url:
        return None

    url = clean_url(url)

    # if the url is referencing an img itself, return it
    if url.split('.')[-1].lower() in img_extensions:
        return url
    try:
        html = requests.get(url, timeout=timeout).text
        soup = BeautifulSoup.BeautifulSoup(html)

        og_image = (soup.find('meta', property='og:image') or
                    soup.find('meta', attrs={'name': 'og:image'}))

        if og_image and og_image['content']:
            src_url = og_image['content']
            return make_abs(url, src_url)

        # <link rel="image_src" href="http://...">
        thumbnail_spec = soup.find('link', rel='image_src')
        if thumbnail_spec and thumbnail_spec['href']:
            src_url = thumbnail_spec['href']
            return make_abs(url, src_url)

    except Exception, e:
        print 'FAILED WHILE EXTRACTING THREAD IMG', str(e)
        return None

    return None
