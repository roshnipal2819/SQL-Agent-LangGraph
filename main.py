from manager import OrderManager

# Mock user configuration for testing
fake_config = {"configurable": {"current_user_id": 2}}


def process_user_query(question: str, config: dict):
    """
    Process user input for testing Manager functionality
    """
    current_user_id = int(config["configurable"]["current_user_id"])
    manager = OrderManager()

    if "create a new order" in question.lower():
        # Fetch food name from the question
        food_name = question.split("for")[-1].strip(".")
        result = manager.create_order(current_user_id, food_name)
        print("Result:", result["message"])

    elif "show me my orders" in question.lower():
        result = manager.get_orders_for_user(current_user_id)
        if result["success"]:
            print("Result:", result["query_result"])
        else:
            print("Error: Failed to fetch orders -", result["query_result"])

    elif "visualize query plan" in question.lower():
        print("Visualizing Query Plan for retrieving user's orders...")
        manager.execute_and_visualize(user_id=current_user_id)


if __name__ == "__main__":
    # Example user queries for testing application flow

    # Create a new order for Tiramisu
    user_question_1 = "Create a new order for tiramisu."
    process_user_query(user_question_1, config=fake_config)

    # Show all orders for the current user
    user_question_2 = "Show me my orders."
    process_user_query(user_question_2, config=fake_config)

    # Visualize the SQL query plan
    user_question_3 = "Visualize query plan."
    process_user_query(user_question_3, config=fake_config)


def app():
    return None