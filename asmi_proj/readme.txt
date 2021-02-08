prvo otici u venv/Scripts i pokrenuti activate

python manage.py runserver 80

python manage.py startapp achievements
python manage.py makemigrations games - pravi migracije za modul 'games'
python manage.py migrate - okida migracije na bazu

Game.objects.filter()