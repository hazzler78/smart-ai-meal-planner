from typing import List, Dict, Optional
from pydantic import BaseModel, Field, validator, confloat
from datetime import datetime

class IngredientSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the ingredient",
        example="flour"
    )
    quantity: float = Field(
        ...,
        gt=0,
        description="Quantity of the ingredient",
        example=200
    )
    unit: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Unit of measurement",
        example="g"
    )

    @validator('name', 'unit')
    def normalize_strings(cls, v):
        return v.strip().lower()

class RecipeBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Recipe name",
        example="Spaghetti Carbonara"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Recipe description",
        example="A classic Italian pasta dish"
    )
    ingredients: List[IngredientSchema] = Field(
        default=[],
        description="List of ingredients with quantities"
    )
    instructions: List[str] = Field(
        ...,
        min_items=1,
        description="Step-by-step instructions",
        example=["Boil pasta", "Prepare sauce", "Mix together"]
    )
    prep_time: int = Field(
        default=0,
        ge=0,
        description="Preparation time in minutes",
        example=15
    )
    cook_time: int = Field(
        default=0,
        ge=0,
        description="Cooking time in minutes",
        example=20
    )
    servings: int = Field(
        default=1,
        gt=0,
        le=50,
        description="Number of servings",
        example=4
    )
    tags: Optional[List[str]] = Field(
        default=[],
        max_items=10,
        description="Recipe tags (e.g., dietary restrictions, cuisine type)",
        example=["italian", "pasta", "quick"]
    )
    rating: Optional[float] = Field(
        None,
        ge=0,
        le=5,
        description="Recipe rating (0-5 stars)",
        example=4.5
    )

    @validator('instructions')
    def validate_instructions(cls, v):
        if not all(isinstance(step, str) and step.strip() for step in v):
            raise ValueError('All instructions must be non-empty strings')
        return [step.strip() for step in v]

    @validator('tags')
    def validate_tags(cls, v):
        if v is None:
            return []
        unique_tags = list({tag.lower().strip() for tag in v if tag.strip()})
        if len(unique_tags) > 10:
            raise ValueError('Maximum 10 tags allowed')
        return unique_tags

    @validator('rating')
    def validate_rating(cls, v):
        if v is not None and not (0 <= v <= 5):
            raise ValueError('Rating must be between 0 and 5')
        return v

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    ingredients: Optional[List[IngredientSchema]] = Field(None, min_items=1)
    instructions: Optional[List[str]] = Field(None, min_items=1)
    prep_time: Optional[int] = Field(None, ge=0)
    cook_time: Optional[int] = Field(None, ge=0)
    servings: Optional[int] = Field(None, gt=0, le=50)
    tags: Optional[List[str]] = None
    rating: Optional[float] = Field(None, ge=0, le=5)

    @validator('tags')
    def validate_update_tags(cls, v):
        if v is None:
            return []
        unique_tags = list({tag.lower().strip() for tag in v if tag.strip()})
        if len(unique_tags) > 10:
            raise ValueError('Maximum 10 tags allowed')
        return unique_tags

class Recipe(RecipeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True