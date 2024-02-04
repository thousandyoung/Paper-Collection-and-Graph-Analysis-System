# Paper Collection and Graph Analysis System

This project implements a technology intelligence retrieval system.

## Features

- [x] Improved performance of Cypher via APOC
- [x] Automatically crawl technology intelligence information with spiders
- [x] Manage spider tasks with multi-threading
- [x] Implement technology intelligence information retrieval and display with Django
- [x] Implement technology intelligence information graph display with ECharts and React
- [x] Support discovery and display of all paths and shortest paths
- [x] Support K-jump query and display
- [x] Support community discovery and display

## Tech Stack

- Backend: Neo4j and Django
- Frontend: ECharts and React

## Installation and Usage

### Backend

- Install and start the Neo4j database
- APOC can be installed by moving the APOC jar file from the $NEO4J_HOME/labs directory to the $NEO4J_HOME/plugins directory and restarting Neo4j.
- Navigate to the `backend` directory in the terminal and execute the following command to install Python dependencies: 
    ```pip install -r requirements.txt```
- Create a new database in the Neo4j database
- Modify the connection parameters of the Neo4j database in the `backend/backend/settings.py` file
- Navigate to the `backend` directory in the terminal and execute the following command to migrate data:
python manage.py migrate

- Execute the following command in the terminal to start the backend server:
`python manage.py runserver`

### Frontend

- Navigate to the `frontend` directory in the terminal and execute the following command to install frontend dependencies:
    ```npm install```

- Modify the address and port of the backend server in the `frontend/src/services` ‘s files
- Execute the following command in the terminal to start the frontend server:

    ```npm start```

- Open http://localhost:3000/ in the browser to view the web page.


## UI Preview
![KG](img/KG.jpg)
![papers](img/papers.jpg)
![spider](img/spider.jpg)

## Appendix
### APOC Optimization Results
![APOC Optimization Results](img/apoc.jpg)

### Community Discovery Performance Table
![Community Discovery Performance Table](img/cdpt.jpg)

### Flowchart
![Flowchart 1](img/fc1.jpg)
![Flowchart 2](img/fc2.jpg)
