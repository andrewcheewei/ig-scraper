from scraper import *

session = login()
validate_url()
# add session as param
scrape(session)