# SIMPLON DEV IA | Brief 3 (09/01/24)

## FastAPI - exposer les données de transactions immobilières via une API

### Contexte

Rendu du brief en semaine 3 introduisant aux principes d'API et API REST en utilisant FastAPI. Après avoir réalisé le second brief ([voir ici](https://github.com/Sandalcho7/simplon_brief02)) nous demandant de rédiger les requêtes SQL pour répondre aux différentes user stories, nous sommes maintenant en charge de développer l'API REST exposant les résultats de ces requêtes en utilisant FastAPI.

### Prérequis

Avant de démarrer le développement le projet, il est nécessaire d'installer FastAPI, Uvicorn, SQLite et PyYAML sur l'environnement de travail. Pour effectuer ces installations, vous pouvez éxécuter la commande suivante :
```bash
pip install -r ressources/requirements.txt
```

### Data

[Lien vers les user stories](https://docs.google.com/spreadsheets/d/110DFqhV0eNhR1mzBkRR5DD6Aey-lgXuTlf3VeSzWD58/edit#gid=0)

[Lien vers les données à utiliser](https://www.kaggle.com/datasets/benoitfavier/immobilier-france/data)

[Premiers pas sur FastAPI](https://fastapi.tiangolo.com/fr/tutorial/first-steps/)

[Paramètres de chemin sur FastAPI](https://fastapi.tiangolo.com/fr/tutorial/path-params/)

### Notes

Certaines requêtes SQL sont légèrement différentes des user stories fournies, par l'ajout de paramètres, je les ai rendues plus génériques et donc utilisables dans de plus nombreux cas (différentes années, villes, etc.).

### Doc

Pour un hôte (127.0.0.1) et un port (8000), accédez à http://127.0.0.1:8000/docs sur votre navigateur, une fois le serveur lancé, pour accéder aux fonctionnalités de l'API.

<br><hr>

<br>User story 1 :
    URL: /average_revenue/{city}
        Method: GET
        URL Params:
            city [string] (required)
        Success Response: JSON object with average revenue for the selected city.
        Error Response:
            400 Bad Request if null response

<br>User story 2 :
    URL: /last_transactions/{city}_last_{number}
        Method: GET
        URL Params:
            city [string] (required)
            number [int] (required)
        Success Response: JSON object with last transactions for the selected city. The 'number' parameter selects the number of displayed transactions.
        Error Response:
            400 Bad Request if null response

<br>User story 3 :
    URL: /transactions_count/{city}_{year}
        Method: GET
        URL Params:
            city [string] (required)
            year [string] (required)
        Success Response: JSON object with transactions count for the selected city and year.
        Error Response:
            400 Bad Request if null response

<br>User story 4 :
    URL: /average_price_per_square_meter/{year}_{type}
        Method: GET
        URL Params:
            city [string] (required)
            type [string] (required)
        Success Response: JSON object with average price per square meter for the selected city and building type.
        Error Response:
            400 Bad Request if null response

<br>User story 5 :
    URL: /transactions_count2/{city}_{year}_{type}_{rooms}
        Method: GET
        URL Params:
            city [string] (required)
            year [string] (required)
            type [string] (required)
            rooms [int] (required)
        Success Response: JSON object with transactions count for selected city, year, building type, and number of rooms.
        Error Response:
            400 Bad Request if null response

<br>User story 6 :
    URL: /transactions_by_pieces/{city}_{year}_{type}
        Method: GET
        URL Params:
            city [string] (required)
            year [string] (required)
        Success Response: JSON object with transactions repartition for the selected city, year, and building type.
        Error Response:
            400 Bad Request if null response

<br>User story 7 :
    URL: /average_price_per_square_meter2/{city}_{year}_{type}
        Method: GET
        URL Params:
            city [string] (required)
            year [string] (required)
            type [string] (required)
        Success Response: JSON object with average price per square meter for the selected city, year, and building type.
        Error Response:
            400 Bad Request if null response

<br>User story 8 :
    URL: /transactions_by_dpt/
        Method: GET
        Success Response: JSON object with department ranking for transactions count.
        Error Response:
            400 Bad Request if null response

<br>User story 9 :
    URL: /transactions_count3/{year1}_{revenu}_{year2}_{type}
        Method: GET
        URL Params:
            year1 [string] (required) - Year of the average taxable income
            revenu [int] (required) - Minimal average taxable income
            year2 [string] (required) - Year of the transactions count
            type [string] (required) - Building type
        Success Response: JSON object with transactions count for the selected year and building type, for the cities that had an average taxable income above the selected minimal income ('revenu') at a chosen year ('year2').
        Error Response:
            400 Bad Request if null response

<br>User story 10

    URL: /cities_top10_transactions/
    Method: GET
    Success Response: JSON object with the 10 cities that record the highest number of transactions.
    Error Response:
        400 Bad Request if null response

<br>User stories 11 & 12

    URL: /cities_top10_price/{type}
    Method: GET
    URL Params:
        type [string] (required)
    Success Response: JSON object with the 10 cities that have the lowest average price per square meter.
    Error Response:
        400 Bad Request if null response