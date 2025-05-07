# Django Project Tutorial

## Installation

1. Create a Python Virtual Environment (venv) and activate it. For Linux/macOS:
```bash
python3 -m venv env

source env/bin/activate
```

2. Install necessary pip packages
```bash
pip install django djangorestframework django-cors-headers faker numpy
```
OR
```bash
pip install -r requirements.txt
```
Django Cors Headers is a middleware and faker is a lib that we will use to generate mock data to test out our endpoints. Numpy will also be used to help generate random data within certain distributions.

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

### Overwriting standard ViewSet methods

The `ModelViewSet` provides default implementations for standard operations. You can override methods to customize behavior. Here's a mapping of HTTP methods to `ModelViewSet` methods:

| HTTP Method | Method Name        | Description                   |
| ----------- | ------------------ | ----------------------------- |
| GET         | `list()`           | Returns a list of objects     |
| GET         | `retrieve()`       | Returns a single object by ID |
| POST        | `create()`         | Creates a new object          |
| PUT         | `update()`         | Updates an object entirely    |
| PATCH       | `partial_update()` | Partially updates an object   |
| DELETE      | `destroy()`        | Deletes an object             |

Example:

```python
class ModelNameViewSet(viewsets.ModelViewSet):
    queryset = ModelName.objects.all()
    serializer_class = ModelNameSerializer

    def list(self, request):
        # Custom logic before default behavior
        response = super().list()
        # Modify response if needed
        return response
```

### Adding custom endpoints

Use `@action` or `@api_view` decorators to define custom routes.

* Inside a ViewSet:

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class ModelNameViewSet(viewsets.ModelViewSet):
    ...

    @action(detail=True, methods=['get'])
    def custom_action(self, request):
        params = request.query_params
        objs = self.queryset.all()
        result = do_custom_logic(objs, params)
        return Response({'result': result})
```

* Standalone view:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def custom_view(request):
    return Response({"message": "Hello from custom view"})
```

Then register it in `urls.py`:

```python
urlpatterns += [
    path('custom-view/', custom_view),
]
```

### Raising custom errors or sending custom responses

When handling errors or specific conditions, you can either raise exceptions using DRF's exceptions module or send a custom response with a specific status code.

#### Using DRF's exceptions module

DRF provides built-in exceptions to handle errors gracefully:

```python
from rest_framework.exceptions import ValidationError, NotFound

if invalid_condition:
    raise ValidationError("This input is not valid")

if not object:
    raise NotFound("Item not found")
```

#### Sending a response with a custom status code

Alternatively, you can return a custom response with a specific HTTP status code:

```python
from rest_framework.response import Response
from rest_framework import status

if invalid_condition:
    return Response({"error": "This input is not valid"}, status=status.HTTP_400_BAD_REQUEST)
    # or simply status=400

if not object:
    return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
    # or simply status=404
```

Both approaches can be used depending on the context and desired behavior.

### Personalize `serializers.py`

Serializers in Django REST Framework serve two main purposes:
1. **Validation**: They validate incoming request data against defined rules
2. **Transformation**: They convert complex data types (like Django models) into Python native types that can be easily converted to JSON/XML

#### Customizing ModelSerializer

The default `ModelSerializer` can be customized by overriding its methods.

```python
from rest_framework import serializers
from .models import ModelName

class ModelNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelName
        fields = ['id', 'first_name', 'last_name', 'full_name']
    
    # Customize how data is returned
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add additional data or modify existing
        data['created_at'] = instance.created_at.strftime('%Y-%m-%d')
        return data
    
    # Customize how data is validated
    def validate(self, data):
        if data['first_name'] == data['last_name']:
            raise serializers.ValidationError("First name cannot be the same as last name")
        return data
    
    # Customize how objects are created
    def create(self, validated_data):
        # Add custom logic before creation
        instance = super().create(validated_data)
        # Add custom logic after creation
        return instance
```

#### Creating Custom Serializers

Sometimes you need a serializer that doesn't map directly to a model. This is useful for:
- Complex data validation
- Nested data structures
- Custom API responses

```python
from rest_framework import serializers

class CustomDataSerializer(serializers.Serializer):
    # Define fields manually
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField(min_value=0, max_value=120)
    email = serializers.EmailField()
    
    # Nested serializer
    address = serializers.DictField(
        child=serializers.CharField()
    )
```

This custom serializer can be used in views to validate incoming data or format outgoing responses, even when there's no corresponding model.

## Test your API

Testing your API is crucial to ensure it works as expected and to catch any issues before deploying to production. There are several ways to test your API endpoints:

### With browser

The simplest way to test your API is through your web browser. Django REST Framework provides a browsable API interface that you can access by opening your browser and navigating to your API endpoints:
- All models: http://localhost:8000/api/
- Specific endpoints: http://localhost:8000/api/model-name/

The browsable API interface allows you to:
- See the JSON response
- Test POST, PUT, PATCH, and DELETE methods through a form interface
- View available endpoints

### With Postman or Thunder Client

For more advanced testing, you can use API clients like Postman or Thunder Client (VS Code extension). These tools provide more features and better control over your requests:

1. **GET requests** (List all records):
```
GET http://localhost:8000/api/model-name/
```

2. **GET requests** (Get specific record):
```
GET http://localhost:8000/api/model-name/1/
```

3. **POST requests** (Create new record):
```
POST http://localhost:8000/api/model-name/
Content-Type: application/json

{
    "field1": "value1",
    "field2": "value2"
}
```

4. **PUT/PATCH requests** (Update record):
```
PUT http://localhost:8000/api/model-name/1/
Content-Type: application/json

{
    "field1": "new_value"
}
```

5. **DELETE requests** (Remove record):
```
DELETE http://localhost:8000/api/model-name/1/
```

These clients also allow you to:
- Save requests for later use
- Create collections of related requests
- Set up environment variables
- View detailed response headers and status codes

### Sending Parameters in Requests

There are three main ways to send parameters in API requests:

1. **Query Parameters** (in URL):
```
GET http://localhost:8000/api/model-name/?search=test&page=2
```
In Django view:
```python
def list(self, request):
    search = request.query_params.get('search')
    page = request.query_params.get('page')
```

2. **Path Parameters** (in URL path):
```
GET http://localhost:8000/api/model-name/123/
```
In Django view:
```python
def retrieve(self, request, pk=None):
    # pk will be 123
    instance = self.queryset.get(pk=pk)
```

3. **JSON Body** (in request body):
```
POST http://localhost:8000/api/model-name/
Content-Type: application/json

{
    "name": "test",
    "age": 25
}
```
In Django view:
```python
def create(self, request):
    name = request.data.get('name')
    age = request.data.get('age')
```

In Thunder Client:
- Query Parameters: Add them in the "Query" tab
- Path Parameters: Include them directly in the URL
- JSON Body: Add them in the "Body" tab, select "JSON" format