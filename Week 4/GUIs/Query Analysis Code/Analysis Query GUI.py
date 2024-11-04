import pyodbc
from tkinter import *
from tkinter import ttk, messagebox

# Connect to SQL Server
def connect_to_database():
    try:
        conn = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            'Server=DESKTOP-UTL48SK;'
            'Database=Feedback_Project1;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))
        return None

# Fetch the data based on the query selected by the user
def run_query(query):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]  # Get column names
            return columns, rows
        except Exception as e:
            messagebox.showerror("Query Error", str(e))
        finally:
            conn.close()
    return None, None

# Format complex or tuple data to strings for Treeview
def format_value(value):
    if isinstance(value, (list, tuple)):
        return ", ".join(map(str, value))
    return str(value)

# For Clearing treeview
def update_treeview(columns, rows):
    for row in tree.get_children():
        tree.delete(row)

    tree["columns"] = columns
    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, anchor="center")

    for row in rows:
        formatted_row = [format_value(cell) for cell in row]
        tree.insert("", "end", values=formatted_row)

# Update result display
def display_results():
    query_name = query_selection.get()
    if query_name in QUERIES:
        query = QUERIES[query_name]
        columns, rows = run_query(query)
        if columns and rows:
            update_treeview(columns, rows)
        else:
            messagebox.showinfo("No Results", "No data returned or query error.")

# the queries
QUERIES = {
    "Total Number of Feedback Entries": "SELECT COUNT(*) AS total_feedback FROM Feedback;",
    "Average Rating by Store": """
        SELECT s.id AS store_id, s.addresses, AVG(f.rating) AS average_rating
        FROM Feedback f
        JOIN Store s ON f.store_id = s.id
        GROUP BY s.id, s.addresses
        ORDER BY average_rating DESC;
    """,
    "Total Feedback Count by Store": """
        SELECT s.id AS store_id, s.addresses, COUNT(f.id) AS feedback_count
        FROM Feedback f
        JOIN Store s ON f.store_id = s.id
        GROUP BY s.id, s.addresses
        ORDER BY feedback_count DESC;
    """,
    "Rating of Each Customer": """
        SELECT c.id AS customer_id, c.names, f.rating AS rating
        FROM Feedback f
        JOIN Customer c ON f.customer_id = c.id
        ORDER BY rating DESC;
    """,
    "Monthly Feedback Count Over Time": """
        SELECT YEAR(dates) AS year, MONTH(dates) AS month, COUNT(*) AS feedback_count
        FROM Orders o
        JOIN Feedback f ON o.id = f.order_id
        GROUP BY YEAR(dates), MONTH(dates)
        ORDER BY year, month;
    """,
    "Average Rating Over Time": """
        SELECT YEAR(dates) AS year, MONTH(dates) AS month, AVG(f.rating) AS average_rating
        FROM Orders o
        JOIN Feedback f ON o.id = f.order_id
        GROUP BY YEAR(dates), MONTH(dates)
        ORDER BY year, month;
    """,
    "Feedback Distribution by Rating": """
        SELECT rating, COUNT(*) AS count
        FROM Feedback
        GROUP BY rating
        ORDER BY rating;
    """,
    "Top Products by Average Rating": """
        SELECT p.id AS product_id, p.names, AVG(f.rating) AS average_rating
        FROM OrderDetails od
        JOIN Feedback f ON od.order_id = f.order_id
        JOIN Product p ON od.product_id = p.id
        GROUP BY p.id, p.names
        ORDER BY average_rating DESC;
    """,
    "Feedback Sentiment Analysis": """
        SELECT 
            CASE 
                WHEN review LIKE '%good%' THEN 'Positive'
                WHEN review LIKE '%bad%' THEN 'Negative'
                ELSE 'Neutral'
            END AS sentiment,
            COUNT(*) AS count
        FROM Feedback
        GROUP BY 
            CASE 
                WHEN review LIKE '%good%' THEN 'Positive'
                WHEN review LIKE '%bad%' THEN 'Negative'
                ELSE 'Neutral'
            END;
    """,
    "Average Rating for All Customers": """
        SELECT AVG(f.rating) AS overall_average_rating
        FROM Feedback f;
    """,
    "Store Performance Comparison": """
        SELECT s.id AS store_id, s.addresses, AVG(f.rating) AS average_rating, COUNT(f.id) AS feedback_count
        FROM Feedback f
        JOIN Store s ON f.store_id = s.id
        GROUP BY s.id, s.addresses
        ORDER BY average_rating DESC, feedback_count DESC;
    """,
    "Detailed Feedback Entries for a Specific Store": """
        SELECT f.review, f.rating, c.names
        FROM Feedback f
        JOIN Customer c ON f.customer_id = c.id
        WHERE f.store_id = 1;  -- Replace 1 with the desired store_ID
    """,
    "Feedback with Ratings Lower than Average": """
        SELECT f.review, f.rating, s.addresses
        FROM Feedback f
        JOIN Store s ON f.store_id = s.id
        WHERE f.rating < (
            SELECT AVG(rating) FROM Feedback
        );
    """,
    "Feedback with Ratings Higher than Average": """
        SELECT f.review, f.rating, s.addresses
        FROM Feedback f
        JOIN Store s ON f.store_id = s.id
        WHERE f.rating > (
            SELECT AVG(rating) FROM Feedback
        );
    """,
        "Combine Feedback and Total Order Amount": """
        SELECT 
            F.id AS feedback_id,
            F.review,
            F.rating,
            TOA.total_price,
            St.addresses AS store_address,
            C.names AS customer_name
        FROM 
            Feedback F
        JOIN 
            Orders O ON F.order_id = O.id
        JOIN 
            Store St ON O.store_id = St.id
        JOIN 
            Customer C ON F.customer_id = C.id
        JOIN 
            (SELECT 
                O.id AS order_id,
                SUM(P.price * OD.quantity) AS total_price
             FROM 
                Orders O
             JOIN 
                OrderDetails OD ON O.id = OD.order_id
             JOIN 
                Product P ON OD.product_id = P.id
             GROUP BY 
                O.id) TOA ON F.order_id = TOA.order_id;
    """,
}

# Create the GUI
root = Tk()
root.title("Feedback Project Analysis")
query_label = Label(root, text="Select Analysis:")
query_label.pack(pady=10)
query_selection = StringVar(root)
query_selection.set("Average Rating Over Time")
query_dropdown = OptionMenu(root, query_selection, *QUERIES.keys())
query_dropdown.pack(pady=10)
run_button = Button(root, text="Run Analysis", command=display_results)
run_button.pack(pady=10)

# Create a frame for the Treeview and scrollbar
frame = Frame(root)
frame.pack(padx=60, pady=60)
tree = ttk.Treeview(frame, show="headings")
tree.pack(side='left')
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side='right', fill='y')
tree.configure(yscroll=scrollbar.set)
root.mainloop()