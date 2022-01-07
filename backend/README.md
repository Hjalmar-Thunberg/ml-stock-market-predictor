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

**Run on local Kubernetes cluster**
Install minikube
Linux:   `sudo apt/yum install kubectl`
Mac:     `brew install kubectl`
Windows: `choco install kubectl`

Install minikube
Linux:   `sudo apt/yum install minikube`
Mac:     `brew install minikube`
Windows: `choco install minikube`

Apply your docker environment variable exports to configure your local environment to re-use the Docker daemon inside the Minikube instance.
`eval $(minikube docker-env)`

Start minikube.
`minikube start`

Start the image as a pod within kubernetes cluster.
`kubectl run stock-market-pred --image=karrdo/stock-market-pred`

It may take a while, please be patient as the cluster will pull the image from dockerHub and build it inside the cluster.