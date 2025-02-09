from models import SessionLocal, User, Food

session = SessionLocal()

# Add sample users
users = [
    {"name": "Alice", "age": 25, "email": "alice@example.com"},
    {"name": "Bob", "age": 30, "email": "bob@example.com"},
]

for user_data in users:
    # Check if the user already exists in the database
    existing_user = session.query(User).filter(User.email == user_data["email"]).first()
    if not existing_user:
        new_user = User(name=user_data["name"], age=user_data["age"], email=user_data["email"])
        session.add(new_user)

# Add sample food items
foods = [
    {"name": "tiramisu", "price": 6.5},
    {"name": "spaghetti", "price": 12.0},
]

for food_data in foods:
    # Check if the food item already exists in the database
    existing_food = session.query(Food).filter(Food.name == food_data["name"]).first()
    if not existing_food:
        new_food = Food(name=food_data["name"], price=food_data["price"])
        session.add(new_food)

# Commit database session
session.commit()
print("Database populated or updated!")
