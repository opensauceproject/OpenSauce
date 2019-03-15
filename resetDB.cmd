del db.sqlite3
python manage.py migrate
python manage.py loaddata opensauceapp\fixtures\SauceCategory.json
python manage.py loaddata opensauceapp\fixtures\ReportCategory.json
pause