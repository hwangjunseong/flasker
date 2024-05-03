import requests
from bs4 import BeautifulSoup

# url = "https://comic.naver.com/webtoon/weekday"
# response = requests.get(url)
# response.raise_for_status()

# soup = BeautifulSoup(response.text, "lxml")
# title = soup.title
# # print(soup)
# print(title)
# print(type(soup))


response = requests.get('https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=%EC%A3%BC%EC%8B%9D')
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
announcements = []
links = soup.select(".news_tit")
for link in links:
    title = link.text
    url = link.attrs['href']
    #img = soup.find('a', class_='dsc_thumb')
    content = soup.find('a', class_='api_txt_lines dsc_txt_wrap').text
    # announcements.append({'title': title, 'url': url, 'img': img, 'content': content})
    announcements.append({'title': title, 'url': url, 'content': content})



for  ann in announcements:
    print(ann['title'])
    print(ann['url'])
    print(ann['img'])
    print(ann['content'])
    print('--------------------------------')
    #print(ann.title)
    #print(ann.url)
    #print(ann.content)
    #print(ann.img)