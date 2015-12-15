# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchAttributeException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.phantomjs.service import Service as PhantomJSService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import constants
import utils


# 公司链接
URL_LAGOU_COMPANY = 'http://www.lagou.com/gongsi/'
URL_LAGOU_JOB = 'http://www.lagou.com/gongsi/j%s.html'


class SpiderCompany:

    # 是否保存
    save = False

    def __init__(self):
        utils.info('__init__')
        self.driver = webdriver.Chrome(executable_path=constants.PATH_CHROME_DRIVER,
                                       chrome_options=constants.CHROME_OPTIONS)
        # self.driver = webdriver.PhantomJS(executable_path=constants.PATH_PHANTOMJS_BIN,
        #                                   service_args=constants.PHANTOMJS_ARGS)
        utils.info('--------------- 抓取数据开始 -----------------')

    # 爬取逻辑
    def crawl(self, save=False):
        self.save = save
        self.driver.get(URL_LAGOU_COMPANY)
        self.parse_item()
        while self.parse_next():
            utils.info('---------------进入下一页,等待5秒-----------------')
            time.sleep(5)
            self.parse_item()
        utils.info('--------------- 抓取数据结束 -----------------')

    def close(self):
        self.driver.close()

    # 下一页
    def parse_next(self):
        next_page = '//*[@id="company_list"]/div/div/span[text()="%s"]' % u'下一页'
        ele_next_page = self.driver.find_element_by_xpath(next_page)
        result = False
        if 'pager_next_disabled' not in ele_next_page.get_attribute('class'):
            result = True
            ele_next_page.click()
        return result

    # 处理单项
    def parse_item(self):
        ele_items = self.driver.find_elements_by_xpath('//*[@id="company_list"]/ul/li')
        for ele in ele_items:
            company_title = ele.find_element_by_xpath('dl/dd/h3/a')
            company_desc = ele.find_element_by_xpath('dl/p')
            company_type = ele.find_element_by_xpath('div/span[1]')
            company_step = ele.find_element_by_xpath('div/span[3]')
            company_city = ele.find_element_by_xpath('div/span[2]')
            interview = ele.find_element_by_xpath('dl/dd/div/p[1]/a')
            job = ele.find_element_by_xpath('dl/dd/div/p[2]/a')
            resume = ele.find_element_by_xpath('dl/dd/div/p[3]/a')

            item = {}
            try:
                item['company_name'] = company_title.get_attribute('title')
                item['company_id'] = company_title.get_attribute('data-lg-tj-cid')
                item['company_desc'] = company_desc.text
                item['company_type'] = company_type.text
                item['company_step'] = company_step.text
                item['company_city'] = company_city.text
                item['interview_count'] = interview.find_element_by_tag_name('span').text
                item['job_count'] = job.find_element_by_tag_name('span').text
                item['resume_rate'] = resume.find_element_by_tag_name('span').text
                item['created_id'] = utils.get_time_stamp()
            except NoSuchElementException, e:
                utils.error(e.message)
            except NoSuchAttributeException, e:
                utils.error(e.message)
            except Exception, e:
                utils.error(e.message)
            utils.info(item)
            self.save_item(item)

    def save_item(self, item):
        if self.save:
            import database
            database.save_lagou_company(item)
        else:
            utils.info('do not save')


class SpiderJob:

    # 是否保存
    save = False

    def __init__(self):
        utils.info('__init__')
        self.driver = webdriver.Chrome(executable_path=constants.PATH_CHROME_DRIVER,
                                       chrome_options=constants.CHROME_OPTIONS)
        # self.driver = webdriver.PhantomJS(executable_path=constants.PATH_PHANTOMJS_BIN,
        #                                   service_args=constants.PHANTOMJS_ARGS)
        utils.info('--------------- 抓取数据开始 -----------------')

    # 爬取逻辑
    def crawl(self, save=False, company_id=None, _id=None):
        self.save = save
        if not company_id:
            return
        self.driver.get(URL_LAGOU_JOB % company_id)
        self.parse_item(company_id=company_id, _id=_id)
        while self.parse_next():
            utils.info('---------------进入下一页,等待3秒-----------------')
            time.sleep(3)
            self.parse_item(company_id=company_id, _id=_id)
        utils.info('--------------- 抓取数据结束 -----------------')

    def close(self):
        self.driver.close()

    # 下一页
    def parse_next(self):
        next_page = '//*[@id="containerCompanyPositionLists"]/div/div/div[2]/div/span[text()="%s"]' % u'下一页'
        result = False
        try:
            ele_next_page = self.driver.find_element_by_xpath(next_page)
            if 'pager_next_disabled' not in ele_next_page.get_attribute('class'):
                result = True
                ele_next_page.click()
        except NoSuchElementException, e:
            utils.error(e.message)
        return result

    # 处理单项
    def parse_item(self, company_id=None, _id=None):
        ele_items = self.driver.find_elements_by_xpath('//*[@id="containerCompanyPositionLists"]/div/div/ul/li')
        for ele in ele_items:
            company_financing = ele.find_element_by_xpath('//*[@id="company_basic_info"]/div[1]/ul/li[2]/span')
            company_employee = ele.find_element_by_xpath('//*[@id="company_basic_info"]/div[1]/ul/li[3]/span')
            company_name = ele.get_attribute('data-company')
            job_id = ele.get_attribute('data-positionid')
            job_salary = ele.get_attribute('data-salary')
            job_name = ele.find_element_by_xpath('p[1]/a')
            job_desc = ele.find_element_by_xpath('p[2]/span[2]')
            job_publish_date = ele.find_element_by_xpath('p[1]/span')

            item = {}
            try:
                item['_id'] = _id
                item['company_id'] = company_id
                item['company_financing'] = company_financing.text
                item['company_employee'] = company_employee.text
                item['company_name'] = company_name
                item['job_id'] = job_id
                item['job_salary'] = job_salary
                item['job_name'] = job_name.text
                item['job_desc'] = job_desc.text
                item['job_publish_date'] = job_publish_date.text
                item['created_id'] = utils.get_time_stamp()
            except NoSuchElementException, e:
                utils.error(e.message)
            except NoSuchAttributeException, e:
                utils.error(e.message)
            except Exception, e:
                utils.error(e.message)
            utils.info(item)
            self.save_item(item)

    def save_item(self, item):
        if self.save:
            import database
            database.save_lagou_job(item)
        else:
            utils.info('do not save')

# 入口
if __name__ == '__main__':
    # spider = SpiderCompany()
    # spider.crawl()
    spider = SpiderJob()
    spider.crawl(company_id='11209')
    spider.crawl(company_id='89131')
    spider.crawl(company_id='86283')
    spider.close()
