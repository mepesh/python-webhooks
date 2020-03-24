# python-webhooks
connecting python app  with chat-bot for custom services

## Getting Starded
To start using project:
```shell
$ git clone https://github.com/mepesh/python-webhooks
$ cd python-webhooks
```
Setup virtual enviroment:
```shell
$ virtualenv venv
$ source venv/bin/activate
```
Install requirements:
```shell
pip install -r requirements.txt
```
To run flask app
```shell
$ env FLASK_APP=main.py flask run
```
or export enviromental variable from .env.sample to shell and run
```shell
$ export FLASK_APP=main.py
$ flask run
```
or simply run as: 
```shell
$ python main.py
```
