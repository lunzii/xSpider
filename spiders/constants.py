# -*- coding: utf-8 -*-
from selenium.webdriver.chrome.options import Options as ChromeOptions

PATH_CHROME_DRIVER = '/usr/local/Cellar/chromedriver/2.20/bin/chromedriver'
PATH_PHANTOMJS_BIN = '/Users/olunx/Downloads/phantomjs-2.0.1-macosx/bin/phantomjs'

CHROME_OPTIONS = ChromeOptions()
CHROME_OPTIONS.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

PHANTOMJS_ARGS = ['--load-images=no']
