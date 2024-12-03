import { calculateTotalCalories, formatCookingTime } from '../utils/recipeUtils';

describe('calculateTotalCalories', () => {
  test('should return 0 for null or undefined recipe', () => {
    expect(calculateTotalCalories(null)).toBe(0);
    expect(calculateTotalCalories(undefined)).toBe(0);
  });

  test('should return 0 for recipe without ingredients', () => {
    expect(calculateTotalCalories({})).toBe(0);
  });

  test('should calculate total calories correctly', () => {
    const recipe = {
      ingredients: [
        { name: 'Sugar', calories: 100 },
        { name: 'Flour', calories: 150 },
        { name: 'Butter', calories: 200 }
      ]
    };
    expect(calculateTotalCalories(recipe)).toBe(450);
  });

  test('should handle ingredients without calories', () => {
    const recipe = {
      ingredients: [
        { name: 'Sugar', calories: 100 },
        { name: 'Salt' },
        { name: 'Butter', calories: 200 }
      ]
    };
    expect(calculateTotalCalories(recipe)).toBe(300);
  });
});

describe('formatCookingTime', () => {
  test('should handle invalid inputs', () => {
    expect(formatCookingTime(null)).toBe('0 minutes');
    expect(formatCookingTime(undefined)).toBe('0 minutes');
    expect(formatCookingTime(-5)).toBe('0 minutes');
  });

  test('should format minutes only', () => {
    expect(formatCookingTime(30)).toBe('30 minutes');
    expect(formatCookingTime(45)).toBe('45 minutes');
  });

  test('should format hours only', () => {
    expect(formatCookingTime(60)).toBe('1 hour');
    expect(formatCookingTime(120)).toBe('2 hours');
  });

  test('should format hours and minutes', () => {
    expect(formatCookingTime(90)).toBe('1 hour 30 minutes');
    expect(formatCookingTime(150)).toBe('2 hours 30 minutes');
  });
}); 