from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from ..models.recipe import Recipe
from ..schemas.recipe import RecipeCreate, RecipeUpdate

class RecipeService:
    @staticmethod
    def get_recipes(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_rating: Optional[float] = None
    ) -> List[Recipe]:
        """Get recipes with optional filtering and pagination."""
        query = db.query(Recipe)

        if search:
            search_term = search.strip().lower()
            query = query.filter(or_(
                Recipe.name.ilike(f"%{search_term}%"),
                Recipe.description.ilike(f"%{search_term}%")
            ))

        if tags:
            normalized_tags = [tag.lower().strip() for tag in tags]
            for tag in normalized_tags:
                query = query.filter(Recipe.tags.like(f'%{tag}%'))

        if min_rating is not None:
            query = query.filter(Recipe.rating >= min_rating)

        return query.order_by(Recipe.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_recipe(db: Session, recipe_id: int) -> Optional[Recipe]:
        """Get a specific recipe by ID."""
        return db.query(Recipe).filter(Recipe.id == recipe_id).first()

    @staticmethod
    def create_recipe(db: Session, recipe: RecipeCreate) -> Recipe:
        """Create a new recipe."""
        db_recipe = Recipe(**recipe.dict())
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        return db_recipe

    @staticmethod
    def update_recipe(
        db: Session,
        recipe_id: int,
        recipe_update: RecipeUpdate
    ) -> Optional[Recipe]:
        """Update an existing recipe."""
        db_recipe = RecipeService.get_recipe(db, recipe_id)
        if not db_recipe:
            return None

        update_data = recipe_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_recipe, field, value)

        db.commit()
        db.refresh(db_recipe)
        return db_recipe

    @staticmethod
    def delete_recipe(db: Session, recipe_id: int) -> bool:
        """Delete a recipe."""
        db_recipe = RecipeService.get_recipe(db, recipe_id)
        if not db_recipe:
            return False

        db.delete(db_recipe)
        db.commit()
        return True

    @staticmethod
    def search_by_ingredients(
        db: Session,
        ingredients: List[str],
        match_threshold: float = 0.5,
        limit: int = 10
    ) -> List[Recipe]:
        """Search recipes by ingredients with matching threshold."""
        query = db.query(Recipe)
        recipes = query.all()
        
        # Normalize ingredient names
        search_ingredients = {ing.lower().strip() for ing in ingredients}
        
        # Filter and score recipes
        matching_recipes = []
        for recipe in recipes:
            recipe_ingredients = {
                ing["name"].lower().strip() 
                for ing in recipe.ingredients
            }
            
            # Calculate matching score
            matching_count = len(recipe_ingredients & search_ingredients)
            total_required = len(recipe_ingredients)
            match_score = matching_count / total_required
            
            if match_score >= match_threshold:
                matching_recipes.append((recipe, match_score))
        
        # Sort by match score and return top results
        matching_recipes.sort(key=lambda x: x[1], reverse=True)
        return [recipe for recipe, _ in matching_recipes[:limit]]

    @staticmethod
    def get_recipe_stats(db: Session) -> Dict:
        """Get statistics about recipes."""
        total_recipes = db.query(Recipe).count()
        
        # Get average ratings and times
        stats = db.query(
            func.avg(Recipe.rating).label('avg_rating'),
            func.avg(Recipe.prep_time).label('avg_prep_time'),
            func.avg(Recipe.cook_time).label('avg_cook_time')
        ).first()
        
        # Get all unique tags and their counts
        all_recipes = db.query(Recipe).all()
        tag_counts = {}
        for recipe in all_recipes:
            if recipe.tags:
                for tag in recipe.tags:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Get top tags
        top_tags = sorted(
            tag_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            "total_recipes": total_recipes,
            "avg_rating": round(stats.avg_rating or 0, 2),
            "avg_prep_time": round(stats.avg_prep_time or 0, 1),
            "avg_cook_time": round(stats.avg_cook_time or 0, 1),
            "top_tags": dict(top_tags),
            "total_cooking_time_distribution": {
                "under_30min": len([r for r in all_recipes if (r.prep_time + r.cook_time) <= 30]),
                "30_60min": len([r for r in all_recipes if 30 < (r.prep_time + r.cook_time) <= 60]),
                "over_60min": len([r for r in all_recipes if (r.prep_time + r.cook_time) > 60])
            }
        }