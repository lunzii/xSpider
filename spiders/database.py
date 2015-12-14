# -*- coding: utf-8 -*-
from app.models import LagouCompany
from app.models import LagouJob


def save_lagou_company(args):
    item = LagouCompany(**args)
    item.save()


def save_lagou_job(args):
    item = LagouJob(**args)
    item.save()

