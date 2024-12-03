from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.recipe_service import RecipeService
from ..schemas.recipe import (
    Recipe as RecipeSchema,
    RecipeCreate,
    RecipeUpdate
)

router = APIRouter()

@router.get("/", response_model=List[RecipeSchema])
def get_recipes(
    skip: int = Query(0, ge=0, description="Number of recipes to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of recipes to return"),
    search: Optional[str] = Query(None, description="Search term for recipe name or description"),
    tags: Optional[List[str]] = Query(None, description="Filter recipes by tags"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating filter"),
    db: Session = Depends(get_db)
):
    """
    Get all recipes with optional filtering and pagination.
    
    - **skip**: Number of recipes to skip (for pagination)
    - **limit**: Maximum number of recipes to return
    - **search**: Optional search term for recipe name or description
    - **tags**: Optional list of tags to filter by
    - **min_rating**: Optional minimum rating filter
    """
    return RecipeService.get_recipes(
        db,
        skip=skip,
        limit=limit,
        search=search,
        tags=tags,
        min_rating=min_rating
    )

@router.get("/stats", response_model=dict)
def get_recipe_stats(db: Session = Depends(get_db)):
    """Get statistics about recipes including ratings, cooking times, and popular tags."""
    return RecipeService.get_recipe_stats(db)

@router.get("/search/ingredients", response_model=List[RecipeSchema])
def search_recipes_by_ingredients(
    ingredients: List[str] = Query(..., min_items=1, description="List of ingredients to search for"),
    match_threshold: float = Query(0.5, ge=0.0, le=1.0, description="Minimum ingredient match ratio"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of recipes to return"),
    db: Session = Depends(get_db)
):
    """
    Search recipes by ingredients.
    
    - **ingredients**: List of ingredient names to search for
    - **match_threshold**: Minimum percentage of matching ingredients required (0.0 to 1.0)
    - **limit**: Maximum number of recipes to return
    """
    return RecipeService.search_by_ingredients(
        db,
        ingredients,
        match_threshold=match_threshold,
        limit=limit
    )

@router.post("/", response_model=RecipeSchema)
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db)
):
    """Create a new recipe."""
    return RecipeService.create_recipe(db, recipe)

@router.get("/{recipe_id}", response_model=RecipeSchema)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific recipe by ID."""
    recipe = RecipeService.get_recipe(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/{recipe_id}", response_model=RecipeSchema)
def update_recipe(
    recipe_id: int,
    recipe_update: RecipeUpdate,
    db: Session = Depends(get_db)
):
    """Update a recipe."""
    updated_recipe = RecipeService.update_recipe(db, recipe_id, recipe_update)
    if updated_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated_recipe

@router.delete("/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    """Delete a recipe."""
    if not RecipeService.delete_recipe(db, recipe_id):
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"} 