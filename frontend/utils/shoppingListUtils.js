/**
 * Combine ingredients from multiple recipes and consolidate quantities
 * @param {Array} recipes - Array of recipe objects
 * @returns {Array} Combined list of ingredients
 */
export const combineIngredients = (recipes) => {
  if (!Array.isArray(recipes)) {
    return [];
  }

  const ingredientMap = new Map();

  recipes.forEach(recipe => {
    if (recipe && Array.isArray(recipe.ingredients)) {
      recipe.ingredients.forEach(ingredient => {
        const key = `${ingredient.name}-${ingredient.unit}`.toLowerCase();
        if (ingredientMap.has(key)) {
          const existing = ingredientMap.get(key);
          existing.quantity += ingredient.quantity || 0;
        } else {
          ingredientMap.set(key, {
            name: ingredient.name,
            quantity: ingredient.quantity || 0,
            unit: ingredient.unit
          });
        }
      });
    }
  });

  return Array.from(ingredientMap.values());
};

/**
 * Calculate estimated cost for a shopping list
 * @param {Array} ingredients - Array of ingredients with quantities and unit prices
 * @returns {number} Total estimated cost
 */
export const calculateEstimatedCost = (ingredients) => {
  if (!Array.isArray(ingredients)) {
    return 0;
  }

  return ingredients.reduce((total, ingredient) => {
    const quantity = ingredient.quantity || 0;
    const unitPrice = ingredient.unitPrice || 0;
    return total + (quantity * unitPrice);
  }, 0);
}; 