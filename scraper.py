import requests 
import getpass
from datetime import datetime
import requests 
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
        print(page_text.get_text())
        # invalid public links do not contain a '|' in its scraped text
        if 'instagram.com/p/' not in post_url or '|' not in page_text.get_text():
            print("Invalid Instagram post url")
            continue 
        else:
            break 
    return post_url

def login():
    user = input('Enter username: ')
    pwd = input('Enter password: ')
    credential = {'username': user, 'password': pwd}
    
    session = requests.Session()
    session.headers.update({'Referer': 'https://www.instagram.com/'})
    request = session.get('https://www.instagram.com/')

    csrf_token = session.cookies.get_dict()['csrftoken']
    session.headers.update({'X-CSRFToken': csrf_token})
    if not csrf_token:
        print("CSRF token not found")
        exit()

    enc_password = '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(datetime.now().timestamp()), pwd)
    login_response = session.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', data={'enc_password': enc_password, 'username': user}, allow_redirects=True)
    response_json = login_response.json()
    print(response_json)

    if response_json['authenticated']:
        print("Success!")
    if not response_json['authenticated']:
        if response_json['user']:
            print('Incorrect password')
        else:
            print('Username does not exist')
    if response_json['status'] == 'fail':
        print(response_json['message'])
        exit()   
        
    return session

def scrape(session):
    loader = instaloader.Instaloader()

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