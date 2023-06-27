from reportlab.pdfgen import canvas
import os

class Invoice:
    def __init__(self, customer_name, contact_number, token_id, date, delivery_address):
        self.customer_name = customer_name
        self.contact_number = contact_number
        self.delivery_address = delivery_address
        self.token_id = token_id
        self.date=date
        self.cuisines = []
    
    def add_cuisine(self, name, quantity, rate, discount, discount_per):
        self.cuisines.append(
            {
                "name": name,
                "quantity": quantity,
                "rate": rate,
                "discount": discount if quantity // discount_per > 0 else 0.0,
                "discount_per": discount_per,
                "total": quantity * rate * (1 - (discount if quantity//discount_per > 0 else 0.0))
            }
        )

def generate_pdf(invoice):
    os.makedirs("gen-invoice-pdfs", exist_ok=True)
    c = canvas.Canvas("gen-invoice-pdfs/invoice_{}.pdf".format(invoice.token_id), pagesize=(200, 250), bottomup=0)
    c.setFillColorRGB(7/255, 14/255, 23/255)
    c.line(70, 22, 180, 22)
    c.line(5, 45, 195, 45)
    c.line(10, 120, 190, 120)
    c.line(28, 108, 28, 220)
    c.line(90, 108, 90, 220)
    c.line(120, 108, 120, 220)
    c.line(140, 108, 140, 220)
    c.line(155, 108, 155, 220)
    c.line(10, 220, 190, 220)
    c.translate(10, 40)
    c.scale(1, -1)
    c.drawImage("app/static/images/invoice-logo.png", 0, 0, width=30, height=30)
    c.scale(1, -1)
    c.translate(-10, -40)
    c.setFont("Times-Bold", 10)
    c.drawCentredString(125, 20, "ResBot")
    c.setFont("Times-Bold", 5)
    c.drawCentredString(125, 30, "Biratnagar, Morang")
    # c.drawCentredString(125, 35, self.city.get() + ", India")
    # c.setFont("Times-Bold", 6)
    # c.drawCentredString(125, 42, "GST No:"+self.gst.get())
    c.setFont("Times-Bold", 7)
    c.drawCentredString(100, 55, "INVOICE")
    c.setFont("Times-Roman", 5)
    c.drawRightString(50, 60, "Invoice No. :")
    c.drawString(55, 60, invoice.token_id)
    c.drawRightString(50, 70, "Date :")
    c.drawString(55, 70, invoice.date)
    c.drawRightString(50, 80, "Customer Name :")
    c.drawString(55, 80, invoice.customer_name)
    c.drawRightString(50, 90, "Phone No. :")
    c.drawString(55, 90, invoice.contact_number)
    c.drawRightString(50, 100, "Delivery Address: ")
    c.drawString(55, 100, invoice.delivery_address)
    c.roundRect(10, 108, 180, 130, 0, stroke=1, fill=0)
    c.drawCentredString(20, 117, "S.No.")
    c.drawCentredString(55, 117, "Orders")
    c.drawCentredString(105, 117, "Rate")
    c.drawCentredString(130, 117, "Dis.")
    c.drawCentredString(149, 117, "Qty.")
    c.drawCentredString(170, 117, "Total")
    
    total = 0
    for y_index, item in enumerate(invoice.cuisines):
        c.drawCentredString(18, 127 + (y_index * 10), str(y_index+1))
        c.drawCentredString(55, 127 + (y_index * 10) , str(item["name"]))
        c.drawCentredString(105, 127 + (y_index * 10), "Rs."+str(item["rate"]))
        c.drawCentredString(130, 127 + (y_index * 10), str(item["discount"]))
        c.drawCentredString(149, 127 + (y_index * 10), str(item["quantity"]))
        c.drawCentredString(170, 127 + (y_index * 10), "Rs."+str(item["total"]))
        total += item["total"]



    # total 
    c.drawCentredString(170, 215, "Rs."+str(total))

    c.drawString(30, 230, "This is system generated invoice!!")
    c.drawRightString(180, 228, "Keep it safe")
    c.drawRightString(180, 235, "Signature")
    # c.showPage()
    c.save()

    return True
