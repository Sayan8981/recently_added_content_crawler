 
#!/bin/bash
pwd
echo  "\n"
echo  "The list of files \n"
echo  "\n"
ls
echo  "\n"
chmod +x create_db.py
echo  "\n"

python create_db.py
cd django_file_recent_content_crawler/
python manage.py makemigrations crawler_model
python manage.py migrate
cd ..
cd recent_content_crawler/recent_content_crawler/spiders/
pwd
echo "\n"
ls

#command to run spider 
echo "\n"
echo "spider running started..................."
scrapy crawl recently_added