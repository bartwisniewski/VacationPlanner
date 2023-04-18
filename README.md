# Vacation Planner

* [General info](#general-info)
* [Tech-stack](#tech-stack)
* [Architecture](#architecture)
* [Diagrams](#diagrams)
* [Description](#description)
* [How to run](#how-to-run)
* [Testing](#testing)
* [Deployment](#deployment)
* [CI CD](#ci-cd)
* [Web scrapper](#web-scrapper)

## General info
<b>Vacation planner</b>. Web application to plan group vacation, select date, place, vote on them and choose the best option for everyone. Additional tool to search web for suiting accommodation options. Integrated chat to communicate between group members or event participants

## Tech-stack
<ul>
<li>Python</li>
<li>Django</li>
<li>Django Rest Framework</li>
<li>Celery</li>
<li>RabbitMQ</li>
<li>Javascript</li>
<li>Postgresql</li>
<li>Redis</li>
</ul>

## Architecture
### Repositories
Project has a polyrepo structure. It is divided into two repositories:
<ul>
<li>core - this repository. Main functionality and frontend: https://github.com/bartwisniewski/VacationPlanner</li>
<li>scrapper. Web scrapper microservice: https://github.com/bartwisniewski/vpscrap
</ul>

### C4
Project architecture is documented as a C4 diagrams in a DSL file created in a Structurizr:
https://github.com/bartwisniewski/VacationPlanner/blob/main/doc/architecture/workspace.dsl

Commands:
- To see the diagrams run locally `$ doc/architecture/preview.sh`
- To validate DSL run locally `$ doc/architecture/validate.sh`

## Diagrams
### C4

|||
| ------------- | ------------- |
| Context  | Containers |
|<img src="https://user-images.githubusercontent.com/29715549/232713086-7a390ced-7f95-46b5-8d13-27debedd0fc8.png" width="100%" height="100%">|<img src="https://user-images.githubusercontent.com/29715549/232713973-82ad524a-6d9e-4881-9583-71fc28d3cacb.png" width="100%" height="100%">|
| Components - core  | Components - scrapper |
|<img src="https://user-images.githubusercontent.com/29715549/232714034-2b2d9003-0a35-4098-b768-e033a77ced60.png" width="100%" height="100%">|<img src="https://user-images.githubusercontent.com/29715549/232714101-01695b24-ab07-4cb8-8467-507848e685c1.png" width="100%" height="100%">|

### Data

## Description
Vacation planner. Web application to plan group vacation, select date, place, vote on them and choose the best option for everyone. Additional tool to search web for suiting accommodation options. Integrated chat to communicate between group members or event participants

## How to run
Project is prepared to run locally in docker:
download both services:

```git clone https://github.com/bartwisniewski/VacationPlanner```

```git clone https://github.com/bartwisniewski/vpscrap```

run docker compose for both repositories:

```docker-compose -f <base directory>/vpscrap/deployment/dev/docker-compose.yml up --build -d```

```docker-compose -f <base directory>/vpcore/deployment/dev/docker-compose.yml up --build -d```

open in a browser:
127.0.0.1:8001

## Testing
As this is a portfolio project, not a real production application project is not fully covered with testing. To show possiblities I have prepared tests for 1 django app: "Friends"

Locally tests can be run with use of tox

```pip install tox```

cd to the project and run:

```tox -e core```

## Deployment
For learning purposes core part of a project has been deployed on AWS EB with use of EB CLI

## CI CD
- pre-commit-hooks
https://github.com/bartwisniewski/VacationPlanner/blob/main/.pre-commit-config.yaml
- github actions
https://github.com/bartwisniewski/VacationPlanner/blob/main/.github/workflows/django.yml

## Web scrapper
Seperate microservice for web scrapping, source available here:
https://github.com/bartwisniewski/vpscrap
