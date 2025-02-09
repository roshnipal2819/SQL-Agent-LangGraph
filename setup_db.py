import random
from models import Base, engine, SessionLocal, User, Food, Order


def init_db():
    """
    Initialize and populate the database with sample data.
    """
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    try:
        # Users
        users = [
            {"name": "Alice", "age": 30, "email": "alice@example.com"},
            {"name": "Bob", "age": 25, "email": "bob@example.com"},
            {"name": "Charlie", "age": 35, "email": "charlie@example.com"},
        ]

        for user_data in users:
            # Check if the user already exists in the database
            existing_user = session.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                new_user = User(name=user_data["name"], age=user_data["age"], email=user_data["email"])
                session.add(new_user)

        # Foods
        foods = [
            {"name": "Pizza Margherita", "price": 12.5},
            {"name": "Spaghetti Carbonara", "price": 15.0},
            {"name": "Lasagne", "price": 14.0},
            {"name": "Tiramisu", "price": 6.5},
        ]

        for food_data in foods:
            # Check if the food item already exists in the database
            existing_food = session.query(Food).filter(Food.name == food_data["name"]).first()
            if not existing_food:
                new_food = Food(name=food_data["name"], price=food_data["price"])
                session.add(new_food)

        # Orders (randomized)
        orders = [
            Order(food_id=random.randint(1, 4), user_id=random.randint(1, 3))
            for _ in range(5)
        ]
        session.add_all(orders)

        session.commit()
        print("Database successfully initialized with sample data.")

    except Exception as e:
        session.rollback()
        print(f"Error initializing database: {e}")

    finally:
        session.close()


if __name__ == "__main__":
    init_db()
