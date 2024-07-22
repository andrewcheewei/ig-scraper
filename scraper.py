#    ig-scraper - a simple instagram post scraper
#    Copyright (C) <2024>  <Andrew Chee>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import getpass
from datetime import datetime
import requests_html
from bs4 import BeautifulSoup
from instaloader import *
from urllib.parse import urlparse
import json

def validate_url() -> str:
    while True:
        post_url = input('Enter Instagram post url: ')
        s = requests_html.HTMLSession()
        page = s.get(post_url)
        page_text = BeautifulSoup(page.text, 'lxml')
        # invalid links do not contain a '|' in its scraped text
        if 'instagram.com/p/' not in post_url or '|' not in page_text.get_text():
            print("Invalid Instagram post url")
            continue 
        else:
            break 
    return post_url

def scrape():
    loader = instaloader.Instaloader()
    user = input('Enter username: ')
    pwd = getpass.getpass('Enter password: ')
    loader.login(user, pwd)
    
    # obtain post from url
    path = urlparse(validate_url()).path
    shortcode = path.lstrip('/p/').rstrip('/')
    post = Post.from_shortcode(loader.context, shortcode)

    comments = []
    for comment in post.get_comments():
        comments.append({
            'username': comment.owner.username,
            'text': comment.text
        })
    
    likes = []
    for like in post.get_likes():
        likes.append(like.username)

    data = {
        'shortcode': shortcode,
        'num_likes': post.likes,
        'likes': likes,
        'comments': comments
    }

    with open('post_data.json', 'w') as file:
        json.dump(data, file, indent=4)