DIR=$(pwd)
cd ..
python manage.py dumpdata opensauceapp.Sauce > $DIR/sauces.json
cd $DIR
python remove_pk.py sauces.json