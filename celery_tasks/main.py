# -*- coding: utf-8 -*-
import os
from celery import Celery

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'huluobei.settings'

celery_app = Celery('huluobei')
# 配置
celery_app.config_from_object('celery_tasks.config')
# 注册
celery_app.autodiscover_tasks(['celery_tasks.crawl'])
