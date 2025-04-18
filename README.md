# To-Do List Application with FastAPI and React

## Description

This is a full-stack To-Do List application built with a FastAPI backend and a React frontend. It allows users to create, read, update, and delete tasks, as well as filter them by completion status. The frontend includes a dark mode toggle.

## Table of Contents

-   [Description](#description)
-   [Table of Contents](#table-of-contents)
-   [Setup Instructions](#setup-instructions)
-   [Backend API Endpoints](#backend-api-endpoints)
-   [Live Links](#live-links)
-   [Technologies Used](#technologies-used)


## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd todo-app
    ```

2.  **Backend Setup:**

    * Navigate to the backend directory:

        ```bash
        cd backend
        ```

    * (Optional but Recommended) Create a virtual environment:

        ```bash
        python -m venv venv
        # Activate the virtual environment:
        # Windows:
        .\venv\Scripts\activate
        # macOS/Linux:
        source venv/bin/activate
        ```

    * Install backend dependencies:

        ```bash
        pip install fastapi sqlalchemy aiosqlite 
        # or, if you have a requirements.txt file:
        # pip install -r requirements.txt
        ```

        * **Note:** This project uses `aiosqlite` for asynchronous SQLite database operations.

    * Run the backend server:

        ```bash
        uvicorn main:app --reload
        # Assuming your main FastAPI app instance ('app') is in 'main.py'
        ```

        * The backend will be running at `http://localhost:8000`.

3.  **Frontend Setup:**

    * Navigate to the frontend directory:

        ```bash
        cd ../frontend
        ```

    * Install frontend dependencies:

        ```bash
        npm install
        # or yarn install
        ```

    * Run the frontend development server:

        ```bash
        npm run dev
        ```

        * The frontend will be running at `http://localhost:5173`

## Backend API Endpoints

### Base URL: `https://todo-app-fastapi-0lea.onrender.com/docs` 

| Endpoint               | Method | Request Body                                 | Response Body                                                                                                                                | Description                                                                 |
| :--------------------- | :----- | :------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `/todos/?skip={int}&limit={int}&completed={bool}` | GET    | None                                           | `[ { "id": int, "title": str, "completed": bool }, ... ]`                                                     | Get all tasks, with optional pagination (`skip`, `limit`) and filtering. |
| `/todos/`               | POST   | `{ "title": "New Task Title", "completed": bool (optional, default: false) }` | `{ "id": int, "title": str, "completed": bool }`                                                             | Create a new task.                                                        |
| `/todos/{todo_id}`     | GET    | None                                           | `{ "id": int, "title": str, "completed": bool }`                                                             | Get a single task by ID.                                                    |
| `/todos/{todo_id}`     | PUT    | `{ "title": str (optional), "completed": bool (optional) }` | `{ "id": int, "title": str, "completed": bool }`                                                             | Update a task. Only provided fields are updated.                            |
| `/todos/{todo_id}`     | DELETE | None                                           | `{ "message": "Todo deleted" }`                                                                                                             | Delete a task by ID.                                                        |

**Note:**

* The frontend interacts with the backend running at `http://localhost:8000` during development. You will need to replace this with your deployed backend URL in the frontend code (likely in `src/App.jsx`) when you deploy.
* The `GET /todos/` endpoint supports optional query parameters `skip` (for pagination), `limit` (for pagination), and `completed` (to filter by completion status: `true` for completed, `false` for pending).

## Live Links

-   Backend: `https://todo-app-fastapi-0lea.onrender.com/docs` 
-   Frontend: `https://todo-app-fastapi-react-ussc-git-main-arielll74s-projects.vercel.app/` 

## Technologies Used

-   Backend: FastAPI, Python, SQLAlchemy (async), aiosqlite
-   Frontend: React, JavaScript, Axios

