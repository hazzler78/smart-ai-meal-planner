import pytest
from smart_meal_planner_backend.services.recipe_service import RecipeService
from smart_meal_planner_backend.schemas.recipe import RecipeCreate, RecipeUpdate

def test_create_recipe(db_session, sample_recipe_data):
    recipe = RecipeService.create_recipe(db_session, RecipeCreate(**sample_recipe_data))
    assert recipe.name == sample_recipe_data["name"]
    assert recipe.description == sample_recipe_data["description"]
    assert len(recipe.ingredients) == len(sample_recipe_data["ingredients"])
    assert recipe.prep_time == sample_recipe_data["prep_time"]
    assert recipe.cook_time == sample_recipe_data["cook_time"]
    assert recipe.servings == sample_recipe_data["servings"]
    assert set(recipe.tags) == set(sample_recipe_data["tags"])

def test_get_recipe(db_session, sample_recipe_data):
    # Create a recipe first
    recipe = RecipeService.create_recipe(db_session, RecipeCreate(**sample_recipe_data))
    
    # Get the recipe
    retrieved_recipe = RecipeService.get_recipe(db_session, recipe.id)
    assert retrieved_recipe is not None
    assert retrieved_recipe.id == recipe.id
    assert retrieved_recipe.name == recipe.name

def test_get_nonexistent_recipe(db_session):
    recipe = RecipeService.get_recipe(db_session, 999)
    assert recipe is None

def test_update_recipe(db_session, sample_recipe_data):
    # Create a recipe first
    recipe = RecipeService.create_recipe(db_session, RecipeCreate(**sample_recipe_data))
    
    # Update the recipe
    update_data = RecipeUpdate(
        name="Updated Recipe",
        prep_time=15,
        cook_time=25,
        tags=["updated", "test"]
    )
    
    updated_recipe = RecipeService.update_recipe(db_session, recipe.id, update_data)
    assert updated_recipe is not None
    assert updated_recipe.name == "Updated Recipe"
    assert updated_recipe.prep_time == 15
    assert updated_recipe.cook_time == 25
    assert set(updated_recipe.tags) == {"updated", "test"}

def test_delete_recipe(db_session, sample_recipe_data):
    # Create a recipe first
    recipe = RecipeService.create_recipe(db_session, RecipeCreate(**sample_recipe_data))
    
    # Delete the recipe
    success = RecipeService.delete_recipe(db_session, recipe.id)
    assert success is True
    
    # Verify recipe is deleted
    deleted_recipe = RecipeService.get_recipe(db_session, recipe.id)
    assert deleted_recipe is None

def test_search_recipes(db_session, sample_recipe_data):
    # Create multiple recipes
    RecipeService.create_recipe(db_session, RecipeCreate(**sample_recipe_data))
    
    veggie_recipe = dict(sample_recipe_data)
    veggie_recipe.update({
        "name": "Vegetable Stir Fry",
        "description": "A healthy veggie recipe",
        "tags": ["vegetarian", "healthy"]
    })
    RecipeService.create_recipe(db_session, RecipeCreate(**veggie_recipe))
    
    # Test search by name
    results = RecipeService.get_recipes(db_session, search="spaghetti")
    assert len(results) == 1
    assert results[0].name == "Test Spaghetti"
    
    # Test search by tag
    results = RecipeService.get_recipes(db_session, tags=["vegetarian"])
    assert len(results) == 1
    assert results[0].name == "Vegetable Stir Fry"

def test_recipe_stats(db_session, sample_recipe_data):
    # Create a recipe
    RecipeService.create_recipe(db_session, RecipeCreate(**sample_recipe_data))
    
    stats = RecipeService.get_recipe_stats(db_session)
    assert stats["total_recipes"] == 1
    assert "italian" in stats["top_tags"]
    assert stats["total_cooking_time_distribution"]["under_30min"] == 1  # 30 mins total (10 prep + 20 cook)

def test_search_by_ingredients(db_session, sample_recipe_data):
    # Create a recipe
    RecipeService.create_recipe(db_session, RecipeCreate(**sample_recipe_data))
    
    # Search with matching ingredients
    results = RecipeService.search_by_ingredients(db_session, ["pasta"])
    assert len(results) == 1
    assert results[0].name == "Test Spaghetti"
    
    # Search with non-matching ingredients
    results = RecipeService.search_by_ingredients(db_session, ["chicken"])
    assert len(results) == 0 

def test_create_recipe_without_ingredients(db_session):
    """Test creating a recipe without any ingredients."""
    recipe_data = {
        "name": "Simple Water",
        "description": "Just water",
        "instructions": ["Pour water in glass"],
        "prep_time": 1,
        "cook_time": 0,
        "servings": 1,
        "tags": ["beverage"],
        "ingredients": []
    }
    recipe = RecipeService.create_recipe(db_session, RecipeCreate(**recipe_data))
    assert recipe.name == recipe_data["name"]
    assert len(recipe.ingredients) == 0

def test_search_recipes_with_nonexistent_tag(db_session, sample_recipe_data):
    """Test searching for recipes with a tag that doesn't exist."""
    RecipeService.create_recipe(db_session, RecipeCreate(**sample_recipe_data))
    results = RecipeService.get_recipes(db_session, tags=["nonexistent"])
    assert len(results) == 0

def test_search_recipes_case_insensitive(db_session, sample_recipe_data):
    """Test that recipe search is case insensitive."""
    RecipeService.create_recipe(db_session, RecipeCreate(**sample_recipe_data))
    results = RecipeService.get_recipes(db_session, search="SPAGHETTI")
    assert len(results) == 1
    assert results[0].name == "Test Spaghetti"

def test_search_recipes_with_multiple_tags(db_session, sample_recipe_data):
    """Test searching for recipes with multiple tags."""
    recipe = RecipeService.create_recipe(db_session, RecipeCreate(**sample_recipe_data))
    
    # Create another recipe with multiple tags
    veggie_recipe = dict(sample_recipe_data)
    veggie_recipe.update({
        "name": "Healthy Pasta",
        "tags": ["vegetarian", "healthy", "pasta"]
    })
    RecipeService.create_recipe(db_session, RecipeCreate(**veggie_recipe))
    
    # Search with multiple tags
    results = RecipeService.get_recipes(db_session, tags=["pasta", "healthy"])
    assert len(results) == 1
    assert results[0].name == "Healthy Pasta"

def test_update_recipe_nonexistent(db_session):
    """Test updating a recipe that doesn't exist."""
    update_data = RecipeUpdate(name="New Name")
    result = RecipeService.update_recipe(db_session, 999, update_data)
    assert result is None

def test_delete_recipe_nonexistent(db_session):
    """Test deleting a recipe that doesn't exist."""
    result = RecipeService.delete_recipe(db_session, 999)
    assert result is False