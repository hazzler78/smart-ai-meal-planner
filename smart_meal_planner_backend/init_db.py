from datetime import datetime, timedelta
from database import engine, Base, SessionLocal
from models import inventory, recipe, shopping_list

def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)

def seed_data():
    """Seed the database with sample data."""
    db = SessionLocal()
    try:
        # Add sample inventory items if none exist
        if not db.query(inventory.InventoryItem).first():
            sample_items = [
                inventory.InventoryItem(
                    name="Milk",
                    quantity=2,
                    unit="liters",
                    expiry_date=datetime.now() + timedelta(days=7)
                ),
                inventory.InventoryItem(
                    name="Eggs",
                    quantity=12,
                    unit="pieces",
                    expiry_date=datetime.now() + timedelta(days=14)
                ),
                inventory.InventoryItem(
                    name="Bread",
                    quantity=1,
                    unit="loaf",
                    expiry_date=datetime.now() + timedelta(days=5)
                )
            ]
            db.add_all(sample_items)

        # Add sample recipes if none exist
        if not db.query(recipe.Recipe).first():
            sample_recipe = recipe.Recipe(
                name="Simple Scrambled Eggs",
                description="A classic breakfast dish",
                ingredients=[
                    {"name": "Eggs", "quantity": 2, "unit": "pieces"},
                    {"name": "Milk", "quantity": 0.1, "unit": "liters"},
                    {"name": "Salt", "quantity": 1, "unit": "pinch"}
                ],
                instructions=[
                    "Beat eggs in a bowl",
                    "Add a splash of milk and salt",
                    "Cook in a pan over medium heat",
                    "Stir until cooked through"
                ],
                prep_time=10
            )
            db.add(sample_recipe)

        db.commit()
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Seeding database with sample data...")
    seed_data()
    print("Database initialization completed successfully!") 