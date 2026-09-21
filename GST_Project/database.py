import sqlite3

# ================= DATABASE CONNECT =================

conn = sqlite3.connect("gst_invoice.db")

cursor = conn.cursor()

# ================= CREATE TABLE =================

cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_name TEXT,

    gst_number TEXT,

    product_name TEXT,

    quantity INTEGER,

    price REAL,

    gst REAL,

    total REAL
)
""")

conn.commit()

# ================= SAVE DATA =================

def save_invoice(

    customer_name,
    gst_number,
    product_name,
    quantity,
    price,
    gst,
    total
):

    cursor.execute("""

    INSERT INTO invoices (

        customer_name,
        gst_number,
        product_name,
        quantity,
        price,
        gst,
        total

    )

    VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        customer_name,
        gst_number,
        product_name,
        quantity,
        price,
        gst,
        total
    ))

    conn.commit()

# ================= FETCH DATA =================

def get_invoices():

    cursor.execute("""

    SELECT
    customer_name,
    gst_number,
    product_name,
    quantity,
    price,
    gst,
    total

    FROM invoices

    """)

    return cursor.fetchall()


def delete_all_invoices():
    conn = sqlite3.connect("gst_invoice.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM invoices")

    conn.commit()
    conn.close()
# import sqlite3

# # Connect Database
# conn = sqlite3.connect("gst_invoice.db")

# cursor = conn.cursor()

# # Create Table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS invoices (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     customer_name TEXT,
#     gst_number TEXT,
#     total REAL,
#     date TEXT
# )
# """)

# conn.commit()


# # Save Invoice Function
# def save_invoice(customer_name, gst_number, total, date):

#     cursor.execute("""
#     INSERT INTO invoices(customer_name, gst_number, total, date)
#     VALUES (?, ?, ?, ?)
#     """, (customer_name, gst_number, total, date))

#     conn.commit()

# # ================= FETCH INVOICES =================

# def get_invoices():

#     cursor.execute("""
#     SELECT customer_name, gst_number, total, date
#     FROM invoices
#     """)

#     return cursor.fetchall()

# # ================= LOAD SAVED DATA =================

# def load_saved_invoices():

#     records = get_invoices()

#     for row in records:

#         saved_tree.insert(
#             "",
#             "end",
#             values=row
#         )
