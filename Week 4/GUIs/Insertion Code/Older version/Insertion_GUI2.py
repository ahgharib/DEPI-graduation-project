import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys
import os

sys.path.append(os.path.abspath("C:/programing/DEPI/python and database"))
from db_functions2 import *

root = tk.Tk()
root.title("Insert Data")
conn = connect_db()

def open_insert_customer():
    customer_window = tk.Toplevel(root)
    customer_window.title("Insert Customer")

    tk.Label(customer_window, text="Customer Name:").pack()
    customer_name_entry = tk.Entry(customer_window)
    customer_name_entry.pack()

    tk.Label(customer_window, text="Customer State:").pack()
    customer_state_entry = tk.Entry(customer_window)
    customer_state_entry.pack()

    def handle_insert_customer():
        name = customer_name_entry.get()
        state = customer_state_entry.get()
        insert_customer(conn, name, state)
        messagebox.showinfo("Success", "Customer added successfully!")
        customer_window.destroy()

    tk.Button(customer_window, text="Insert Customer", command=handle_insert_customer).pack()

def open_insert_store():
    store_window = tk.Toplevel(root)
    store_window.title("Insert Store")

    tk.Label(store_window, text="Store Address:").pack()
    store_address_entry = tk.Entry(store_window)
    store_address_entry.pack()

    tk.Label(store_window, text="Latitude:").pack()
    latitude_entry = tk.Entry(store_window)
    latitude_entry.pack()

    tk.Label(store_window, text="Longitude:").pack()
    longitude_entry = tk.Entry(store_window)
    longitude_entry.pack()

    def handle_insert_store():
        address = store_address_entry.get()
        latitude = float(latitude_entry.get())
        longitude = float(longitude_entry.get())
        insert_store(conn, latitude, longitude, address)
        messagebox.showinfo("Success", "Store added successfully!")
        store_window.destroy()

    tk.Button(store_window, text="Insert Store", command=handle_insert_store).pack()

def open_insert_product():
    product_window = tk.Toplevel(root)
    product_window.title("Insert Product")

    tk.Label(product_window, text="Product Name:").pack()
    product_name_entry = tk.Entry(product_window)
    product_name_entry.pack()

    tk.Label(product_window, text="Product Price:").pack()
    product_price_entry = tk.Entry(product_window)
    product_price_entry.pack()

    def handle_insert_product():
        name = product_name_entry.get()
        price = float(product_price_entry.get())
        insert_product(conn, name, price)
        messagebox.showinfo("Success", "Product added successfully!")
        product_window.destroy()

    tk.Button(product_window, text="Insert Product", command=handle_insert_product).pack()

def open_insert_order():
    order_window = tk.Toplevel(root)
    order_window.title("Insert Order")

    tk.Label(order_window, text="Order Date (YYYY-MM-DD):").pack()
    order_date_entry = tk.Entry(order_window)
    order_date_entry.pack()

    tk.Label(order_window, text="Customer ID:").pack()
    customer_id_entry = tk.Entry(order_window)
    customer_id_entry.pack()

    tk.Label(order_window, text="Store Address:").pack()
    store_combo = ttk.Combobox(order_window, width=75)
    store_combo.pack()

    stores = get_stores(conn)
    store_addresses = [address for _, address in stores]
    store_combo['values'] = store_addresses
    store_combo.current(0)

    def handle_insert_order():
        order_date = order_date_entry.get()
        customer_id = int(customer_id_entry.get())
        selected_store_address = store_combo.get()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Store WHERE addresses = ?", (selected_store_address,))
        store_id = cursor.fetchone()[0]
        insert_order(conn, order_date, customer_id, selected_store_address)
        messagebox.showinfo("Success", "Order added successfully!")
        order_window.destroy()

    tk.Button(order_window, text="Insert Order", command=handle_insert_order).pack()

def update_order_details(event, order_combo, order_details_text):
    selected_order_id = order_combo.get()
    if selected_order_id:
        try:
            order_id = int(selected_order_id)
            order_details = get_order_details(conn, order_id)
            order_details_text.delete(1.0, tk.END)
            if order_details:
                for product, quantity in order_details:
                    order_details_text.insert(tk.END, f"Product: {product}, Quantity: {quantity}\n")
            else:
                order_details_text.insert(tk.END, "No details available for this order.\n")
        except ValueError:
            order_details_text.delete(1.0, tk.END)
            order_details_text.insert(tk.END, "Invalid order ID.\n")

def open_insert_order_details():
    order_details_window = tk.Toplevel(root)
    order_details_window.title("Insert Order Details")

    tk.Label(order_details_window, text="Order ID:").pack()

    order_combo = ttk.Combobox(order_details_window, width=30)
    order_combo.pack()

    orders = get_orders_id(conn)
    order_ids = [str(order[0]) for order in orders]
    if order_ids:
        order_combo['values'] = order_ids
        order_combo.current(0)
    else:
        order_combo.set("No orders available")

    tk.Label(order_details_window, text="Order Details:").pack()
    order_details_text = tk.Text(order_details_window, width=40, height=10)
    order_details_text.pack()

    order_combo.bind("<<ComboboxSelected>>", lambda event: update_order_details(event, order_combo, order_details_text))

    tk.Label(order_details_window, text="Product Name:").pack()
    product_id_combo = ttk.Combobox(order_details_window, width=30)
    product_id_combo.pack()

    products = get_products(conn)
    product_names = [product[1] for product in products]
    product_id_combo['values'] = product_names
    product_id_combo.current(0)

    tk.Label(order_details_window, text="Quantity:").pack()
    quantity_entry = tk.Entry(order_details_window)
    quantity_entry.pack()

    def handle_insert_order_details():
        order_id = int(order_combo.get())
        selected_product_name = product_id_combo.get()
        product_id = next((pid for pid, name in products if name == selected_product_name), None)

        if not product_id:
            messagebox.showerror("Error", "Selected product not found!")
            return
        
        quantity = int(quantity_entry.get())
        insert_order_details(conn, order_id, product_id, quantity)
        messagebox.showinfo("Success", "Order details added successfully!")
        order_details_window.destroy()

    tk.Button(order_details_window, text="Insert Order Details", command=handle_insert_order_details).pack()

def open_insert_feedback():
    feedback_window = tk.Toplevel(root)
    feedback_window.title("Insert Feedback")

    tk.Label(feedback_window, text="Customer ID:").pack()
    feedback_customer_id_entry = tk.Entry(feedback_window)
    feedback_customer_id_entry.pack()

    tk.Label(feedback_window, text="Store Address:").pack()
    store_address_combo = ttk.Combobox(feedback_window, width=30)
    store_address_combo.pack()

    tk.Label(feedback_window, text="Order ID:").pack()
    order_id_combo = ttk.Combobox(feedback_window, width=30)
    order_id_combo.pack()

    tk.Label(feedback_window, text="Review:").pack()
    feedback_review_entry = tk.Entry(feedback_window)
    feedback_review_entry.pack()

    tk.Label(feedback_window, text="Rating (1-5):").pack()
    feedback_rating_entry = tk.Entry(feedback_window)
    feedback_rating_entry.pack()

    feedback_status_label = tk.Label(feedback_window, text="", fg="red")
    feedback_status_label.pack()

    submit_button = tk.Button(feedback_window, text="Insert Feedback")
    submit_button.pack()

    stores = []

    def update_store_addresses(event):
        nonlocal stores
        customer_id = feedback_customer_id_entry.get()
        store_address_combo.set('')
        store_address_combo['values'] = []
        order_id_combo.set('')
        order_id_combo['values'] = []

        if not customer_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid Customer ID.")
            return

        stores = get_stores_for_customer(conn, customer_id)
        if stores:
            store_address_combo['values'] = [store[1] for store in stores]
            store_address_combo.current(0)
        else:
            store_address_combo.set("No stores available")

    def update_order_ids(event):
        customer_id = feedback_customer_id_entry.get()
        selected_store_address = store_address_combo.get()
        store_id = next((store[0] for store in stores if store[1] == selected_store_address), None)

        if store_id:
            orders = get_orders_for_customer_and_store(conn, customer_id, store_id)
            if orders:
                order_id_combo['values'] = [order[0] for order in orders]
                order_id_combo.current(0)
            else:
                order_id_combo.set("No orders available")
            
            order_id_combo.bind("<<ComboboxSelected>>", check_feedback_status)

    def check_feedback_status(event):
        selected_order_id = int(order_id_combo.get())
        if feedback_exists(conn, selected_order_id):
            feedback_status_label.config(text="Feedback already exists for this order.")
            submit_button.config(state="disabled")
        else:
            feedback_status_label.config(text="")
            submit_button.config(state="normal")

    feedback_customer_id_entry.bind("<FocusOut>", update_store_addresses)
    store_address_combo.bind("<<ComboboxSelected>>", update_order_ids)

    def handle_insert_feedback():
        customer_id = int(feedback_customer_id_entry.get())
        selected_store_address = store_address_combo.get()
        store_id = next((store[0] for store in stores if store[1] == selected_store_address), None)
        order_id = int(order_id_combo.get())
        review = feedback_review_entry.get()
        rating = int(feedback_rating_entry.get())

        if store_id is None or order_id is None:
            messagebox.showerror("Error", "Invalid store or order selection!")
            return

        insert_feedback(conn, customer_id, store_id, order_id, review, rating)
        messagebox.showinfo("Success", "Feedback added successfully!")
        feedback_window.destroy()

    submit_button.config(command=handle_insert_feedback)

def feedback_exists(conn, order_id):
    cursor = conn.cursor()
    query = """
    SELECT COUNT(*)
    FROM Feedback f
    WHERE f.order_id = ?;
    """
    cursor.execute(query, (order_id,))
    count = cursor.fetchone()[0]
    return count > 0

def get_stores_for_customer(conn, customer_id):
    cursor = conn.cursor()
    query = """
    SELECT DISTINCT s.id, s.addresses 
    FROM Orders o
    JOIN Store s ON o.store_id = s.id
    WHERE o.customer_id = ?;
    """
    cursor.execute(query, (customer_id,))
    return cursor.fetchall()

def get_orders_for_customer_and_store(conn, customer_id, store_id):
    cursor = conn.cursor()
    query = """
    SELECT o.id
    FROM Orders o
    WHERE o.customer_id = ? AND o.store_id = ?;
    """
    cursor.execute(query, (customer_id, store_id))
    return cursor.fetchall()

tk.Label(root, text="Insert into Customer Table").pack()
tk.Button(root, text="Insert Customer", command=open_insert_customer).pack()

tk.Label(root, text="Insert into Store Table").pack()
tk.Button(root, text="Insert Store", command=open_insert_store).pack()

tk.Label(root, text="Insert into Product Table").pack()
tk.Button(root, text="Insert Product", command=open_insert_product).pack()

tk.Label(root, text="Insert into Order Table").pack()
tk.Button(root, text="Insert Order", command=open_insert_order).pack()

tk.Label(root, text="Insert into Order Details Table").pack()
tk.Button(root, text="Insert Order Details", command=open_insert_order_details).pack()

tk.Label(root, text="Insert into Feedback Table").pack()
tk.Button(root, text="Insert Feedback", command=open_insert_feedback).pack()

root.mainloop()
conn.close()