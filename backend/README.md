# Django Project Tutorial

## Installation

1. Create a Python Virtual Environment (venv) and activate it. For Linux/macOS:
```bash
python3 -m venv env

source env/bin/activate
```

2. Install necessary pip packages
```bash
pip install django djangorestframework django-cors-headers faker
```
OR
```bash
pip install -r requirements.txt
```
Django Cors Headers is a middleware and faker is a lib that we will use to generate mock data to test out our endpoints.

## Run start-up commands

```bash
django-admin startproject mwd .

python manage.py migrate

python manage.py runserver
```

An example web page should appear in http://localhost:8000/ if everything was succesfully installed.

## Create your app and adjust settings

```bash
django-admin startapp api
```

Another common names for apps are `app` and `core`, besides from `api`.

Now, move to `settings.py` and add the following changes:
```python
INSTALLED_APPS = [
    ...,
    ...,
    'corsheaders',
    'rest_framework',
    'api',
]
```
```python
MIDDLEWARE = [
    ...,
    ...,
    'corsheaders.middleware.CorsMiddleware',
]
```
And define this new constant:
```python
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'https://localhost:3000',
)
```
If Cors throws any errors later when accessing the API via front-end, also consider editing this:
```python
ALLOWED_HOSTS = ['*']
```

## Create a superuser
Run the following command and follow the instructions to define username and password:
```bash
python manage.py createsuperuser
```
Now, access admin page in http://localhost:8000/admin/.

## Create your first model

Go to `models.py` and create a model, based on the previously defined mock-up and the application requirements.

```python
class ModelName(models.Model):
    char_field_example = models.CharField(max_length=100)
    integer_field_example = models.IntegerField()

    def __str__(self):
        return self.char_field_example
```

Magic method `__str__` is useful to visualize information in Django Admin, but is optional.

At this point, there is a local database in your repository called `db.sqlite3`. To effectively apply the changes in models.py and be able to see the new registered table using a database administrator (e.g., DBeaver), you need to run the following commands:

```bash
python manage.py makemigrations

python manage.py migrate
```
```makemigrations``` is used to register changes in database structure (tables and columns), and ```migrate``` effectively apply these changes in your local database. All migrations should be commited when working on a real project!

Now, if you open your local database, you'll already see the new created table. But to use it on our application, we need to add changes in `admin.py`, `serializers.py`, `views.py` and `urls.py`.

Here is a summary (and maybe an over-simplication, but enough for now) of each file's funcionality:
- admin --> register the model to be available in the admin page, so the superuser is allowed to see, edit, remove and add records to the table;
- serializers --> it is used by the API (in views) and defines how the information is transported (serialized) from the back-end to the front-end;
- views --> defines each endpoint of our API and how the data is handled (which calculations are applied);
- urls --> defines specifically by which url each endpoint will be accessed by the client.

`admin.py`:
```python
from .models import (
    ModelName,
    ModelName2,
    ...,
)

admin.site.register(ModelName)
admin.site.register(ModelName2)
admin.site.register(...)
```

```serializers.py```. It needs to be created inside app folder (`api`, in our case):

```python
from rest_framework import serializers
from .models import (
    ModelName,
    ModelName2,
    ...,
)

class ModelNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelName
        fields = '__all__'
```

`views.py`:
```python
from django.shortcuts import render
from rest_framework import viewsets

from .serializers import (
    ModelNameSerializer,
    ...,
)

from .models import (
    ModelName,
    ...,
)

class ModelNameViewSet(viewsets.ModelViewSet):
    queryset = ModelName.objects.all()
    serializer_class = ModelNameSerializer
```

By defining the ModelViewSet like this, all CRUD functionalities are automatically implemented via the request types (POST, GET, DELETE, PUT and PATCH).

`urls.py` (this one is inside `backend` folder):
```python
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import (
    ModelNameViewSet,
    ...,
)

router = routers.DefaultRouter()
router.register(r'model-name', ModelNameViewSet)
...

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
```

Now you are already able to test your API via browser, front-end or clients as Postman or Thunder Client. Just run ```python manage.py runserver``` and access the defined URLs.

Move forward and repeat this process to define the rest of the necessary models (tables) of the database.

## Personalize your API

With the current implementation, one is already able to develop the application. In this case, it would be necessary to apply the filters and calculat the metrics in React (front-end).

However, if you want to improve your skills in Django, it is possible to perform part of the calculations in the back-end and load the data to the client already transformed.

This can be useful to optimize future projects by two main ways:
1. Decreasing the number of requests:
- A personalized endpoint can handle multiple tables at once, therefore eliminating the need to GET request every table.
2. Increasing performance:
- Django Queryset ORMs perform the calculations in SQL, which is way more performative than JavaScript or Python. Also, you don't need to serialize all your data to then apply the calculations.

This is specially helpful when dealing with slow server connections or huge amounts of data. It is also an option if the developer feels more comfortable with Python than JavaScript.