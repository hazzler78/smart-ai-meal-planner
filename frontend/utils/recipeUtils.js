/**
 * Calculate total calories for a recipe
 * @param {Object} recipe - Recipe object with ingredients array
 * @returns {number} Total calories
 */
export const calculateTotalCalories = (recipe) => {
  if (!recipe || !recipe.ingredients) {
    return 0;
  }
  return recipe.ingredients.reduce((total, ingredient) => {
    return total + (ingredient.calories || 0);
  }, 0);
};

/**
 * Format cooking time to human readable string
 * @param {number} minutes - Cooking time in minutes
 * @returns {string} Formatted time string
 */
export const formatCookingTime = (minutes) => {
  if (!minutes || minutes < 0) {
    return '0 minutes';
  }
  
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  
  if (hours === 0) {
    return `${minutes} minutes`;
  }
  
  if (remainingMinutes === 0) {
    return `${hours} hour${hours > 1 ? 's' : ''}`;
  }
  
  return `${hours} hour${hours > 1 ? 's' : ''} ${remainingMinutes} minutes`;
}; 