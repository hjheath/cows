# cows

NHS Hack Day 26 Project - Finding Computers on Wheels (cows)


             __n__n__
      .------`-/-'
     /  ##  ## (oo)
    / \## __   ./
       |//YY \|/
       |||   |||
     Where's Bessie?

This application consists of:

* A python script that regularly sends data from a cow to the server
* A flask web server that listens for cow data and saves them to a sqlite database
* A JSON API to serve the data (on the same flask server)

## Developing the app

Installing dependencies:
`pip install -r requirements.txt`

Running the server:
`flask run --debug`

Running the cow worker:
`python send_cow_data.py <cow_name>`

Connect to the database:
`sqlite3 instance/cows.sqlite3`

Reset the database:
```sh
flask shell

>>> from app import db
>>> db.drop_all()
```

## JSON API

* List cows: `GET /cows`
* Get cow: `GET /cows/<name>`
* Update cow: `PUT /cows/<name>`

![alt text](https://github.com/hjheath/cows/blob/main/static/nhshacklogo.png)
Runner up prize NHS Hack 2024 24/25 February
