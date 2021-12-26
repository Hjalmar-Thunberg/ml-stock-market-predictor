**Requirements**

- Pandas
- Pipenv
- Django
- Django-admin

**How to setup:**
1. cd to ./api in your terminal
2. `pip3 install pipenv`
3. `pipenv shell`
4. `pipenv install`
5. `py|python manage.py makemigrations`
6. `py|python manage.py migrate`
> 'py' for Windows, 'python' for Mac/Linux

**How to run:**
`python manage.py runserver [PORT NUMBER]`

Port number is optional, it would default to port 8000 if you don't specify.

**Build and run docker image**
`docker build --tag python-django .`
`docker run --publish 8000:8000 python-django`
