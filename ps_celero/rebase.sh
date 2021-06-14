rm api/migrations/0*.py;
rm api/migrations/__pycache__ -rf;
rm db.sqlite3;
python manage.py makemigrations;
python manage.py migrate;