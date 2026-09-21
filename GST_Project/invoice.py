items = []

grand_total = 0


def add_item(product, qty, price, gst):

    global grand_total

    subtotal = qty * price

    gst_amount = subtotal * gst / 100

    total = subtotal + gst_amount

    item = {
        "product": product,
        "qty": qty,
        "price": price,
        "gst": gst,
        "gst_amount": gst_amount,
        "total": round(total, 2)
    }

    items.append(item)

    grand_total += total

    return item, grand_total