from setuptools import setup, find_packages

setup(
    name='ig-scraper',
    version='0.0.1',
    description='A simple Instagram post scraper',
    author='Andrew Chee',
    author_email='andrewcheewei@gmail.com',
    url='https://www.github.com/andrewcheewei/ig-scraper',
    scripts=['main.py'],
    packages=find_packages(),
    install_requires=[
        'requests_html',
        'instaloader',
        'lxml_html_clean',
        'bs4',
    ],
)