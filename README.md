# Tiny To-Do App (Flask + Azure)

## 1) Executive Summary
- **Problem.** With the daily workloads of everyday life, students and small teams just need a lightweight way to track and place tasks in an organized list without having to constantly log in to heavy tools or navigate complex websites. When in a rush, students need a simple to do with minimal functions that allow one to add tasks quickly, remove them when finished, or cross tasks off when they are finally complete. 
- **Solution.** Tiny To-Do is a minimal Flask web app that stores todos in Azure Blob Storage and runs in a Docker container. It is a solution for students looking for such a simple app. 

## 2) System Overview
**Course Concept(s).**  
- Flask APIs (web services module)  
- Cloud storage via Azure Blob Storage

**Architecture Diagram.**  
![Sample App Function](assets/app.png)

API Endpoints:
  - `GET /api/todos`
  - `POST /api/todos`
  - `POST /api/todos/<id>/toggle`
  - `DELETE /api/todos/<id>`
- **Data/Models/Services.**
  - Data: list of todos: `[{ "id": str, "text": str, "done": bool }, ...]`.
  - Storage: Azure Blob Storage, container `todo-data`.
  - Services: Flask app running in Docker and Azure App Service deployment

## 3) How to Run (Local)

### Prerequisites
- Install [Docker](https://docs.docker.com/get-docker/).
- Create a `.env` file in the project root based on `.env.example`.

Example `.env` (do NOT commit your real secrets):

```env
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=...your-real-string-here..."
TODO_CONTAINER="todo-data"
PORT=8000
```
- Build Docker 
```env
docker build -t tiny-todo:latest .
docker run --rm \
  -p 8080:8000 \
  --env-file .env \
  tiny-todo:latest
```
- Open the App: http://localhost:8080/
- Health Check:
```env
curl http://localhost:8080/api/health
```

## 4) Design Decisions 
- **Why this concept?** I chose to design the to-do list while keeping this specific design in mind because it allowed me to use concepts that I used in class while also creating a simple concept that is easy to use and build upon for future use. While this project is more simple than other alternative designs that were considered, it allows users to learn mechanics quickly and creates a simple and fast way to keep track of daily tasks without the hassle of complex learning curves. 
- **Alternatives Considered**I considered separating the to-do list into days of the week but finally planned against the idea as it would over complicate the app. The main purpose of the app is to provide a quick and easy way to keep track of daily and everchanging apps in the midst of work-heavy and fast-paced days. If I added multiple days of the week, the quick and "fast-paced" concept of the app would be diminished and provide an added layer of complexity that other apps already provide. 
- **Tradeoffs** All tasks will be stored inside a single JSON blob in Azure Blob Storage. This is easy to manage and works quite well for everyday tasks that are to be deleted by the end of the daybut not ideal for large datasets. If the app were to be scaled to multiple users, it would be smarter to construct and use a proper database. I intentionally avoided using advanced features which would slow down the user experience. However, the tradeoff is that the app is less customizable. The code is simple and easy to maintain but not designed for large-scale extensions. 
- **Security & Privacy** The data lives in a private Azure Blob Storage container; only the app can write to it via its connection string.

## 5) Results & Evaluation
I manually tested each API route (add, toggle, delete, list) and included a test in tests/test_health.py, which verifies that the /api/health endpoint returns a successful status.

## What's Next 
I want to allow each user to have their own private to-do list. Additionally, I want to work to add more features such as "clear all completed tasks" or "mark all as done" to speed up the user's processes. Finally, as the app gains traction, I want to migrate from JSON to a database for more scalability. 

## 7) Links
- **GitHub Repo:** https://github.com/rashiadhikarira/tiny-todo-azure
- **Public Cloud App:** https://tiny-todo-26021.azurewebsites.net/
