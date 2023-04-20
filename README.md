# Vacation Planner

* [Description](#description)
* [Tech-stack](#tech-stack)
* [Architecture](#architecture)
* [Diagrams](#diagrams)
* [How to run](#how-to-run)
* [Testing](#testing)
* [Deployment](#deployment)
* [CI CD](#ci-cd)
* [Web scrapper](#web-scrapper)

## Description
<details><summary><b>General info</b></summary>Web application to plan group vacation, select date, place, vote on them and choose the best option for everyone. Additional tool to search web for suiting accommodation options. Integrated chat to communicate between group members or event participants</details>
<details><summary><b>Application purpose</b></summary>
Application will be used to arrange vacations for a group of friends. The main problem is selecting matching date and place to go. Application will allow users to group together, create events, propose dates and places and vote on them to select the best possible option.</details>
<details><summary><b>Application flow</b></summary>
- Register and login
- Configure your family (adults, children, infants)
- Create or join a group
- Create event for a group and automatically add all group members to it
- Creator of an event becomes its owner and can grant owner or admin status to any other member
- At each step members of a group can leave the event
- Each group member can propose and vote on a date (start and end of the event). After voting each member of a group must confirm finishing this step.
- Date is approved by a event owner or admin
- User can add vacation places to its own profile to propose it in event. It should contain link, capacity, description and other necessary information
- User can start web scrapping task to retrieve list of suitable places
- Users can propose and vote on a place to go
- Place is approved by a event owner / admin
- User that proposed selected place gets an email and internal notification to book this place
- User that proposed selected place mark it as booked or retrieve the proposal to go back to place selection. He can also give information about advance payment 
- Event is marked as booked
- All the time users can communicate through chat within friends group or event
</details>

## Tech-stack
<ul>
<li>Python</li>
<li>Django</li>
<li>Django Rest Framework</li>
<li>Celery</li>
<li>RabbitMQ</li>
<li>Javascript</li>
<li>Postgresql</li>
<li>Selenium</li>
<li>Redis</li>
<li>Docker</li>
<li>AWS</li>
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

### Database
<img src="https://user-images.githubusercontent.com/29715549/232879614-dc41dcd4-47a2-4bc5-899d-330e73515aec.png" width="100%" height="100%">

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
