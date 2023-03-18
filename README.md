# Technology Intelligence Retrieval System

This project implements a technology intelligence retrieval system, which includes spider crawling technology intelligence information, multi-threaded spider task management, technology intelligence information retrieval and display, technology intelligence information graph display, path discovery and display, K-jump query and display, and clustering/community discovery and display. The backend uses the Neo4j and Django frameworks, and the frontend uses Relation-graph and React frameworks.

## Features

- [x] Automatically crawl technology intelligence information with spiders
- [x] Manage spider tasks with multi-threading
- [x] Implement technology intelligence information retrieval and display with Django
- [ ] Implement technology intelligence information graph display with Relation-graph and React
- [ ] Support discovery and display of all paths and shortest paths
- [ ] Support K-jump query and display
- [ ] Support clustering/community discovery and display

## Tech Stack

- Backend: Neo4j and Django
- Frontend: Relation-graph and React

## References

- Django: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django
- React: https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Client-side_JavaScript_frameworks/React_getting_started
- Relation-graph: https://github.com/seeksdream/relation-graph
- Neo4j: https://neo4j.com/docs/
- Neo4j Application: https://www.jianshu.com/p/4788ddc0e350
- Neo4j Performance Optimization Guide: https://neo4j.com/developer/guide-performance-tuning/
- Practice of Selenium Multi-threading: https://cloud.tencent.com/developer/article/1667332
- Neo4j Performance Optimization: https://www.slideshare.net/neo4j/optimizing-cypher-32550605

## Installation and Usage

### Backend

- Install and start the Neo4j database
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

- Modify the address and port of the backend server in the `frontend/src/config.js` file
- Execute the following command in the terminal to start the frontend server:

    ```npm start```

- Open http://localhost:3000/ in the browser to view the web page.

## Acknowledgments

This project uses the following open source projects:

- Relation-graph
