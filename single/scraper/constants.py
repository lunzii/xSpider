# -*- coding: utf-8 -*-
from selenium.webdriver.chrome.options import Options as ChromeOptions

# 本地测试路径
PATH_CHROME_DRIVER = '/usr/local/Cellar/chromedriver/2.20/bin/chromedriver'
PATH_PHANTOMJS_BIN = '/Users/olunx/Downloads/phantomjs-2.0.1-macosx/bin/phantomjs'

# 服务器路径
# PATH_PHANTOMJS_BIN = '存放phantomjs的路径'

CHROME_OPTIONS = ChromeOptions()
CHROME_OPTIONS.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

PHANTOMJS_ARGS = ['--load-images=no']

# 是否使用ChromeDriver否则使用Phantomjs
USE_CHROME_DRIVER = True