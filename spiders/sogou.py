# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchAttributeException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.phantomjs.service import Service as PhantomJSService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import requests
import constants
import utils

# 公司链接
URL_SOGOU_WECHAT = 'http://weixin.sogou.com%s'


class SpiderArticle:

    # 是否保存
    save = False

    def __init__(self):
        utils.info('__init__')
        if constants.USE_CHROME_DRIVER:
            self.driver = webdriver.Chrome(executable_path=constants.PATH_CHROME_DRIVER,
                                           chrome_options=constants.CHROME_OPTIONS)
        else:
            self.driver = webdriver.PhantomJS(executable_path=constants.PATH_PHANTOMJS_BIN,
                                              service_args=constants.PHANTOMJS_ARGS)
        utils.info('--------------- 抓取数据开始 -----------------')

    # 爬取逻辑
    def crawl(self, wechat_id=None, save=False):
        self.save = save
        if not wechat_id:
            return
        path = '/weixin?type=1&query=%s&ie=utf8' % wechat_id
        self.driver.get(URL_SOGOU_WECHAT % path)

        # 第一个搜索结果
        class_account = '_item'
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_account))
            )
        except TimeoutException:
            return
        else:
            ele = self.driver.find_element_by_class_name(class_account)

            # 跳转页面
            href = ele.get_attribute('href')
            self.driver.get(URL_SOGOU_WECHAT % href)

            # 文章列表
            self.parse_item(wechat_id)
            utils.info('--------------- 抓取数据结束 -----------------')
            time.sleep(5)

    def close(self):
        self.driver.close()

    # 处理单项
    def parse_item(self, wechat_id):
        # 文章列表
        class_article = 'wx-rb3'
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_article))
            )
        except TimeoutException:
            return
        else:
            ele_items = self.driver.find_elements_by_class_name(class_article)
            articles = []
            for ele in ele_items:
                item = {}
                try:
                    title = ele.find_element_by_xpath('div[2]/h4/a')
                    link = title.get_attribute('href')
                    desc = ele.find_element_by_xpath('div[2]/p')
                    publish = ele.find_element_by_xpath('div[2]/div')
                    item['wechat_id'] = wechat_id
                    item['title'] = title.text
                    item['link'] = link
                    item['desc'] = desc.text
                    item['publish'] = publish.text
                except NoSuchElementException, e:
                    utils.error(e.message)
                except NoSuchAttributeException, e:
                    utils.error(e.message)
                except Exception, e:
                    utils.error(e.message)
                utils.info(item)
                articles.append(item)
            self.parse_link(articles)

    def parse_link(self, items):
        for item in items:
            link = item['link']
            self.driver.get(link)
            url = self.driver.current_url
            item['url'] = url
            self.save_item(item)
            time.sleep(5)

    def save_item(self, item):
        if self.save:
            import database
            database.save_wx_gzh_article(item)
        else:
            utils.info('do not save')


# 入口
if __name__ == '__main__':
    # spider = SpiderCompany()
    # spider.crawl()
    spider = SpiderArticle()
    spider.crawl(wechat_id='mofczb')
    spider.close()
