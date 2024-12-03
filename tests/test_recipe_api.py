import pytest
from fastapi import status

def test_create_recipe(client, sample_recipe_data):
    response = client.post("/api/v1/recipes/", json=sample_recipe_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == sample_recipe_data["name"]
    assert "id" in data

def test_create_recipe_invalid_data(client):
    # Missing required fields
    response = client.post("/api/v1/recipes/", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Invalid prep_time
    invalid_data = {
        "name": "Test Recipe",
        "ingredients": [{"name": "test", "quantity": 1, "unit": "piece"}],
        "instructions": ["Step 1"],
        "prep_time": -1
    }
    response = client.post("/api/v1/recipes/", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_recipes(client, sample_recipe_data):
    # Create a recipe first
    client.post("/api/v1/recipes/", json=sample_recipe_data)
    
    # Test get all recipes
    response = client.get("/api/v1/recipes/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == sample_recipe_data["name"]

def test_get_recipes_with_filters(client, sample_recipe_data):
    # Create recipes
    client.post("/api/v1/recipes/", json=sample_recipe_data)
    
    veggie_recipe = dict(sample_recipe_data)
    veggie_recipe.update({
        "name": "Vegetable Stir Fry",
        "tags": ["vegetarian"]
    })
    client.post("/api/v1/recipes/", json=veggie_recipe)
    
    # Test search
    response = client.get("/api/v1/recipes/?search=vegetable")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Vegetable Stir Fry"
    
    # Test tag filter
    response = client.get("/api/v1/recipes/?tags=vegetarian")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert "vegetarian" in data[0]["tags"]

def test_get_recipe_by_id(client, sample_recipe_data):
    # Create a recipe
    response = client.post("/api/v1/recipes/", json=sample_recipe_data)
    recipe_id = response.json()["id"]
    
    # Get the recipe
    response = client.get(f"/api/v1/recipes/{recipe_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == recipe_id
    assert data["name"] == sample_recipe_data["name"]

def test_get_nonexistent_recipe(client):
    response = client.get("/api/v1/recipes/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_recipe(client, sample_recipe_data):
    # Create a recipe
    response = client.post("/api/v1/recipes/", json=sample_recipe_data)
    recipe_id = response.json()["id"]
    
    # Update the recipe
    update_data = {
        "name": "Updated Recipe Name",
        "prep_time": 15,
        "tags": ["updated"]
    }
    response = client.put(f"/api/v1/recipes/{recipe_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["prep_time"] == update_data["prep_time"]
    assert data["tags"] == update_data["tags"]

def test_delete_recipe(client, sample_recipe_data):
    # Create a recipe
    response = client.post("/api/v1/recipes/", json=sample_recipe_data)
    recipe_id = response.json()["id"]
    
    # Delete the recipe
    response = client.delete(f"/api/v1/recipes/{recipe_id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify recipe is deleted
    response = client.get(f"/api/v1/recipes/{recipe_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_search_recipes_by_ingredients(client, sample_recipe_data):
    # Create a recipe
    client.post("/api/v1/recipes/", json=sample_recipe_data)
    
    # Search by ingredient
    response = client.get("/api/v1/recipes/search/ingredients?ingredients=pasta")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_recipe_data["name"]

def test_get_recipe_stats(client, sample_recipe_data):
    # Create recipes
    client.post("/api/v1/recipes/", json=sample_recipe_data)
    
    # Get stats
    response = client.get("/api/v1/recipes/stats")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_recipes" in data
    assert "top_tags" in data
    assert "total_cooking_time_distribution" in data 