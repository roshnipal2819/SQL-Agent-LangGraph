# Project Title

This project provides an interface for a restaurant order system developed in Python 3.12.8, using SQLAlchemy ORM and SQLite as the database. The system is composed of three key tables - Users, Food, and Orders. 

## Setup & Installation

1. Install Python 3.12.8 and necessary packages. 

2. Set up environmental variables in a `.env` file, specifying the `DATABASE_URL`.

3. Clone or download the repository.

## Usage

Open the `sql.ipynb` file in Jupyter Notebook and run it:

```shell
jupyter notebook sql.ipynb
```

## Database Schema

The database includes:

1. **Users**: Holds user data and a relationship with the Orders table.
2. **Food**: Represents food items and carries a relationship with the Orders table.
3. **Orders**: Contains order details and has relationships with the Users and Food tables.

## Features

- Interaction: Users can make requests, e.g., placing an order for a food item.
- Visualization: Users can visualize their orders within Jupyter Notebook.
- Order History: Users can retrieve and view their past orders.
