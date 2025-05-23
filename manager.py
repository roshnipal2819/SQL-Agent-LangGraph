from sqlalchemy.orm import Query
from sqlalchemy import text
from models import SessionLocal, Food, Order
from graphviz import Digraph


class OrderManager:
    """
    Handles order-related operations and query visualization.
    """

    def __init__(self):
        self.session = SessionLocal()

    def _generate_query_plan(self, sql_query: Query):
        """
        Generate the query plan for a given SQLAlchemy Query object using EXPLAIN.
        """
        try:
            # Compile the query into raw SQL
            compiled_query = str(sql_query.statement.compile(compile_kwargs={"literal_binds": True}))
            print("Compiled Query:")
            print(compiled_query)

            # Execute EXPLAIN Statement for Query Plan
            explain_command = f"EXPLAIN {compiled_query}"
            query_plan = self.session.execute(text(explain_command)).fetchall()

            return query_plan
        except Exception as e:
            print(f"Error generating query plan: {e}")
            return []

    def _generate_query_plan_graph(self, query_plan):
        """
        Visualize a query plan using Graphviz and save it as an image.
        """
        try:
            graph = Digraph(format="png", engine="dot")
            graph.attr(rankdir="TB", fontsize="10")

            # Add nodes and edges for query plan
            for idx, plan in enumerate(query_plan):
                graph.node(str(idx), plan[0])

                # Create edges (linked sequentially)
                if idx > 0:  # Link sequentially
                    graph.edge(str(idx - 1), str(idx))

            # Render graph to an image file
            image_name = "query_plan"
            graph.render(image_name, cleanup=True)
            print(f"Query plan graph saved as: {image_name}.png")
            return f"{image_name}.png"
        except Exception as e:
            print(f"Error generating query plan graph: {e}")

    def _print_query(self, query: Query):
        """
        Helper to print the SQL generated by a Query object.
        """
        if query is None:
            return

        print("Executing SQL Query:")
        print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))

    def execute_and_visualize(self, user_id: int):
        """
        Visualize query execution plans for the Get Orders Query.
        """
        try:
            query = (
                self.session.query(Order)
                .join(Food, Food.id == Order.food_id)
                .filter(Order.user_id == user_id)
            )

            self._print_query(query)
            # Generate and visualize the query plan
            query_plan = self._generate_query_plan(query)

            if not query_plan:
                print("No query plan generated.")
                return

            # self._generate_query_plan_graph(query_plan)

        except Exception as e:
            print(f"Error executing query: {e}")

    def get_orders_for_user(self, user_id: int):
        """
        Retrieve orders for the user and structure output exactly as in the notebook.
        """
        try:
            query = (
                self.session.query(Order)
                .join(Food, Food.id == Order.food_id)
                .filter(Order.user_id == user_id)
            )
            orders = query.all()

            if not orders:
                return {"success": True, "query_result": "No orders found for the user."}

            # Structure orders for output (as seen in the notebook)
            raw_order_results = [
                {"food_name": order.food.name, "price": order.food.price}
                for order in orders
            ]

            # Generate a human-readable answer
            human_readable_answer = self.generate_human_readable_orders("Bob", raw_order_results)

            return {"success": True, "query_result": human_readable_answer}

        except Exception as e:
            return {"success": False, "query_result": str(e)}
        finally:
            self.session.close()

    def generate_human_readable_orders(self, user_name: str, orders: list) -> str:
        """
        Generates a human-readable answer for the user's orders.

        Args:
            user_name (str): The name of the user requesting order information.
            orders (list): A list of orders where each order contains 'food_name' and 'price'.

        Returns:
            str: A conversational, human-readable summary of the orders.
        """
        # If no orders exist
        if not orders:
            return f"Hello {user_name}, you don’t have any orders yet. Why not try something from our menu?"

        # Process the results to summarize repeated food items
        order_summary = {}
        for order in orders:
            food_name = order["food_name"]
            price = order["price"]
            if food_name not in order_summary:
                # Add food if not already in the summary
                order_summary[food_name] = {"count": 1, "price": price}
            else:
                # Increment the count if it already exists
                order_summary[food_name]["count"] += 1

        # Build the human-readable response
        human_readable_lines = []
        for food, data in order_summary.items():
            # Add quantity if there are multiple orders for the same item
            if data["count"] > 1:
                human_readable_lines.append(f"{data['count']}x {food} for ${data['price']:.2f} each")
            else:
                human_readable_lines.append(f"{food} for ${data['price']:.2f}")

        # Join all items with proper formatting
        order_list = ", ".join(human_readable_lines[:-1]) + f", and {human_readable_lines[-1]}" if len(
            human_readable_lines) > 1 else human_readable_lines[0]

        # Final conversational response
        return f"Hello {user_name}, you have ordered {order_list}! Thank you for dining with us. 😊"

    def create_order(self, user_id: int, food_name: str):
        """
        Create a new order for a user using a given food item's name.
        """
        try:
            food_query = self.session.query(Food).filter(Food.name == food_name)
            self._print_query(food_query)

            food = food_query.first()
            if not food:
                return {"success": False, "message": "Food not found."}

            new_order = Order(user_id=user_id, food_id=food.id)
            self.session.add(new_order)
            self.session.commit()
            return {"success": True, "message": "Order created successfully."}
        except Exception as e:
            self.session.rollback()
            return {"success": False, "message": f"Error: {e}"}
        finally:
            self.session.close()
