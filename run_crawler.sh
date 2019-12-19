 
#!/bin/bash
sudo apt-get install python-pip
sudo pip install scrapy
sudo pip install django
pwd
echo  "\n"
echo  "The list of files \n"
echo  "\n"
ls

dt=$(date '+%d/%m/%Y %H:%M:%S')
echo $dt

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
scrapy crawl recently_added > output_log.txt

sleep 15m

echo "\n"
echo "Preparing to create csv file from database..............."

python db_output.py

sleep 10s

cd ../

path="$(pwd)/recently_added_content_crawler/attachments"
python zip.py
mv *.zip $path

cd $path

echo "Executed................$dt"