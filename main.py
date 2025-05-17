import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
import json
import os

class Table:
    def __init__(self, root):
        for i in range(total_rows):
            for j in range(total_columns):
                if i == 0:
                    # Header row style
                    self.e = Entry(root, width=20, fg='white',
                                   font=('Arial', 11, 'bold'),
                                   bg='darkblue', justify='center')
                else:
                    # Regular data row style
                    self.e = Entry(root, width=20, fg='black',
                                   font=('Arial', 11, 'normal'),
                                   justify='center')

                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])

def format_display_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%d.%m.%Y") 
    except ValueError:
        return date_str  # in case it’s already formatted or invalid
 
# Am i in dzhan


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
                    price = round(float(item.get('price', 0)), 2)

                    products.append((id, name, category, format(price, '.2f')))
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
                    id = item.get('saleID','')
                    sales.append((name, quantity, date, id))
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print("Error reading products:", e)
    return sales


# ---------- TASK 2 ----------
def product_list(root):
    products = read_products("data/products.json")
    headers = ['ID', 'Name', 'Category', 'Price']
    table_data = [headers] + [list(product) for product in products]

    window = Toplevel(root)
    window.title("Product List")

    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()
    window.geometry(f"600x400+{x}+{y}")

    global lst, total_rows, total_columns
    lst = table_data
    total_rows = len(lst)
    total_columns = len(lst[0])

    Table(window)

    close_button = tk.Button(window, text="Close", command=window.destroy)
    close_button.grid(row=total_rows + 1, columnspan=total_columns, pady=10)

""" #--------TASK 2---------
#razdeleni za da moje da raboti table (murzi me)
#ne sa pravilni opisaniqta na funkciite no mi trqbvaha dve za dvete tablici
def display_task_2(root):
    sales = read_sales("data/sales.json")
    window = tk.Toplevel(root)
    window.title("Task 2: Display Sales")
    headers = ['Name', 'Quantity', 'Date']
    table_rows = []
    for sale in sales:
        name, quantity, date = sale
        formatted_date = format_display_date(date)
        table_rows.append([name, quantity, formatted_date])

    table_data = [headers] + table_rows
    
   
    # Position window beside the main window
    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()
    window.geometry(f"600x400+{x}+{y}")

    # Set global variables for table
    global lst, total_rows, total_columns
    lst = table_data
    total_rows = len(lst)
    total_columns = len(lst[0])

    # Create table
    Table(window)
    close_button = tk.Button(window, text="Close", command=window.destroy)
    close_button.grid(row=total_rows + 1, columnspan=total_columns, pady=10)

 """
# ---------- TASK 3 ----------
def summarize_sales(sales):
    summary = {}
    for name, quantity,_,_ in sales:
        if name in summary:
            summary[name] += quantity
        else:
            summary[name] = quantity
    return summary


def summary_sales(root):
    sales = read_sales("data/sales.json")
    summary = summarize_sales(sales)

    window = tk.Toplevel(root)
    window.title("Summary of Sales")

    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()
    window.geometry(f"600x400+{x}+{y}")

    headers = ['Product Name', 'Total Sold']
    table_data = [headers] + [[product, total] for product, total in summary.items()]

    global lst, total_rows, total_columns
    lst = table_data
    total_rows = len(lst)
    total_columns = len(lst[0])

    Table(window)

    close_button = tk.Button(window, text="Close", command=window.destroy)
    close_button.grid(row=total_rows + 1, columnspan=total_columns, pady=10)


# ---------- TASK 4 ----------
def search_product(root):
    sales = read_sales("data/sales.json")
    summary = summarize_sales(sales)


    window = tk.Toplevel(root)
    window.title("Search Product")

    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()
    window.geometry(f"600x400+{x}+{y}")

    tk.Label(window, text="Enter product name:").pack(pady=5)
    entry = tk.Entry(window, width=30)
    entry.pack(pady=5)

    result_label = tk.Label(window, text="", fg="blue")
    result_label.pack(pady=10)


    def search():
        product_input = entry.get().strip().lower()
        # print(f"User input (lowercased): '{product_input}'")  # DEBUG

        found = False
        for key in summary:
            key_lower = key.lower()
            # print(f"Comparing with key: '{key}' (lowercased: '{key_lower}')")  # DEBUG

            if key_lower == product_input:
                result_label.config(text=f"{key} → Total Sold: {summary[key]}", fg="blue")
                found = True
                break

        if not found:
            result_label.config(text="Product not found.", fg="red")

    tk.Button(window, text="Search", command=search).pack(pady=5)
    tk.Button(window, text="Close", command=window.destroy).pack(pady=5)


# ---------- TASK 5 and 6 ----------
def filter_sales_by_quantity(sales, min_quantity=5):
    return [sale for sale in sales if sale[1] >= min_quantity]


def filter_sales(root):
    sales = read_sales("data/sales.json")
    
    window = tk.Toplevel(root)
    window.title("Filter Sales")

    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()
    window.geometry(f"600x400+{x}+{y}")

    tk.Label(window, text="Minimum Quantity:").pack(pady=(10, 0))
    spinbox = tk.Spinbox(window, from_=1, to=100, width=5)
    spinbox.pack(pady=5)

    table_frame = tk.Frame(window)
    table_frame.pack(padx=10, pady=10)

    headers = ['Product ID', 'Quantity', 'Date']

    def show_table(data):
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Format date column (3rd column) in each row
        formatted_data = []
        for row in data:
         formatted_row = list(row)
         formatted_row[2] = format_display_date(row[2])  # format the date
         formatted_data.append(formatted_row)

        table_data = [headers] + formatted_data

        global lst, total_rows, total_columns
        lst = table_data
        total_rows = len(lst)
        total_columns = len(lst[0])

        Table(table_frame)

    def apply_filter():
        min_qty = int(spinbox.get())
        filtered = [sale for sale in sales if sale[1] >= min_qty]
        show_table(filtered)

    # Show all sales initially
    show_table(sales)

    tk.Button(window, text="Apply Filter", command=apply_filter).pack(pady=5)
    tk.Button(window, text="Close", command=window.destroy).pack(pady=5)



# ---------- TASK 7 ----------
def new_sale(root):
    with open("data/products.json", "r", encoding="utf-8") as file:
        product_data = json.load(file)
        product_names = [item['name'] for item in product_data['products']]

    sales = []

    def add_sale():
        name = product_combobox.get()
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

        new_sale = {"productName": name, "quantity": quantity, "date": date}

        if os.path.exists("data/sales.json"):
            with open("data/sales.json", "r", encoding="utf-8") as file:
                data = json.load(file)
        else:
            data = {}

        sales_list = data.get("sales", [])
        sales_list.append(new_sale)
        data["sales"] = sales_list

        with open("data/sales.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        dt = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = f"{dt.day}.{dt.month}.{dt.year}"

        listbox.insert(tk.END, f"{name} - {quantity} pcs on {formatted_date}")

        quantity_entry.delete(0, tk.END)

    window = tk.Toplevel(root)
    window.title("Task 7: Add New Sale")
    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()
    window.geometry(f"600x500+{x}+{y}")

    # Product Name (dropdown)
    tk.Label(window, text="Product Name:").pack(pady=(10, 0))
    product_combobox = ttk.Combobox(window, values=product_names, state="readonly", width=37)
    product_combobox.pack(pady=5)
    product_combobox.set(product_names[0])  # Default selection

    tk.Label(window, text="Quantity:").pack(pady=(10, 0))
    quantity_entry = tk.Entry(window, width=40)
    quantity_entry.pack(pady=5)

    tk.Label(window, text="Select Date:").pack(pady=(10, 0))
    cal = Calendar(window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=5)

    tk.Button(window, text="Add Sale", command=add_sale).pack(pady=10)

    listbox = tk.Listbox(window, width=50, height=10)
    listbox.pack(padx=10, pady=10)

    for sale in sales:
     formatted_date = format_display_date(sale[2])
     listbox.insert(tk.END, f"{sale[0]} - {sale[1]} pcs on {formatted_date}")

# add recepit products to sales.json
      
def add_from_receipt(products, sale_date):
    with open("data/sales.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            
    highest_id = 0
    for sale in data.get("sales", []):
        sale_id = sale.get("saleID", "")
        if sale_id:
            id_var = int(sale_id)
            if id_var > highest_id:
                highest_id = id_var
    
    transaction_id = highest_id + 1
    
    for item in products:
        new_sale = {
            "productName": item["name"],
            "quantity": item["quantity"],
            "date": sale_date,
            "saleID": transaction_id
        }
        data["sales"].append(new_sale)
    
    with open("data/sales.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    
    return transaction_id


# ---------- TASK 8 ----------
def new_transaction(root):
    with open("data/products.json", "r", encoding="utf-8") as f:
        products_data = json.load(f)["products"]
    product_names = [product["name"] for product in products_data]

    selected_products = []

    def add_product():
        name = product_combo.get()
        quantity_str = quantity_entry.get()

        if not name or not quantity_str:
            messagebox.showwarning("Input Error", "Please select a product and enter quantity.")
            return

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Quantity must be a positive integer.")
            return

        product = next((p for p in products_data if p["name"] == name), None)
        if not product:
            messagebox.showerror("Error", "Product not found.")
            return

        selected_products.append({
            "name": name,
            "quantity": quantity,
            "price": product["price"]
        })

        refresh_receipt_display()

        # Reset fields
        product_combo.set("")
        quantity_entry.delete(0, tk.END)

    def refresh_receipt_display():
        receipt_box.delete(0, tk.END)
        total = 0
        for item in selected_products:
            line = f"{item['name']} x{item['quantity']} = €{item['quantity'] * item['price']:.2f}"
            receipt_box.insert(tk.END, line)
            total += item['quantity'] * item['price']
        total_label.config(text=f"Total: €{total:.2f}")

    def save_receipt():
     if not selected_products:
         messagebox.showwarning("Empty Receipt", "No products added.")
         return

     if not os.path.exists("receipts"):
            os.makedirs("receipts")

     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
     readable_date = datetime.now().strftime("%d %B %Y, %H:%M")
     current_date = datetime.now().strftime("%Y-%m-%d")
     filename = f"receipts/receipt_{timestamp}.txt"

     total = 0
     receipt_lines = [
        "      ★ Coffee Store Receipt ★",
        "=============================================",
        f"Date: {readable_date}",
        "",
        f"{'Product':<20}{'Qty':<5}{'Unit':<8}{'Total':<8}",
        "-" * 45
    ]

     for item in selected_products:
        line_total = item['quantity'] * item['price']
        receipt_lines.append(
            f"{item['name']:<20}{item['quantity']:<5}€{item['price']:<8.2f}€{line_total:<8.2f}"
        )
        total += line_total

     receipt_lines += [
          "-" * 45,
        f"{'Total:':<24}{'':5}{'':5}€{total:<8.2f}",
        "",
        "Thank you for shopping with us!",
        "We hope to see you again soon 😊",
    ]

     with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(receipt_lines))

     add_from_receipt(selected_products, current_date)
     messagebox.showinfo("Receipt Saved", f"Receipt saved to:\n{filename}")

 

    # GUI Window
    window = tk.Toplevel(root)
    window.title("Task 8: Create Receipt")

    x = root.winfo_x() + root.winfo_width()
    y = root.winfo_y()
    window.geometry(f"600x500+{x}+{y}")

    tk.Label(window, text="Select Product:").pack(pady=(10, 0))
    product_combo = ttk.Combobox(window, values=product_names, width=40)
    product_combo.pack(pady=5)

    tk.Label(window, text="Enter Quantity:").pack()
    quantity_entry = tk.Entry(window, width=20)
    quantity_entry.pack(pady=5)

    tk.Button(window, text="Add Product", command=add_product).pack(pady=10)

    receipt_box = tk.Listbox(window, width=50, height=12)
    receipt_box.pack(pady=10)

    total_label = tk.Label(window, text="Total: €0.00", font=("Arial", 12, "bold"))
    total_label.pack(pady=5)

    tk.Button(window, text="Save Receipt", command=save_receipt).pack(pady=10)

# ---------- MAIN MENU ----------
def main_menu():
    root = tk.Tk()
    bg = PhotoImage(file = "img\coffee.png")
    label1 = Label( root, image = bg)
    label1.place(x = 0, y = 0)
    root.title("Course Project Menu")
    root.iconbitmap("img\images.ico") #samostoqtelno izrabotena s gimp!!

    tk.Label(root, text="Choose a Task to View:", font=("Arial", 14)).pack(pady=10)


    tk.Button(root, text="Task 1&2 Dispalay Products", width=40, command=lambda: product_list(root)).pack(pady=5)
    # tk.Button(root, text="Task 1&2: Display Sales", width=40, command=lambda: display_task_2(root)).pack(pady=5)
    tk.Button(root, text="Task 3: Summary Dictionary", width=40, command=lambda: summary_sales(root)).pack(pady=5)
    tk.Button(root, text="Task 4: Search in Dictionary", width=40, command=lambda: search_product(root)).pack(pady=5)
    tk.Button(root, text="Task 5: Filter Sales by Quantity", width=40, command=lambda: filter_sales(root)).pack(pady=5)
    tk.Button(root, text="Task 7: Add New Sale", width=40, command=lambda: new_sale(root)).pack(pady=5) #wip
    tk.Button(root, text="Task 8: Receipt Form", command=lambda: new_transaction(root)).pack(pady=5)


    root.mainloop()


if __name__ == "__main__":
    main_menu()
