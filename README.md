# article-django
Project Setup:

- git clone https://github.com/arjunshahi/article-django.git
- cd article-django
- create a new file `.env` inside basedir(sample: `.env.sample`)
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver 
