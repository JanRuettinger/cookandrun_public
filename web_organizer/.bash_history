ls
pwd
export FLASK_APP=/home/flask/wsgi.py
flask db upgrade
ls
flask recreate_db
flask populate_db
