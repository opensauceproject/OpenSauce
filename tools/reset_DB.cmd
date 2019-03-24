cd ..
del db.sqlite3
python manage.py migrate
python manage.py loaddata opensauceapp\fixtures\SauceCategory.json
python manage.py loaddata opensauceapp\fixtures\ReportCategory.json
python manage.py loaddata opensauceapp\fixtures\Sauce.json
python manage.py createsuperuser --username admin --email admin@opensauce.ch
