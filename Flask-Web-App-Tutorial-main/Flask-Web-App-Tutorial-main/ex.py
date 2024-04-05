from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://news.naver.com/")

bsObject = BeautifulSoup(html, "html.parser")
print(type(bsObject))
#for link in bsObject.find_all('a'):
#print(link.text.strip(), link.get('href'))

#for link in bsObject.find_all('img'):
   # print(link.text.strip(), link.get('src'))