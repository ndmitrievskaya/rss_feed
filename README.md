# RSS FEED

RSS FEED - an application to get last news from the feeds you enjoy! 

## Getting Started

To start this project you need to clone this repository to your local machine. 

### Prerequisites

After cloning the repo you need to install all the requirements with the command below. 

```
pip install -r requirements.txt
```
You also need Docker to be installed and started. Please check [docker.com](https://www.docker.com) for further instructions. 

### How to use

First you need to build up the containers.

```
docker-compose up --build -d  
```

To start the app you need only one simple command. Check if you are in the root directory of the project.

```
docker-compose up
```

It will start the containers.
Before correct usage you need to make the cache table in the database with the commands below

```
docker-compose exec web alembic revision --autogenerate -m 'Create rss feed cache table'
docker-compose exec web alembic upgrade head
```

After all project will be available on http://127.0.0.1:8000/docs and with the endpoint localhost:8000/get_news

## Authors

* **Nika Dmitrievskaya** - *Initial work* - [kabanovanika](https://github.com/ndmitrievskaya)
