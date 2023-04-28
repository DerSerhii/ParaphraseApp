# PARAPHRASE TEST

This project is made as part of a test task. It implements an API that takes data 
as a syntax tree of English text and returns its paraphrased versions. This is done
using the [Django](https://www.djangoproject.com/) framework.

### Getting started
Download the code base on your local machine. You may prefer to use virtual environment 
to separate the project's dependencies from other packages you have installed.

To install dependencies use `pip` or [poetry](https://python-poetry.org/):
```
pip install -r requirements.txt
```
```
poetry install
```

After downloading the project, set the required environment variables. 
Refer the table in *Environment variables* section for more information.

### Environment variables
The project requires some environment variables defined. To set up an environ variable do:
1. Create `.env` file in the root of Django project.
```
.
├── paraphrasetest
│   ├── .env            <---- Here
│   ├── manage.py
│   └── paraphrasetest
│       ├── asgi.py
│       ├── __init__.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── requirements.txt
```
2. Paste the following entry in the `.env` file: 
```
DJANGO_SECRET_KEY=some_django_secret_key_see_below
```
|  Variable name	  | Variable description                                                                                                                                                                                                                                       |
|:----------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|DJANGO_SECRET_KEY	| The secret key is required by Django security middleware. For the security reasons this can not be shared across the internet, and should be setup for each project individual instance separately. Here is a good service to get it: https://djecrety.ir/ |

### Launch of the project

To run the project do:
```
python manage.py runserver
```

Send a request using Postman:
```commandline
http://127.0.0.1:8000/api/paraphrase/?limit=5&tree=(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter) ) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic) ) ) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets) ) (VP (VBN filled) (PP (IN with) (NP (NP (JJ trendy) (NNS bars) ) (, ,) (NP (NNS clubs) ) (CC and) (NP (JJ Catalan) (NNS restaurants) ) ) ) ) ) ) )
```
