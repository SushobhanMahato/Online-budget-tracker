### Run in local 

Step by step precedures to get the project running in development mode:

```bash
cd budget_tracker

#make sure to create a virtual environment
venv\Scripts\activate 

pip3 install -r requirements.txt 

python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic #optional

python manage.py runserver 8080

#go to http://127.0.0.1:8080/
