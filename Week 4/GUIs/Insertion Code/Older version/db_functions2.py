import pyodbc

def connect_db():
    try:
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=DESKTOP-UTL48SK;'
            'Database=Feedback_Project1;'
            'Trusted_Connection=yes;'
        )
        print("Connection to the database was successful!")
        return conn
    except pyodbc.OperationalError as e:
        print("Error: Could not connect to the database.")
        print(e)

def insert_customer(conn, name, state):
    query = """
    INSERT INTO Customer (names, states)
    VALUES (?, ?);
    """
    cursor = conn.cursor()
    cursor.execute(query, (name, state))
    conn.commit()

def insert_store(conn, latitude, longitude, address):
    query = """
    INSERT INTO Store (latitude, longitude, addresses)
    VALUES (?, ?, ?);
    """
    cursor = conn.cursor()
    cursor.execute(query, (latitude, longitude, address))
    conn.commit()

def insert_product(conn, name, price):
    query = """
    INSERT INTO Product (names, price)
    VALUES (?, ?);
    """
    cursor = conn.cursor()
    cursor.execute(query, (name, price))
    conn.commit()

def insert_order(conn, date, customer_id, store_address):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Customer WHERE id = ?", (customer_id,))
    if cursor.fetchone() is None:
        print(f"Customer ID {customer_id} does not exist.")
        return
    cursor.execute("SELECT id FROM Store WHERE addresses = ?", (store_address,))
    store_row = cursor.fetchone()
    if store_row is None:
        print(f"Store address '{store_address}' does not exist.")
        return
    store_id = store_row[0]

    query = """
    INSERT INTO Orders (dates, customer_id, store_id)
    VALUES (?, ?, ?);
    """
    cursor.execute(query, (date, customer_id, store_id))
    conn.commit()

def insert_order_details(conn, order_id, product_id, quantity):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Orders WHERE id = ?", (order_id,))
    if cursor.fetchone() is None:
        print(f"Order ID {order_id} does not exist.")
        return
    cursor.execute("SELECT id FROM Product WHERE id = ?", (product_id,))
    if cursor.fetchone() is None:
        print(f"Product ID {product_id} does not exist.")
        return

    query = """
    INSERT INTO OrderDetails (order_id, product_id, quantity)
    VALUES (?, ?, ?);
    """
    cursor.execute(query, (order_id, product_id, quantity))
    conn.commit()

def insert_feedback(conn, customer_id, store_id, order_id, review, rating):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Orders WHERE id = ? AND customer_id = ? AND store_id = ?", 
                   (order_id, customer_id, store_id))
    if cursor.fetchone() is None:
        print(f"Order ID {order_id} does not match with customer ID {customer_id} and store ID {store_id}.")
        return

    query = """
    INSERT INTO Feedback (customer_id, store_id, order_id, review, rating)
    VALUES (?, ?, ?, ?, ?);
    """
    cursor.execute(query, (customer_id, store_id, order_id, review, rating))
    conn.commit()

def get_orders_without_feedback(conn):
    cursor = conn.cursor()
    query = """
    SELECT o.id FROM Orders o
    LEFT JOIN Feedback f ON o.id = f.order_id
    WHERE f.id IS NULL;
    """
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def get_orders_id(conn):
    cursor = conn.cursor()
    query = """
    SELECT o.id FROM Orders o;
    """
    cursor.execute(query)
    orders = cursor.fetchall()
    print("Orders fetched!")
    return orders

def get_customers(conn):
    cursor = conn.cursor()
    query = "SELECT id, names FROM Customer"
    cursor.execute(query)
    return cursor.fetchall()

def get_stores(conn):
    cursor = conn.cursor()
    query = "SELECT id, addresses FROM Store"
    cursor.execute(query)
    return cursor.fetchall()

def get_products(conn):
    cursor = conn.cursor()
    query = "SELECT id, names FROM Product"
    cursor.execute(query)
    return cursor.fetchall()

def get_order_details(conn, order_id):
    cursor = conn.cursor()
    query = """
    SELECT p.names, od.quantity
    FROM OrderDetails od
    JOIN Product p ON od.product_id = p.id
    WHERE od.order_id = ?;
    """
    cursor.execute(query, (order_id,))
    order_details = cursor.fetchall()
    return order_details
