# -*- coding: utf-8 -*-

import datetime
import time
import logging
logger = logging.getLogger(__name__)


def get_time_stamp():
    return '%s%s' % (datetime.datetime.now().strftime('%Y%m%d%H%M%s'), time.clock())


def info(msg):
    print(msg)
    logger.info(msg)


def error(msg):
    print(msg)
    logger.error(msg)

