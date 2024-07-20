import requests 
import json
import getpass
from datetime import datetime
import time

def scraper():
    post_url = input('Enter post url: ')

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
        return False

    enc_password = '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(datetime.now().timestamp()), pwd)
    login_response = session.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', data={'enc_password': enc_password, 'username': user}, allow_redirects=True)
    response_json = login_response.json()

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