from reportlab.pdfgen import canvas
import os

class Invoice:
    def __init__(self, customer_name, contact_number, token_id, date):
        self.customer_name = customer_name
        self.contact_number = contact_number
        self.token_id = token_id
        self.date=date
        self.cuisines = []
    
    def add_cuisine(self, name, quantity, rate):
        self.cuisines.append(
            {
                "name": name,
                "quantity": quantity,
                "rate": rate,
                "total": quantity * rate
            }
        )

def generate_pdf(invoice):
    os.makedirs("gen-invoice-pdfs", exist_ok=True)
    
    c = canvas.Canvas("gen-invoice-pdfs/invoice_{}.pdf".format(invoice.token_id), pagesize=(200, 250), bottomup=0)
    c.setFillColorRGB(7/255, 14/255, 23/255)
    c.line(70, 22, 180, 22)
    c.line(5, 45, 195, 45)
    c.line(15, 120, 185, 120)
    c.line(35, 108, 35, 220)
    c.line(110, 108, 110, 220)
    c.line(140, 108, 140, 220)
    c.line(155, 108, 155, 220)
    c.line(15, 220, 185, 220)
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
    c.setFont("Times-Bold", 6)
    # c.drawCentredString(125, 42, "GST No:"+self.gst.get())
    c.setFont("Times-Bold", 8)
    c.drawCentredString(100, 55, "INVOICE")
    c.setFont("Times-Bold", 5)
    c.drawRightString(70, 70, "Invoice No. :")
    c.drawRightString(100, 70, invoice.token_id)
    c.drawRightString(70, 80, "Date :")
    c.drawRightString(120, 80, invoice.date)
    c.drawRightString(70, 90, "Customer Name :")
    c.drawRightString(120, 90, invoice.customer_name)
    c.drawRightString(70, 100, "Phone No. :")
    c.drawRightString(100, 100, invoice.contact_number)
    c.roundRect(15, 108, 170, 130, 2, stroke=1, fill=0)
    c.drawCentredString(25, 118, "S.No.")
    c.drawCentredString(75, 118, "Orders")
    c.drawCentredString(120, 118, "Price")
    c.drawCentredString(148, 118, "Qty.")
    c.drawCentredString(170, 118, "Total")
    
    total = 0
    for y_index, item in enumerate(invoice.cuisines):
        c.drawCentredString(25, 135 + (y_index * 10), str(y_index+1))
        c.drawCentredString(75, 135 + (y_index * 10) , str(item["name"]))
        c.drawCentredString(120, 135 + (y_index * 10), "Rs."+str(item["rate"]))
        c.drawCentredString(148, 135 + (y_index * 10), str(item["quantity"]))
        c.drawCentredString(170, 135 + (y_index * 10), "Rs."+str(item["total"]))
        total += item["total"]



    # total 
    c.drawCentredString(170, 200, "Rs."+str(total))

    c.drawString(30, 230, "This is system generated invoice!!")
    c.drawRightString(180, 228, "Keep it safe")
    c.drawRightString(180, 235, "Signature")
    # c.showPage()
    c.save()

    return True
