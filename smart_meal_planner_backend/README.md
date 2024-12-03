# Smart AI Meal Planner Backend

[![CI Pipeline](https://github.com/hazzler78/smart-ai-meal-planner/actions/workflows/ci.yml/badge.svg)](https://github.com/hazzler78/smart-ai-meal-planner/actions/workflows/ci.yml)
[![CD Pipeline](https://github.com/hazzler78/smart-ai-meal-planner/actions/workflows/cd.yml/badge.svg)](https://github.com/hazzler78/smart-ai-meal-planner/actions/workflows/cd.yml)

A production-ready FastAPI backend for the Smart AI Meal Planner application. Built with modern Python and best practices for scalability, maintainability, and security.

## Deployment Status
[![CD Pipeline](https://github.com/hazzler78/smart-ai-meal-planner/actions/workflows/cd.yml/badge.svg)](https://github.com/hazzler78/smart-ai-meal-planner/actions/workflows/cd.yml)

## Live API Endpoints
- Base URL: https://smart-ai-meal-planner.herokuapp.com
- Interactive Docs: https://smart-ai-meal-planner.herokuapp.com/docs
- API Reference: https://smart-ai-meal-planner.herokuapp.com/redoc

## Setup & Development

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL:
- Create a database named 'smart_meal_planner'
- Update database credentials in config.py if needed

5. Initialize the database:
```bash
alembic upgrade head
```

6. Run the application:
```bash
uvicorn main:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Features

- Inventory Management
- Recipe Management
- Shopping List
- AI-powered meal suggestions

## Project Structure

```
smart_meal_planner_backend/
├── alembic/
├── models/
│   ├── inventory.py
│   ├── recipe.py
│   └── shopping_list.py
├── config.py
├── database.py
├── main.py
└── requirements.txt
``` 