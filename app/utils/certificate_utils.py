from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime


def generate_certificate(agent_name, application_no, expiry_date):

    folder = "certificates"

    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = f"{folder}/{application_no}.pdf"

    c = canvas.Canvas(file_path, pagesize=A4)

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(300, 800, "AP RERA RENEWAL CERTIFICATE")

    c.setFont("Helvetica", 14)

    c.drawString(100, 700, f"Agent Name : {agent_name}")
    c.drawString(100, 670, f"Application No : {application_no}")
    c.drawString(100, 640, f"Expiry Date : {expiry_date}")

    c.drawString(100, 600, "This certificate confirms that the renewal")
    c.drawString(100, 580, "application has been approved by AP RERA.")

    c.drawString(100, 520, f"Issue Date : {datetime.today().date()}")

    c.save()

    return file_path