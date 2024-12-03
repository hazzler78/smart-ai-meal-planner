import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from typing import Generator

# Import all models to ensure they are registered with SQLAlchemy
from smart_meal_planner_backend.models.recipe import Recipe
from smart_meal_planner_backend.models.inventory import InventoryItem
from smart_meal_planner_backend.models.shopping_list import ShoppingListItem
from smart_meal_planner_backend.database import Base, get_db
from smart_meal_planner_backend.main import app

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

@pytest.fixture(scope="function")
def engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Create all tables for all declared models
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_recipe_data():
    return {
        "name": "Test Spaghetti",
        "description": "A test recipe",
        "ingredients": [
            {"name": "pasta", "quantity": 500, "unit": "g"},
            {"name": "tomato sauce", "quantity": 1, "unit": "cup"}
        ],
        "instructions": [
            "Boil water",
            "Cook pasta",
            "Add sauce"
        ],
        "prep_time": 10,
        "cook_time": 20,
        "servings": 4,
        "tags": ["italian", "pasta", "quick"]
    } 