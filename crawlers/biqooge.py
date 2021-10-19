import requests
from bs4 import BeautifulSoup
# from crawler import models


root_url = r"https://www.biqooge.com/"
start = 1
headers = {
    'cookie': 'UM_distinctid=17c970c2406f4-0e56a3c095df7c-b7a1438-1fa400-17c970c240799b; '
              'jieqiVisitId=article_articleviews=1|3306|33063; '
              'CNZZDATA1278827600=1764292142-1634611857-https%3A%2F%2Fwww.baidu.com%2F|1634622657',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'referer': 'https://www.biqooge.com/wanben/1_1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/94.0.4606.81 Safari/537.36',
    }


def get_content(content_url: str) -> str:
    resp = requests.get(url=content_url, headers=headers)
    soup = BeautifulSoup(resp.content, features='html.parser')
    content = soup.select('div#content')[0].text
    return content


def get_chapters(book_id: int, current_chapter: int, chapter_count: int):
    # todo
    url_chapters = root_url + '0_' + str(book_id) + r'/'
    response = requests.get(url_chapters, headers=headers)
    content = response.content
    # print(content[:256])
    soup = BeautifulSoup(content, features="html.parser")
    begin = 8 + current_chapter
    end = 8 + current_chapter + chapter_count
    # print(soup.prettify())
    # author = soup.select('#maininfo>#info>h1')[0].text.strip()
    # intro = soup.select('#maininfo>#intro>p')[0].text.strip()
    # print(author, intro)

    # chapters = soup.select('.box_con>#list>dl>dd')[9:]
    chapters = soup.select('.box_con>#list>dl>dd')[begin:end]
    return chapters

    # for chapter in chapters:
    #     chapter_name = chapter.a.text.strip()
    #     url1 = chapter.a['href']
    #     url = root_url + url1
    #     content = get_content(content_url=url)


def get_a_chapter(book_id: int):
    url_chapters = root_url + '0_' + str(book_id) + r'/'
    response = requests.get(url_chapters, headers=headers)
    content = response.content
    soup = BeautifulSoup(content, features="html.parser")

    book_name = soup.select('#maininfo>#info>h1')[0].text.strip()
    author = soup.select('#maininfo>#info>p')[0].text.strip().split('：')[1]
    digest = soup.select('#maininfo>#intro>p')[0].text.strip()
    # print(author, intro)

    return book_name, author, digest


