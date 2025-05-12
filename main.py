import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import json

# ---------- TASK 1 ----------
def read_products(filename):
    products = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            product_list = data.get("products", [])
            for item in product_list:
                if isinstance(item, dict):
                    id = int(item.get("productID", 0))
                    name = item.get('name', '')
                    category = item.get('category', '')
                    price = float(item.get('price', 0))
                    products.append((id, name, category, price))
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print("Error reading products:", e)
    return products


def read_sales(filename):
    sales = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            category_list = data.get("sales",[])
            for item in category_list:
                if isinstance(item, dict):
                    name = item.get('productName','')
                    quantity = int(item.get('quantity', 0))
                    date = item.get('date', '')
                    sales.append((name, quantity, date))
                    # trqbva da se dobavi id za vsqka pokupka, za da moje da se vidi vuv vid na kasova belejka 
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print("Error reading products:", e)
    return sales


# ---------- TASK 2 ----------
def display_task_1_and_2(root):
    products = read_products("data/products.json")
    sales = read_sales("data/sales.json")


    # Create Toplevel window and position it beside the main window
    window = tk.Toplevel(root)
    window.title("Task 1 & 2: Display Products and Sales")
   
    # Position window beside the main window
    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()
    window.geometry(f"600x400+{x}+{y}")


    product_listbox = tk.Listbox(window, width=50, height=12)
    product_listbox.grid(row=0, column=0, padx=10, pady=10)


    sales_listbox = tk.Listbox(window, width=50, height=12)
    sales_listbox.grid(row=0, column=1, padx=10, pady=10)


    for product in products:
        product_listbox.insert(tk.END, f"ProductID: {product[0]}, Name: {product[1]}, Category: {product[2]}, Price: {product[3]}")


    for sale in sales:
        sales_listbox.insert(tk.END, f"Product: {sale[0]}, Quantity: {sale[1]}, Date: {sale[2]}")


    tk.Button(window, text="Close", command=window.destroy).grid(row=1, columnspan=2, pady=10)


# ---------- TASK 3 ----------
def summarize_sales(sales):
    summary = {}
    for name, quantity, _ in sales:
        if name in summary:
            summary[name] += quantity
        else:
            summary[name] = quantity
    return summary


def display_task_3(root):
    sales = read_sales("data/sales.json")
    summary = summarize_sales(sales)


    window = tk.Toplevel(root)
    window.title("Task 3: Summary of Sales")


    # Position window beside the main window
    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()
    window.geometry(f"600x400+{x}+{y}")


    listbox = tk.Listbox(window, width=50, height=15)
    listbox.pack(padx=10, pady=10)


    for product, total in summary.items():
        listbox.insert(tk.END, f"{product}: Total Sold = {total}")


    tk.Button(window, text="Close", command=window.destroy).pack(pady=5)


# ---------- TASK 4 ----------
def display_task_4(root):
    sales = read_sales("data/sales.json")
    summary = summarize_sales(sales)


    window = tk.Toplevel(root)
    window.title("Task 4: Search Product Sales")


    # Position window beside the main window
    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()
    window.geometry(f"600x400+{x}+{y}")


    tk.Label(window, text="Enter product name:").pack(pady=5)
    entry = tk.Entry(window, width=30)
    entry.pack(pady=5)


    result_label = tk.Label(window, text="", fg="blue")
    result_label.pack(pady=10)


    def search():
        product = entry.get().strip()
        if product in summary:
            result_label.config(text=f"{product} → Total Sold: {summary[product]}")
        else:
            result_label.config(text="Product not found.", fg="red")


    tk.Button(window, text="Search", command=search).pack(pady=5)
    tk.Button(window, text="Close", command=window.destroy).pack(pady=5)


# ---------- TASK 5 and 6 ----------
def filter_sales_by_quantity(sales, min_quantity=5):
    return [sale for sale in sales if sale[1] >= min_quantity]


def display_task_5(root):
    sales = read_sales("data/sales.json")

    def show_filtered():
        min_qty = int(spinbox.get())
        nonlocal filtered_sales
        filtered_sales = filter_sales_by_quantity(sales, min_qty)


        listbox.delete(0, tk.END)
        if filtered_sales:
            for sale in filtered_sales:
                listbox.insert(tk.END, f"{sale[0]} - {sale[1]} pcs on {sale[2]}")
        else:
            listbox.insert(tk.END, f"No sales with quantity ≥ {min_qty}.")


    def save_to_file():
        if not filtered_sales:
            messagebox.showinfo("No Data", "No filtered data to save. Please filter first.")
            return

        
        filename = "filtered_sales.json"
        with open(filename, "w", encoding="utf-8") as f:
            #trqbva da se convertne za da moje da se save-va kato json
            for sale in filtered_sales:
                f.write(f"{sale[0]},{sale[1]},{sale[2]}\n")
        messagebox.showinfo("Saved", f"Filtered sales saved to {filename}")


    filtered_sales = []


    window = tk.Toplevel(root)
    window.title("Task 5 & 6: Filter and Save Sales")


    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()
    window.geometry(f"600x400+{x}+{y}")


    tk.Label(window, text="Minimum Quantity:").pack(pady=(10, 0))
    spinbox = tk.Spinbox(window, from_=1, to=100, width=5)
    spinbox.pack(pady=5)


    listbox = tk.Listbox(window, width=50, height=15)
    listbox.pack(padx=10, pady=10)


    tk.Button(window, text="Show Filtered Sales", command=show_filtered).pack(pady=5)
    tk.Button(window, text="Save to File", command=save_to_file).pack(pady=5)
    tk.Button(window, text="Close", command=window.destroy).pack(pady=5)


# ---------- TASK 7 ----------
def display_task_7(root):
    sales = [("Apple", 20, "2025-05-01"), ("Banana", 30, "2025-05-02")]


    def add_sale():
        name = name_entry.get()
        quantity = quantity_entry.get()
        date = cal.get_date()


        if not name or not quantity or not date:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return


        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showwarning("Input Error", "Quantity must be a number.")
            return


        sales.append((name, quantity, date))


        with open("data/sales.json", "a", encoding="utf-8") as file:
            file.write(f"{name},{quantity},{date}\n")


        listbox.insert(tk.END, f"{name} - {quantity} pcs on {date}")
        name_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)


    window = tk.Toplevel(root)
    window.title("Task 7: Add New Sale")


    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()
    window.geometry(f"600x400+{x}+{y}")


    tk.Label(window, text="Product Name:").pack(pady=(10, 0))
    name_entry = tk.Entry(window, width=40)
    name_entry.pack(pady=5)


    tk.Label(window, text="Quantity:").pack(pady=(10, 0))
    quantity_entry = tk.Entry(window, width=40)
    quantity_entry.pack(pady=5)


    tk.Label(window, text="Select Date:").pack(pady=(10, 0))
    cal = Calendar(window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=5)


    tk.Button(window, text="Add Sale", command=add_sale).pack(pady=10)


    listbox = tk.Listbox(window, width=50, height=15)
    listbox.pack(padx=10, pady=10)


    for sale in sales:
        listbox.insert(tk.END, f"{sale[0]} - {sale[1]} pcs on {sale[2]}")


# ---------- MAIN MENU ----------
def main_menu():
    root = tk.Tk()
    root.title("Course Project Menu")


    tk.Label(root, text="Choose a Task to View:", font=("Arial", 14)).pack(pady=10)


    tk.Button(root, text="Task 1 & 2: Read and Display Data", width=40, command=lambda: display_task_1_and_2(root)).pack(pady=5)
    tk.Button(root, text="Task 3: Summary Dictionary", width=40, command=lambda: display_task_3(root)).pack(pady=5)
    tk.Button(root, text="Task 4: Search in Dictionary", width=40, command=lambda: display_task_4(root)).pack(pady=5)
    tk.Button(root, text="Task 5: Filter Sales by Quantity", width=40, command=lambda: display_task_5(root)).pack(pady=5)
    tk.Button(root, text="Task 7: Add New Sale", width=40, command=lambda: display_task_7(root)).pack(pady=5)


    root.mainloop()


if __name__ == "__main__":
    main_menu()
