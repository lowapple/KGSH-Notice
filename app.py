# -*- coding: utf-8 -*-

import facebook
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from PIL import Image
from config import Config
import sys

class Log:
    def setLog(self, str):
        f = open('./log/notification.txt', 'w')
        f.write(str)
        f.close()

    def getLog(self):
        f = open('./log/notification.txt', 'r+')
        str = f.readline()
        f.close()
        return str


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

        driver = webdriver.PhantomJS('./bin/linux/phantomjs')

        # 페이지 가져오기
        soup = self.get_page(url=base_url + notice_list_url)

        # 최상단 요소 가져오
        element = soup.select("#Con > div.boardnew2011 > div.table")
        element_item = element[0].find_all('tr')[1]

        # print(element_item)

        notice_url = element_item.find('a')['href']
        next_title = element_item.find('a')['title']

        facebook_message = next_title

        print(next_title)

        # 이전 값과 비교하기
        prev_title = log.getLog()
        if prev_title != next_title:
            print('new post')

            # 값 세팅
            log.setLog(next_title)

            # 글 작성하기
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
            callback(facebook_message)
        else:
            print('old post')

def put_facebook(message):
    graph = facebook.GraphAPI(
        access_token=config.getAccessToken())
    graph.put_photo(image=open('./img/cap.png', 'rb'), message=message)


config = Config()
log = Log()
scrap = ScrapKgsh()

scrap.start(put_facebook)
