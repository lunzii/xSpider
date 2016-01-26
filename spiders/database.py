# -*- coding: utf-8 -*-
from app.models import LagouCompany
from app.models import LagouJob
from app.models import WxGzhArticle
import utils


# 拉勾公司
def save_lagou_company(args):
    item = LagouCompany(**args)
    item.save()


# 拉勾职位
def save_lagou_job(args):
    _id = args['_id']
    try:
        company = LagouCompany.objects.get(id=_id)
    except LagouCompany.DoesNotExist, e:
        utils.error(e.message)
    else:
        company.company_employee = args['company_employee']
        company.company_financing = args['company_financing']
        del args['_id']
        del args['company_employee']
        del args['company_financing']
        company.save()
        item = LagouJob(**args)
        item.save()


# 公众号文章
def save_wx_gzh_article(args):
    item = WxGzhArticle(**args)
    item.save()
