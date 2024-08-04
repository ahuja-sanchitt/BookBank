
# API Creation Guide

## Introduction

This guide will walk you through creating API endpoints in this project.

## Table of Contents

1. [Setting Up Django](#setting-up-django)
2. [Defining Models](#defining-models)
3. [Creating Serializers](#creating-serializers)
4. [Defining Views](#defining-views)
5. [URL Routing](#url-routing)
6. [CRUD Operations](#crud-operations)
7. [Authentication](#authentication)
8. [Data Validation](#data-validation)
9. [Best Practices](#best-practices)

## Setting Up Django

### What is Django?

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It’s free and open-source, with a large community and robust documentation.

### Steps to Set Up Django

1. **Install Django and Django REST Framework:**

   ```bash
   pip install django djangorestframework
   ```

2. **Create a new Django project:**

   ```bash
   django-admin startproject book_project
   cd book_project
   ```

3. **Create a new Django app:**

   ```bash
   python manage.py startapp books
   ```

4. **Add the app and REST framework to `INSTALLED_APPS` in `settings.py`:**

   ```python
   INSTALLED_APPS = [
       ...
       'rest_framework',
       'books',
   ]
   ```

5. **Configure DB settings in `settings.py`:**
   ```python
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'your_database_host',  
        'PORT': 'your_database_port', 
    }
    }   
   ```


## Defining Models

### What are Models?

Models are a single, definitive source of information about your data. They contain the essential fields and behaviors of the data you’re storing. Django follows the DRY (Don't Repeat Yourself) principle, making it easier to maintain the code.

### Steps to Define Models

1. **Create models for your book-related functionalities in `books/models.py`:**

   ```python
   from django.db import models

   class Book(models.Model):
       title = models.CharField(max_length=200)
       author = models.CharField(max_length=200)
       published_date = models.DateField()
       isbn = models.CharField(max_length=13, unique=True)
       page_count = models.IntegerField()
       cover_url = models.URLField()
       language = models.CharField(max_length=2)

       def __str__(self):
           return self.title
   ```

2. **Run migrations to create the database schema:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Creating Serializers

### What are Serializers?

Serializers in Django REST Framework are used to convert complex data types, such as querysets and model instances, into native Python data types that can then be easily rendered into JSON, XML, or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after validating the incoming data.

### Steps to Create Serializers

1. **Create serializers for your models in `books/serializers.py`:**

   ```python
   from rest_framework import serializers
   from .models import Book

   class BookSerializer(serializers.ModelSerializer):
       class Meta:
           model = Book
           fields = '__all__'
   ```

## Defining Views

### What are Views?

Views in Django are used to encapsulate the logic responsible for processing a user’s request and returning a response. In Django REST Framework, views handle the data processing and representation.

### Steps to Define Views

1. **Create views for your API endpoints in `books/views.py`:**

   ```python
   from rest_framework import status
   from rest_framework.decorators import api_view
   from rest_framework.response import Response
   from .models import Book
   from .serializers import BookSerializer

   @api_view(['GET'])
   def book_list(request):
       if request.method == 'GET':
           books = Book.objects.all()
           serializer = BookSerializer(books, many=True)
           return Response(serializer.data)

    ```       

## URL Routing

### What is URL Routing?

URL routing in Django is the mechanism through which requests are mapped to the appropriate view based on the URL. This involves defining URL patterns that correspond to different views.

### Steps to Define URL Routing

1. **Define URL routing for your API in `books/urls.py`:**

   ```python
   from django.urls import path
    from .views import book_list, book_detail

    urlpatterns = [
    path('books/', book_list, name='book-list'),    
    ]
   ```

2. **Include the app's URLs in the project’s `urls.py`:**

   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('api/', include('books.urls')),
   ]
   ```


## CRUD Operations with Function-Based Views in Django REST Framework

Views in Django REST Framework (DRF) allow you to perform CRUD operations using different HTTP methods. Here's a basic overview of how each operation is handled

### List
Use the `@api_view` decorator with the `GET` method to return a list of objects.
Use the @api_view decorator with the `POST` method to create a new object.
Use the @api_view decorator with the `PUT` method to update an existing object
Use the @api_view decorator with the `DELETE` method to delete an object

## Authentication

### What is Authentication?

Authentication is the process of verifying the identity of a user. In Django REST Framework, this is typically done using authentication classes that handle different authentication methods.

### Steps to Implement Authentication

1. **Add authentication classes to `settings.py`**:

   ```python
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.BasicAuthentication',
           'rest_framework.authentication.SessionAuthentication',
       ],
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
   }
   ```

2. **Add permission classes decorator on each view**:

   ```python
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def list_objects(request):
    objects = YourModel.objects.all()
    serializer = YourModelSerializer(objects, many=True)
    return Response(serializer.data
   ```

## Data Validation

### What is Data Validation?

Data validation is the process of ensuring that the data provided by a user meets the required standards before it is processed. This can include checking data types, lengths, formats, and more.

### Steps to Add Data Validation

1. **Add custom validation to serializers**:

   ```python
   from rest_framework import serializers
   from .models import Book

   class BookSerializer(serializers.ModelSerializer):
       class Meta:
           model = Book
           fields = '__all__'

       def validate_isbn(self, value):
           if not value.isdigit() or len(value) != 13:
               raise serializers.ValidationError("ISBN must be a 13 digit number.")
           return value
   ```

## Best Practices

- **Use meaningful names** for your models, serializers, and views.
- **Keep your code DRY** (Don't Repeat Yourself) by using mixins and generic views where applicable.
- **Write tests** for your API endpoints to ensure they work as expected.
- **Use version control** to manage your codebase and collaborate with other developers.
- **Document your API** using tools like Swagger or Django REST framework's built-in documentation.


