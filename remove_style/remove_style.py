import sys
import requests
from bs4 import BeautifulSoup

url = sys.argv
if len(url) != 2:
    print('Incorrect number of arguments. Enter an URL as an argument')
    sys.exit(1)
print('Parsing the data...')
page = ''
try:
    page = requests.get(str(url[1]))
except requests.exceptions.RequestException as e:
    print('Incorrect URL. Please, try again')
    sys.exit(1)
soup = BeautifulSoup(page.content, 'html.parser')
for tag in soup.find_all():
    del tag['style']
print(soup.prettify())