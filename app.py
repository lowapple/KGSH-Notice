import facebook
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from PIL import Image


class ScrapKgsh:
    def get_page(self, url):
        # URL Load
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urlopen(req)
        res = res.read()
        html = res.decode('utf-8')

        return BeautifulSoup(html, 'html.parser')

    def start(self, callback):
        # 게임고 공지 홈페이지
        base_url = "http://www.game.hs.kr/2013/"
        notice_list_url = "inner.php?sMenu=G1000"

        driver = webdriver.PhantomJS('./bin/mac/phantomjs')

        # 페이지 가져오기
        soup = self.get_page(url=base_url + notice_list_url)

        # 최상단 요소 가져오
        element = soup.select("#Con > div.boardnew2011 > div.table")
        element_item = element[0].find_all('tr')[1]

        notice_url = ''
        notice_url = element_item.find('a')['href']

        driver.get(base_url + notice_url)

        form_location = driver.find_element_by_id('form_view').location
        form_size = driver.find_element_by_id('form_view').size

        driver.execute_script('document.body.style.background = "white"')
        driver.save_screenshot('./img/cap.png')
        driver.quit()

        left = form_location['x'] - 35
        top = form_location['y'] + 50
        right = left + form_size['width'] + 65
        bottom = top + form_size['height'] - 70

        cap_image = Image.open('./img/cap.png')
        cap_image = cap_image.crop((left, top, right, bottom))
        cap_image.save('./img/cap.png')

        # callback
        callback()


def put_facebook():
    graph = facebook.GraphAPI(
        access_token='EAAEIWZAUv1WkBANiK6EPDgf0Au5ovhWiXTDNJFXbW5vDBcSc6FrTQh58ZBVqZBVuecPjYbp4ZCiZABqhS0Atpa9lWsYiR99pGt8fT7iio2uZBhAEEuQtFPxZAmq64nywmHrRDGZAqpWu1zd366yEHMDyMoZAQSt50mEdEmV1l9t4It69aJGkTt1F7SoCjniGiubInKaES8ZBpA4gZDZD')
    # graph.put_object("525880264415772", "feed", message='테스트')
    graph.put_photo(image=open('./img/cap.png', 'rb'), message='공지')


scrap = ScrapKgsh()
scrap.start(put_facebook)
