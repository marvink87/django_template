# django_template
Personal template for Django

## Features

- Custom user model
- Seperate settings for production and development

## How to Use

To use this project, follow these steps:

1. Create your working environment.
2. Install Django (`$ pipenv install django`)
3. Create a new project using this template

Create a new Django project:

    $ django-admin startproject --template https://github.com/marvink87/django_template/archive/master.zip new_project_name


### Settings ###

Settings are divided by environments: production.py, development.py By default it uses development.py, if you want to change the environment set a environment variable:

    export DJANGO_SETTINGS_MODULE="my_project.settings.production"

or you can use the `settings` param with runserver:

    pipenv run python manage.py runserver --settings=my_project.settings.production
