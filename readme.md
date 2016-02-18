# 启动Celery进程
python manage.py celery worker --loglevel=info

lsof -i -n -P | grep 8000

# 初始化项目

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 执行Scrapy爬虫
scrapy crawl code_control_spider -a id=1 -a do_action=yes

