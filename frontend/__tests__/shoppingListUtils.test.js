import { combineIngredients, calculateEstimatedCost } from '../utils/shoppingListUtils';

describe('combineIngredients', () => {
  test('should return empty array for invalid input', () => {
    expect(combineIngredients(null)).toEqual([]);
    expect(combineIngredients(undefined)).toEqual([]);
    expect(combineIngredients({})).toEqual([]);
  });

  test('should combine ingredients from multiple recipes', () => {
    const recipes = [
      {
        ingredients: [
          { name: 'Flour', quantity: 2, unit: 'cups' },
          { name: 'Sugar', quantity: 1, unit: 'cup' }
        ]
      },
      {
        ingredients: [
          { name: 'Flour', quantity: 1.5, unit: 'cups' },
          { name: 'Butter', quantity: 0.5, unit: 'cup' }
        ]
      }
    ];

    const result = combineIngredients(recipes);
    expect(result).toEqual(expect.arrayContaining([
      { name: 'Flour', quantity: 3.5, unit: 'cups' },
      { name: 'Sugar', quantity: 1, unit: 'cup' },
      { name: 'Butter', quantity: 0.5, unit: 'cup' }
    ]));
    expect(result).toHaveLength(3);
  });

  test('should handle recipes without ingredients', () => {
    const recipes = [
      { name: 'Recipe 1' },
      {
        ingredients: [
          { name: 'Sugar', quantity: 1, unit: 'cup' }
        ]
      }
    ];

    const result = combineIngredients(recipes);
    expect(result).toEqual([
      { name: 'Sugar', quantity: 1, unit: 'cup' }
    ]);
  });

  test('should handle ingredients without quantities', () => {
    const recipes = [
      {
        ingredients: [
          { name: 'Salt', unit: 'tsp' },
          { name: 'Pepper', quantity: 0.5, unit: 'tsp' }
        ]
      }
    ];

    const result = combineIngredients(recipes);
    expect(result).toEqual(expect.arrayContaining([
      { name: 'Salt', quantity: 0, unit: 'tsp' },
      { name: 'Pepper', quantity: 0.5, unit: 'tsp' }
    ]));
  });
});

describe('calculateEstimatedCost', () => {
  test('should return 0 for invalid input', () => {
    expect(calculateEstimatedCost(null)).toBe(0);
    expect(calculateEstimatedCost(undefined)).toBe(0);
    expect(calculateEstimatedCost({})).toBe(0);
  });

  test('should calculate total cost correctly', () => {
    const ingredients = [
      { name: 'Flour', quantity: 2, unitPrice: 0.5 },
      { name: 'Sugar', quantity: 1, unitPrice: 0.75 },
      { name: 'Butter', quantity: 0.5, unitPrice: 3.00 }
    ];

    expect(calculateEstimatedCost(ingredients)).toBe(2.75); // (2 * 0.5) + (1 * 0.75) + (0.5 * 3.00)
  });

  test('should handle ingredients without prices or quantities', () => {
    const ingredients = [
      { name: 'Flour', quantity: 2 },
      { name: 'Sugar', unitPrice: 0.75 },
      { name: 'Salt' }
    ];

    expect(calculateEstimatedCost(ingredients)).toBe(0);
  });
}); 