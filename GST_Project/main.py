import tkinter as tk
from tkinter import ttk, messagebox
from database import save_invoice, get_invoices, delete_all_invoices
from pdf_generator import generate_pdf
import pandas as pd
from datetime import datetime


# ================= MAIN WINDOW =================

root = tk.Tk()
root.title("GST Billing System")
root.geometry("1200x700")
root.config(bg="#f0f0f0")

# ================= STYLE =================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview.Heading",
    font=("Arial", 11, "bold"),
    background="navy",
    foreground="white"
)

style.configure(
    "Treeview",
    rowheight=28,
    font=("Arial", 10)
)

# ================= VARIABLES =================

invoice_counter = 1

invoice_no = tk.StringVar(
    value=f"INV-{invoice_counter:03}"
)

customer_name = tk.StringVar()
gst_number = tk.StringVar()
customer_phone = tk.StringVar()

product_name = tk.StringVar()
quantity = tk.StringVar()
price = tk.StringVar()
gst_percent = tk.StringVar(value="18")

# ================= SHOP DETAILS =================

shop_name = tk.StringVar(value="ZillionSoftech Institute")
shop_address = tk.StringVar(value="Rewari , Haryana")
shop_phone = tk.StringVar(value="8392639422")
shop_gstin = tk.StringVar(value="NDS23452424")

# ================= TITLE =================

title = tk.Label(
    root,
    text="GST BILLING SYSTEM",
    font=("Arial", 24, "bold"),
    bg="navy",
    fg="white",
    pady=15
)

title.pack(fill="x")

# ================= DATE TIME =================

date_label = tk.Label(
    root,
    font=("Arial", 12, "bold"),
    bg="navy",
    fg="white"
)

date_label.place(x=930, y=20)


def update_time():

    current = datetime.now().strftime(
        "%d-%m-%Y  %I:%M:%S %p"
    )

    date_label.config(text=current)

    root.after(1000, update_time)
# ================= SHOP FRAME =================

shop_frame = tk.Frame(
    root,
    bg="#2c2c2c"
)

shop_frame.place(
    x=390,
    y=50,
    width=760,
    height=70
)

tk.Label(
    shop_frame,
    textvariable=shop_name,
    font=("Arial", 22, "bold"),
    bg="#2c2c2c",
    fg="white"
).pack()

tk.Label(
    shop_frame,
    textvariable=shop_address,
    font=("Arial", 11),
    bg="#2c2c2c",
    fg="lightgray"
).pack()

tk.Label(
    shop_frame,
    text=f"Phone : {shop_phone.get()}    GSTIN : {shop_gstin.get()}",
    font=("Arial", 11, "bold"),
    bg="#2c2c2c",
    fg="yellow"
).pack()

# ================= SEARCH BOX =================

search_var = tk.StringVar()

search_entry = tk.Entry(
    root,
    textvariable=search_var,
    width=30,
    font=("Arial", 11)
)

search_entry.place(x=20, y=50)


def search_invoice():

    search_text = search_var.get().lower()

    found = False

    for item in tree.get_children():

        values = tree.item(item)["values"]

        if search_text in str(values).lower():

            tree.selection_set(item)
            tree.focus(item)
            tree.see(item)

            found = True

            break

    if not found:

        messagebox.showinfo(
            "Search",
            "No Matching Record Found"
        )


search_button = tk.Button(
    root,
    text="Search",
    font=("Arial", 10, "bold"),
    bg="black",
    fg="white",
    width=10,
    command=search_invoice
)

search_button.place(x=270, y=47)

# ================= CUSTOMER FRAME =================

customer_frame = tk.LabelFrame(
    root,
    text="Customer Details",
    font=("Arial", 12, "bold"),
    bg="#f0f0f0",
    padx=10,
    pady=10
)

customer_frame.place(
    x=20,
    y=100,
    width=350,
    height=220
)

tk.Label(
    customer_frame,
    text="Customer Name",
    bg="#f0f0f0",
    font=("Arial", 11)
).grid(row=0, column=0, pady=10, sticky="w")

customer_entry = tk.Entry(
    customer_frame,
    textvariable=customer_name,
    width=25
)

customer_entry.grid(row=0, column=1)

tk.Label(
    customer_frame,
    text="GST Number",
    bg="#f0f0f0",
    font=("Arial", 11)
).grid(row=1, column=0, pady=10, sticky="w")

gst_entry = tk.Entry(
    customer_frame,
    textvariable=gst_number,
    width=25
)

gst_entry.grid(row=1, column=1)

tk.Label(
    customer_frame,
    text="Customer Phone",
    bg="#f0f0f0",
    font=("Arial", 11)
).grid(row=2, column=0, pady=10, sticky="w")

phone_entry = tk.Entry(
    customer_frame,
    textvariable=customer_phone,
    width=25
)

phone_entry.grid(row=2, column=1)

tk.Label(
    customer_frame,
    text="Invoice No",
    bg="#f0f0f0",
    font=("Arial", 11)
).grid(row=3, column=0, pady=10, sticky="w")

invoice_entry = tk.Entry(
    customer_frame,
    textvariable=invoice_no,
    width=25
)

invoice_entry.grid(row=3, column=1)

# ================= PRODUCT FRAME =================

product_frame = tk.LabelFrame(
    root,
    text="Product Details",
    font=("Arial", 12, "bold"),
    bg="#f0f0f0",
    padx=10,
    pady=10
)

product_frame.place(
    x=20,
    y=340,
    width=350,
    height=250
)

tk.Label(
    product_frame,
    text="Product Name",
    bg="#f0f0f0",
    font=("Arial", 11)
).grid(row=0, column=0, pady=10, sticky="w")

product_entry = tk.Entry(
    product_frame,
    textvariable=product_name,
    width=25
)

product_entry.grid(row=0, column=1)

tk.Label(
    product_frame,
    text="Quantity",
    bg="#f0f0f0",
    font=("Arial", 11)
).grid(row=1, column=0, pady=10, sticky="w")

qty_entry = tk.Entry(
    product_frame,
    textvariable=quantity,
    width=25
)

qty_entry.grid(row=1, column=1)

tk.Label(
    product_frame,
    text="Price",
    bg="#f0f0f0",
    font=("Arial", 11)
).grid(row=2, column=0, pady=10, sticky="w")

price_entry = tk.Entry(
    product_frame,
    textvariable=price,
    width=25
)

price_entry.grid(row=2, column=1)

tk.Label(
    product_frame,
    text="GST %",
    bg="#f0f0f0",
    font=("Arial", 11)
).grid(row=3, column=0, pady=10, sticky="w")

gst_percent_entry = tk.Entry(
    product_frame,
    textvariable=gst_percent,
    width=25
)

gst_percent_entry.grid(row=3, column=1)

# ================= TABLE FRAME =================

table_frame = tk.Frame(root)

table_frame.place(
    x=390,
    y=130,
    width=770,
    height=390
)

columns = (
    "Product",
    "Qty",
    "Price",
    "GST%",
    "Total"
)

scroll_y = tk.Scrollbar(
    table_frame,
    orient="vertical"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    yscrollcommand=scroll_y.set
)

scroll_y.config(command=tree.yview)
scroll_y.pack(side="right", fill="y")

tree.pack(fill="both", expand=True)

for col in columns:
    tree.heading(col, text=col)

tree.column("Product", width=260)
tree.column("Qty", width=80)
tree.column("Price", width=120)
tree.column("GST%", width=100)
tree.column("Total", width=150)

# ================= TOTAL LABELS =================

subtotal_label = tk.Label(
    root,
    text="Subtotal : ₹ 0",
    font=("Arial", 14, "bold"),
    fg="blue",
    bg="#f0f0f0"
)

subtotal_label.place(x=390, y=535)

gst_label = tk.Label(
    root,
    text="GST Amount : ₹ 0",
    font=("Arial", 14, "bold"),
    fg="green",
    bg="#f0f0f0"
)

gst_label.place(x=390, y=565)

cgst_label = tk.Label(
    root,
    text="CGST : ₹ 0",
    font=("Arial", 14, "bold"),
    fg="purple",
    bg="#f0f0f0"
)

cgst_label.place(x=20, y=540)

sgst_label = tk.Label(
    root,
    text="SGST : ₹ 0",
    font=("Arial", 14, "bold"),
    fg="brown",
    bg="#f0f0f0"
)

sgst_label.place(x=20, y=570)

product_count_label = tk.Label(
    root,
    text="Total Products : 0",
    font=("Arial", 14, "bold"),
    fg="black",
    bg="#f0f0f0"
)

product_count_label.place(x=20, y=600)

total_label = tk.Label(
    root,
    text="Grand Total : ₹ 0",
    font=("Arial", 18, "bold"),
    fg="red",
    bg="#f0f0f0"
)

total_label.place(x=850, y=585)

# ================= TOTAL VARIABLES =================

grand_total = 0
subtotal_amount = 0
total_gst_amount = 0
total_products = 0

# ================= UPDATE LABELS =================

def update_labels():

    subtotal_label.config(
        text=f"Subtotal : ₹ {round(subtotal_amount, 2)}"
    )

    gst_label.config(
        text=f"GST Amount : ₹ {round(total_gst_amount, 2)}"
    )

    cgst_label.config(
        text=f"CGST : ₹ {round(total_gst_amount / 2, 2)}"
    )

    sgst_label.config(
        text=f"SGST : ₹ {round(total_gst_amount / 2, 2)}"
    )

    product_count_label.config(
        text=f"Total Products : {total_products}"
    )

    total_label.config(
        text=f"Grand Total : ₹ {round(grand_total, 2)}"
    )

# ================= FUNCTIONS =================

def clear_all():

    global grand_total
    global subtotal_amount
    global total_gst_amount
    global total_products

    tree.delete(*tree.get_children())

    customer_name.set("")
    gst_number.set("")
    customer_phone.set("")
    product_name.set("")
    quantity.set("")
    price.set("")
    gst_percent.set("18")

    grand_total = 0
    subtotal_amount = 0
    total_gst_amount = 0
    total_products = 0

    update_labels()

    customer_entry.focus()


def clear_database():

    global grand_total
    global subtotal_amount
    global total_gst_amount
    global total_products

    result = messagebox.askyesno(
        "Confirm",
        "Delete all invoice records?"
    )

    if result:

        delete_all_invoices()

        tree.delete(*tree.get_children())

        grand_total = 0
        subtotal_amount = 0
        total_gst_amount = 0
        total_products = 0

        update_labels()

        messagebox.showinfo(
            "Success",
            "All Records Deleted"
        )


def add_product():

    global grand_total
    global subtotal_amount
    global total_gst_amount
    global total_products

    try:

        if customer_name.get() == "":
            messagebox.showerror(
                "Error",
                "Please enter customer name"
            )
            return

        pname = product_name.get()

        if pname == "":
            messagebox.showerror(
                "Error",
                "Please enter product name"
            )
            return

        qty = int(quantity.get())
        pr = float(price.get())
        gst = float(gst_percent.get())

        subtotal = qty * pr
        gst_amount = subtotal * gst / 100
        total = subtotal + gst_amount

        subtotal_amount += subtotal
        total_gst_amount += gst_amount
        grand_total += total
        total_products += qty

        tree.insert(
            "",
            "end",
            values=(
                pname,
                qty,
                pr,
                gst,
                round(total, 2)
            )
        )

        save_invoice(
            customer_name.get(),
            gst_number.get(),
            pname,
            qty,
            pr,
            gst,
            total
        )

        update_labels()

        product_name.set("")
        quantity.set("")
        price.set("")
        gst_percent.set("18")

        product_entry.focus()

    except ValueError:

        messagebox.showerror(
            "Error",
            "Please enter valid quantity, price and GST"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


def load_old_data():

    global grand_total
    global subtotal_amount
    global total_gst_amount
    global total_products

    tree.delete(*tree.get_children())

    grand_total = 0
    subtotal_amount = 0
    total_gst_amount = 0
    total_products = 0

    records = get_invoices()

    if len(records) == 0:

        messagebox.showinfo(
            "Info",
            "No Data Found"
        )

        update_labels()

        return

    for row in records:

        product = row[2]
        qty = int(row[3])
        price_value = float(row[4])
        gst = float(row[5])
        total = float(row[6])

        subtotal = total / (1 + gst / 100)
        gst_amount = total - subtotal

        tree.insert(
            "",
            "end",
            values=(
                product,
                qty,
                price_value,
                gst,
                round(total, 2)
            )
        )

        grand_total += total
        subtotal_amount += subtotal
        total_gst_amount += gst_amount
        total_products += qty

    update_labels()

    messagebox.showinfo(
        "Success",
        "Old Data Loaded Successfully"
    )


def generate_loaded_pdf():

    global invoice_counter

    all_items = []

    for child in tree.get_children():

        values = tree.item(child)["values"]

        item = {
            "product": values[0],
            "qty": float(values[1]),
            "price": float(values[2]),
            "gst": float(values[3]),
            "total": float(values[4])
        }

        all_items.append(item)

    if len(all_items) == 0:

        messagebox.showerror(
            "Error",
            "No Data Found"
        )

        return

    try:

        file_name = generate_pdf(
            customer_name.get(),
            gst_number.get(),
            invoice_no.get(),
            customer_phone.get(),
            all_items,
            grand_total
        )

        messagebox.showinfo(
            "Success",
            f"PDF Generated Successfully\n{file_name}"
        )

        invoice_counter += 1

        invoice_no.set(
            f"INV-{invoice_counter:03}"
        )

    except Exception as e:

        messagebox.showerror(
            "PDF Error",
            str(e)
        )


def delete_item():

    global grand_total
    global subtotal_amount
    global total_gst_amount
    global total_products

    selected = tree.selection()

    if not selected:

        messagebox.showerror(
            "Error",
            "Select Item First"
        )

        return

    values = tree.item(selected[0])["values"]

    qty = int(values[1])
    total = float(values[4])
    gst = float(values[3])

    subtotal = total / (1 + gst / 100)
    gst_amount = total - subtotal

    grand_total -= total
    subtotal_amount -= subtotal
    total_gst_amount -= gst_amount
    total_products -= qty

    tree.delete(selected[0])

    update_labels()


def export_excel():

    data = []

    for child in tree.get_children():

        values = tree.item(child)["values"]

        data.append(values)

    if len(data) == 0:

        messagebox.showerror(
            "Error",
            "No Data Found"
        )

        return

    df = pd.DataFrame(
        data,
        columns=[
            "Product",
            "Qty",
            "Price",
            "GST%",
            "Total"
        ]
    )

    file_name = f"Invoice_{invoice_no.get()}.xlsx"

    df.to_excel(
        file_name,
        index=False
    )

    messagebox.showinfo(
        "Success",
        f"Excel Saved\n{file_name}"
    )

# ================= BUTTON FRAME =================

button_frame = tk.Frame(
    root,
    bg="#f0f0f0"
)

button_frame.place(x=20, y=635)

tk.Button(
    button_frame,
    text="Add Product",
    font=("Arial", 11, "bold"),
    bg="green",
    fg="white",
    width=15,
    command=add_product
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Generate PDF",
    font=("Arial", 11, "bold"),
    bg="orange",
    fg="white",
    width=15,
    command=generate_loaded_pdf
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Load Data",
    font=("Arial", 11, "bold"),
    bg="purple",
    fg="white",
    width=15,
    command=load_old_data
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Delete Item",
    font=("Arial", 11, "bold"),
    bg="darkred",
    fg="white",
    width=15,
    command=delete_item
).grid(row=0, column=3, padx=5)

tk.Button(
    button_frame,
    text="Export Excel",
    font=("Arial", 11, "bold"),
    bg="teal",
    fg="white",
    width=15,
    command=export_excel
).grid(row=0, column=4, padx=5)

tk.Button(
    button_frame,
    text="Clear",
    font=("Arial", 11, "bold"),
    bg="red",
    fg="white",
    width=15,
    command=clear_all
).grid(row=0, column=5, padx=5)

tk.Button(
    button_frame,
    text="Print",
    font=("Arial", 11, "bold"),
    bg="black",
    fg="white",
    width=15,
    command=generate_loaded_pdf
).grid(row=1, column=0, pady=10)

tk.Button(
    button_frame,
    text="Delete All Data",
    font=("Arial", 11, "bold"),
    bg="darkred",
    fg="white",
    width=15,
    command=clear_database
).grid(row=1, column=1, pady=10)

# ================= KEYBOARD MOVEMENT =================

customer_entry.bind(
    "<Return>",
    lambda event: gst_entry.focus()
)

gst_entry.bind(
    "<Return>",
    lambda event: phone_entry.focus()
)

phone_entry.bind(
    "<Return>",
    lambda event: invoice_entry.focus()
)

invoice_entry.bind(
    "<Return>",
    lambda event: product_entry.focus()
)

product_entry.bind(
    "<Return>",
    lambda event: qty_entry.focus()
)

qty_entry.bind(
    "<Return>",
    lambda event: price_entry.focus()
)

price_entry.bind(
    "<Return>",
    lambda event: gst_percent_entry.focus()
)

gst_percent_entry.bind(
    "<Return>",
    lambda event: add_product()
)

# ================= START =================

customer_entry.focus()

root.mainloop()