from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.graphics.barcode import code128
from datetime import datetime
import os

try:
    import qrcode
except:
    qrcode = None

try:
    from num2words import num2words
except:
    num2words = None


def generate_pdf(
        customer_name,
        gst_number,
        invoice_no,
        customer_phone,
        items,
        grand_total
):

    # ================= COMPANY DETAILS =================

    company_name = "ZillionSoftech Institute"
    company_address = "Hisar"
    company_phone = "8392639422"
    company_email = "Zindal@gmail.com"
    company_gstin = "NDS23452424"
    company_pan = "FAE2522524264"

    bank_name = "HDFC BANK"
    account_no = "232948529347274"
    ifsc_code = "HDFC2832"
    upi_id = "ZINDAL123"

    # ================= FOLDER =================

    if not os.path.exists("invoices"):
        os.makedirs("invoices")

    filename = f"invoices/Invoice_{invoice_no}.pdf"

    pdf = canvas.Canvas(filename, pagesize=A4)

    width, height = A4

    # ================= COLORS =================

    blue = colors.HexColor("#123B7A")
    green = colors.HexColor("#1B8A3A")
    light_blue = colors.HexColor("#EAF1FF")
    light_gray = colors.HexColor("#F2F2F2")

    # ================= WATERMARK =================

    # ================= LOGO WATERMARK =================

    pdf.saveState()

    try:
        pdf.setFillAlpha(0.10)   # watermark light
        pdf.drawImage(
        "logo.png",
        170,
        300,
        width=260,
        height=260,
        mask="auto"
        )
    except:
        pass

    pdf.restoreState()

    # ================= TOP HEADER =================

    pdf.setFillColor(blue)
    pdf.rect(0, 805, width, 37, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(width / 2, 817, "GST TAX INVOICE")

    # ================= LOGO =================

    try:
        pdf.drawImage(
            "logo.png",
            25,
            710,
            width=85,
            height=85,
            mask="auto"
        )
    except:
        pdf.setFillColor(blue)
        pdf.circle(67, 752, 38, fill=1)
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawCentredString(67, 744, "ZE")

    # ================= COMPANY DETAILS =================

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawString(125, 770, company_name.upper())

    pdf.setFont("Helvetica", 10)
    pdf.drawString(125, 750, f"Address : {company_address}")
    pdf.drawString(125, 735, f"Phone : {company_phone}")
    pdf.drawString(125, 720, f"Email : {company_email}")
    pdf.drawString(125, 705, f"GSTIN : {company_gstin}")
    pdf.drawString(125, 690, f"PAN : {company_pan}")

    # ================= TAX INVOICE BOX =================

    pdf.setFillColor(blue)
    pdf.roundRect(395, 705, 165, 42, 8, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(477, 720, "TAX INVOICE")

    # ================= INVOICE DETAILS BOX =================

    today = datetime.now().strftime("%d-%m-%Y")

    pdf.setStrokeColor(blue)
    pdf.setFillColor(colors.white)
    pdf.roundRect(395, 580, 165, 105, 5, fill=0, stroke=1)

    pdf.setFillColor(blue)
    pdf.rect(395, 660, 165, 25, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(410, 668, "INVOICE DETAILS")

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(405, 640, f"Invoice No : {invoice_no}")
    pdf.drawString(405, 622, f"Date : {today}")
    pdf.drawString(405, 604, "Place : Haryana")
    pdf.drawString(405, 586, "Payment : Cash")
    # ================= BILL TO BOX =================

    pdf.setStrokeColor(blue)
    pdf.roundRect(30, 575, 330, 105, 5, fill=0, stroke=1)

    pdf.setFillColor(blue)
    pdf.rect(30, 655, 330, 25, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(45, 663, "BILL TO")

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(45, 635, f"Customer Name : {customer_name}")
    pdf.drawString(45, 615, f"Mobile No.    : {customer_phone}")
    pdf.drawString(45, 595, f"GSTIN         : {gst_number}")

    # ================= TABLE HEADER =================

    y = 525

    pdf.setFillColor(blue)
    pdf.rect(30, y, 530, 28, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 9)

    pdf.drawString(38, y + 10, "SR")
    pdf.drawString(70, y + 10, "DESCRIPTION")
    pdf.drawString(240, y + 10, "QTY")
    pdf.drawString(295, y + 10, "RATE")
    pdf.drawString(365, y + 10, "GST%")
    pdf.drawString(430, y + 10, "GST AMT")
    pdf.drawString(500, y + 10, "AMOUNT")

    # ================= PRODUCT ROWS =================

    y -= 25
    sr = 1
    subtotal = 0
    total_gst = 0

    for item in items:

        qty = float(item["qty"])
        rate = float(item["price"])
        gst = float(item["gst"])
        total = float(item["total"])

        item_subtotal = qty * rate
        gst_amount = item_subtotal * gst / 100

        subtotal += item_subtotal
        total_gst += gst_amount

        if sr % 2 == 0:
            pdf.setFillColor(light_gray)
            pdf.rect(30, y - 6, 530, 24, fill=1, stroke=0)

        pdf.setFillColor(colors.black)
        pdf.setFont("Helvetica", 9)

        product_text = str(item["product"])
        if len(product_text) > 25:
            product_text = product_text[:25] + "..."

        pdf.drawString(38, y, str(sr))
        pdf.drawString(70, y, product_text)
        pdf.drawRightString(260, y, str(int(qty)))
        pdf.drawRightString(335, y, f"{rate:.2f}")
        pdf.drawRightString(390, y, f"{gst:.2f}")
        pdf.drawRightString(470, y, f"{gst_amount:.2f}")
        pdf.drawRightString(555, y, f"{total:.2f}")

        pdf.setStrokeColor(colors.lightgrey)
        pdf.line(30, y - 10, 560, y - 10)

        y -= 25
        sr += 1

    # ================= TABLE OUTER BORDER =================

    table_top = 553
    table_bottom = y + 15

    pdf.setStrokeColor(colors.grey)
    pdf.rect(30, table_bottom, 530, table_top - table_bottom, stroke=1, fill=0)

    pdf.line(60, table_top, 60, table_bottom)
    pdf.line(230, table_top, 230, table_bottom)
    pdf.line(270, table_top, 270, table_bottom)
    pdf.line(345, table_top, 345, table_bottom)
    pdf.line(400, table_top, 400, table_bottom)
    pdf.line(480, table_top, 480, table_bottom)

    # ================= GST SUMMARY =================

    cgst = total_gst / 2
    sgst = total_gst / 2

    total_box_y = y - 10

    pdf.setStrokeColor(blue)
    pdf.roundRect(330, total_box_y - 110, 230, 110, 5, fill=0, stroke=1)

    pdf.setFillColor(light_blue)
    pdf.rect(330, total_box_y - 25, 230, 25, fill=1, stroke=0)

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(345, total_box_y - 17, "GST SUMMARY")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(345, total_box_y - 45, "Subtotal")
    pdf.drawRightString(545, total_box_y - 45, f"Rs. {subtotal:.2f}")

    pdf.drawString(345, total_box_y - 65, "CGST")
    pdf.drawRightString(545, total_box_y - 65, f"Rs. {cgst:.2f}")

    pdf.drawString(345, total_box_y - 85, "SGST")
    pdf.drawRightString(545, total_box_y - 85, f"Rs. {sgst:.2f}")

    pdf.setFillColor(green)
    pdf.rect(330, total_box_y - 135, 230, 28, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(345, total_box_y - 125, "GRAND TOTAL")
    pdf.drawRightString(545, total_box_y - 125, f"Rs. {grand_total:.2f}")

# ================= THANK YOU DESIGN =================
 
    thank_x = 50
    thank_y = total_box_y - 70

    pdf.setFillColor(green)
    pdf.setFont("Helvetica-Oblique", 14)
    pdf.drawString(thank_x, thank_y, "Thank you for choosing")

    pdf.setFillColor(colors.green)
    pdf.setFont("Helvetica-BoldOblique", 17)
    pdf.drawString(thank_x + 90, thank_y - 22, "Zillionsoftech!")
    pdf.setFillColor(blue)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(
    thank_x + 90,
    thank_y - 42,
    "Visit Again"
)
# Graduation cap / simple icon
    pdf.setFillColor(blue)
    pdf.setFont("Helvetica-Bold", 34)
    pdf.drawString(thank_x + 70, thank_y - 70, "🎓")

    try:
        pdf.drawImage(
        "cap.png",
        thank_x + 65,
        thank_y - 70,
        width=55,
        height=40,
        mask="auto"
    )
    except:
        pass
    # ================= AMOUNT IN WORDS =================

    if num2words:
        words = num2words(round(grand_total), lang="en_IN").title()
    else:
        words = str(round(grand_total))

    words_y = total_box_y - 145

    pdf.setStrokeColor(blue)
    pdf.roundRect(30, words_y - 35, 530, 45, 5, fill=0, stroke=1)

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(45, words_y - 5, "Amount In Words:")

    pdf.setFont("Helvetica", 9)
    pdf.drawString(45, words_y - 22, words + " Only")

    # ================= BANK DETAILS =================

    bank_y = words_y - 70

    pdf.setStrokeColor(blue)
    pdf.roundRect(30, bank_y - 85, 245, 90, 5, fill=0, stroke=1)

    pdf.setFillColor(blue)
    pdf.rect(30, bank_y - 20, 245, 25, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(45, bank_y - 12, "BANK DETAILS")

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(45, bank_y - 40, f"Bank : {bank_name}")
    pdf.drawString(45, bank_y - 58, f"A/C  : {account_no}")
    pdf.drawString(45, bank_y - 76, f"IFSC : {ifsc_code}")

    # ================= QR CODE =================

    qr_x = 295
    qr_y = bank_y - 80

    pdf.setStrokeColor(blue)
    pdf.roundRect(qr_x, qr_y, 95, 95, 5, fill=0, stroke=1)

    if qrcode:
        try:
            upi_link = f"upi://pay?pa={upi_id}&pn={company_name}&am={grand_total:.2f}"
            qr_img = qrcode.make(upi_link)
            qr_path = os.path.join("invoices", "payment_qr.png")
            qr_img.save(qr_path)

            pdf.drawImage(
                qr_path,
                qr_x + 8,
                qr_y + 15,
                width=78,
                height=72,
                mask="auto"
            )
        except:
            pdf.setFont("Helvetica", 8)
            pdf.drawString(qr_x + 20, qr_y + 50, "QR Error")
    else:
        pdf.setFont("Helvetica", 8)
        pdf.drawString(qr_x + 12, qr_y + 50, "Install qrcode")

    pdf.setFont("Helvetica-Bold", 8)
    pdf.setFillColor(colors.black)
    pdf.drawCentredString(qr_x + 47, qr_y + 5, "Scan & Pay")

    # ================= SIGNATURE BOX =================

    sign_x = 410
    sign_y = bank_y - 80

    pdf.setStrokeColor(blue)
    pdf.roundRect(sign_x, sign_y, 150, 95, 5, fill=0, stroke=1)

    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(colors.black)
    pdf.drawCentredString(
    sign_x + 75,
    sign_y + 55,
    f"For {company_name}"
    )

    pdf.line(sign_x + 20, sign_y + 30, sign_x + 130, sign_y + 30)

    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawCentredString(sign_x + 75, sign_y + 15, "Authorized Signatory")

    # ================= BARCODE =================

    try:
        barcode = code128.Code128(invoice_no, barHeight=28, barWidth=1.1)
        barcode.drawOn(pdf, 360, 90)
        pdf.setFont("Helvetica", 8)
        pdf.drawString(390, 78, invoice_no)
    except:
        pass

    # ================= TERMS =================

    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(30, 105, "Terms & Conditions")

    pdf.setFont("Helvetica", 8)
    pdf.drawString(30, 90, "1. Goods once sold will not be returned.")
    pdf.drawString(30, 78, "2. Warranty as per company policy.")
    pdf.drawString(30, 66, "3. Subject to Hisar jurisdiction.")

    # ================= FOOTER =================

    pdf.setFillColor(blue)
    pdf.rect(0, 0, width, 28, fill=1, stroke=0)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(width / 2, 10,f"For {company_name}"
f"Thank You For Choosing {company_name}" )

    pdf.save()

    return filename