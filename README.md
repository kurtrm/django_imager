[![Build Status](https://travis-ci.org/kurtrm/django_imager.svg?branch=front-end-4)](https://travis-ci.org/kurtrm/django_imager)
[![Coverage Status](https://coveralls.io/repos/github/kurtrm/django_imager/badge.svg?branch=front-end-4)](https://coveralls.io/github/kurtrm/django_imager?branch=front-end-4)

## Django Imager
An image-sharing app built on Django.

## Collaborators
Kurt Maurer
Morgan Nomura


## Local installation
- Create a virtual environment
- Pip install Django, ipython, factory boy, psycopg2
- Create a database
- Add the following environmental variables:
    - SECRET_KEY (set to some string)
    - DATABASE_NAME (set to the name of the database you created)
    - DATABASE_HOST='127.0.0.1'
    - DEBUG='True'
- from the imagersite directory, run: ```./manage.py migrate```

## Serve locally
In the terminal, enter: 
```./manage.py runserver```

## Tests
In the terminal in the Django project directory, enter:
```./manage.py test```

## License
MIT


## Attribution
- Thank you to Ely Paysinger and Carlos Cadena for their assistance with file uploads from the client.
- Additional thanks to Ely Paysinger for assistance on connecting email functionality and his constant willingness to help out with bugs not of his own making.
