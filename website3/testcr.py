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


#response = requests.get('https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=%EC%A3%BC%EC%8B%9D')
category_url = 'https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=%EC%A3%BC%EC%8B%9D'
response = requests.get(category_url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
announcements = []

news_articles = soup.select('ul.list_news._infinite_list > li.bx')

for article in news_articles:

    title = article.select_one('a.news_tit').text
    url = article.select_one('a.news_tit')['href']
    content = article.select_one('a.api_txt_lines.dsc_txt_wrap').text
    pic = article.select_one('a.dsc_thumb img')
    img_url = pic['data-lazysrc']
    #if pic:
    #    img_url = pic['src']
    #else:
    #    img_url = None
    #img_url = img_element['src'] if img_element else None
    announcements.append({'title': title, 'url': url, 'content': content, 'img_url': img_url, 'pic': pic})
    #announcements.append({'title': title, 'url': url, 'content': content})


#  image_url = "https://search.pstatic.net/common/?src=https%3A%2F%2Fimgnews.pstatic.net%2Fimage%2Forigin%2F009%2F2024%2F05%2F10%2F5301298.jpg&type=f200_200&expire=2&refresh=true"

#     # 이미지 다운로드
#     response = requests.get(image_url)
#     if response.status_code == 200:
#         # 이미지를 저장할 디렉토리
#         image_dir = 'images'
#         if not os.path.exists(image_dir):
#             os.makedirs(image_dir)

#         # 이미지 파일명 생성
#         filename = os.path.join(image_dir, 'image.jpg')

#         # 이미지를 파일로 저장
#         with open(filename, 'wb') as f:
#             f.write(response.content)

#         # 이미지 정보를 데이터베이스에 저장
#         new_image = Image(filename=filename)
#         db.session.add(new_image)
#         db.session.commit()

for  ann in announcements:
    print(ann['title'])
    print(ann['url'])
    print(ann['img_url'])
    print(ann['content'])
    print(1)
    print(ann['pic'])
    print('--------------------------------')
    #print(ann.title)
    #print(ann.url)
    #print(ann.content)
    #print(ann.img)