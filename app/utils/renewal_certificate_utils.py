from reportlab.pdfgen import canvas
import os
import qrcode
from datetime import datetime
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from datetime import datetime, timedelta




def generate_certificate(agent_name, registration_no, expiry_date):

    folder = "app/uploads/certificates"

    os.makedirs(folder, exist_ok=True)

    file_path = f"{folder}/renewal_{registration_no}.pdf"

    c = canvas.Canvas(file_path)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, 750, "AP RERA RENEWAL CERTIFICATE")

    c.setFont("Helvetica", 12)

    c.drawString(100, 680, f"Agent Name: {agent_name}")
    c.drawString(100, 650, f"Registration No: {registration_no}")
    c.drawString(100, 620, f"Renewal Valid Till: {expiry_date.date()}")

    c.drawString(100, 580, "Your RERA Agent Registration has been renewed.")

    c.save()

    return file_path


def generate_certificate2(agent_name, registration_no, expiry_date):

    try:

        folder = "app/uploads/certificates"

        os.makedirs(folder, exist_ok=True)

        file_path = f"{folder}/renewal_{registration_no}.pdf"

        c = canvas.Canvas(file_path)

        # Title
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(300, 750, "AP RERA RENEWAL CERTIFICATE")

        # Sub heading
        c.setFont("Helvetica", 12)
        c.drawCentredString(300, 720, "Andhra Pradesh Real Estate Regulatory Authority")

        # Certificate Body
        c.setFont("Helvetica", 12)

        c.drawString(100, 650, f"Agent Name : {agent_name}")
        c.drawString(100, 620, f"Registration Number : {registration_no}")
        c.drawString(100, 590, f"Renewal Valid Till : {expiry_date}")

        c.drawString(100, 550, "This is to certify that the above mentioned agent")
        c.drawString(100, 530, "has successfully renewed their RERA Registration.")

        c.drawString(100, 500, "This certificate is issued by AP RERA.")

        # Issue Date
        today = datetime.today().strftime("%d-%m-%Y")
        c.drawString(100, 450, f"Issue Date : {today}")

        # Signature area
        c.drawString(400, 400, "Authorized Signatory")
        c.drawString(400, 380, "AP RERA")

        c.save()

        print("Certificate generated:", file_path)

        return file_path

    except Exception as e:

        print("Certificate generation error:", str(e))

        return None
    
    
    

# def generate_project_certificate(project):

#     try:
#         folder = "app/uploads/certificates"
#         os.makedirs(folder, exist_ok=True)

#         file_path = f"{folder}/project_{project['application_no']}.pdf"

#         c = canvas.Canvas(file_path)

#         # =========================
#         # HEADER
#         # =========================
#         c.setFont("Helvetica-Bold", 18)
#         c.drawCentredString(300, 780, "PROJECT CERTIFICATE")

#         c.setFont("Helvetica", 12)
#         c.drawCentredString(300, 755, "Andhra Pradesh Real Estate Regulatory Authority")

#         # =========================
#         # LINE
#         # =========================
#         c.line(50, 740, 550, 740)

#         # =========================
#         # BODY
#         # =========================
#         c.setFont("Helvetica", 12)

#         c.drawString(80, 700, f"Application No      : {project['application_no']}")
#         c.drawString(80, 670, f"Project Name        : {project.get('project_name', '-')}")
#         c.drawString(80, 640, f"Promoter Name       : {project.get('name', '-')}")
#         c.drawString(80, 610, f"Promoter Type       : {project.get('promoter_type', '-')}")
#         c.drawString(80, 580, f"PAN Number          : {project.get('pan_number', '-')}")

#         c.drawString(80, 550, f"Project Type        : {project.get('project_type', '-')}")
#         c.drawString(80, 520, f"District            : {project.get('project_district', '-')}")
#         c.drawString(80, 490, f"Address             : {project.get('project_address', '-')}")

#         # =========================
#         # APPROVAL TEXT
#         # =========================
#         c.drawString(80, 440, "This is to certify that the above project")
#         c.drawString(80, 420, "has been APPROVED by AP RERA authority.")

#         c.drawString(80, 390, "This certificate is issued as per RERA regulations.")

#         # =========================
#         # ISSUE DATE
#         # =========================
#         today = datetime.today().strftime("%d-%m-%Y")
#         c.drawString(80, 340, f"Issue Date : {today}")

#         # =========================
#         # SIGNATURE
#         # =========================
#         c.drawString(400, 300, "Authorized Signatory")
#         c.drawString(400, 280, "AP RERA")

#         # Footer line
#         c.line(50, 260, 550, 260)

#         c.save()

#         print("Project Certificate generated:", file_path)

#         return file_path

#     except Exception as e:
#         print("Certificate error:", str(e))
#         return None
def generate_project_certificate(project):

    try:
        folder = "app/uploads/certificates"
        os.makedirs(folder, exist_ok=True)

        file_path = f"{folder}/project_{project['application_no']}.pdf"

        # QR CODE
        qr_data = f"Project: {project['application_no']}"
        qr_path = f"{folder}/qr_{project['application_no']}.png"
        qr = qrcode.make(qr_data)
        qr.save(qr_path)

        # Certificate Number & Validity
        cert_number = f"APRERA-{project['application_no']}"
        issue_date = datetime.today()
        validity_date = issue_date + timedelta(days=1825)  # 5 years

        # DOCUMENT
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        styles = getSampleStyleSheet()

        elements = []

        # =========================
        # STYLES
        # =========================
        center = ParagraphStyle(name='center', alignment=1, fontSize=12, leading=16)
        title = ParagraphStyle(name='title', alignment=1, fontSize=18, leading=22, spaceAfter=10)
        body = ParagraphStyle(name='body', fontSize=11, leading=16)

        # =========================
        # LOGO (TOP CENTER)
        # =========================
        logo_path = "app/static/ap_rera_logo.png"  # 👉 place logo here
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=1.5*inch, height=1.5*inch)
            logo.hAlign = 'CENTER'
            elements.append(logo)

        elements.append(Paragraph("<b>GOVERNMENT OF ANDHRA PRADESH</b>", title))
        elements.append(Paragraph("<b>ANDHRA PRADESH REAL ESTATE REGULATORY AUTHORITY (AP RERA)</b>", center))

        elements.append(Spacer(1, 10))

        elements.append(Paragraph("<b>PROJECT REGISTRATION CERTIFICATE</b>", title))

        elements.append(Spacer(1, 15))

        # =========================
        # CERTIFICATE DETAILS
        # =========================
        elements.append(Paragraph(f"<b>Certificate No:</b> {cert_number}", body))
        elements.append(Paragraph(f"<b>Issue Date:</b> {issue_date.strftime('%d-%m-%Y')}", body))
        elements.append(Paragraph(f"<b>Valid Till:</b> {validity_date.strftime('%d-%m-%Y')}", body))

        elements.append(Spacer(1, 15))

        # =========================
        # MAIN TEXT
        # =========================
        elements.append(Paragraph(
            "This is to certify that the following project has been registered with AP RERA "
            "under the Real Estate (Regulation and Development) Act, 2016.",
            body
        ))

        elements.append(Spacer(1, 15))

        # =========================
        # TABLE
        # =========================
        data = [
            ["Application No", project['application_no']],
            ["Project Name", project.get('project_name', '-')],
            ["Promoter Name", project.get('name', '-')],
            ["Promoter Type", project.get('promoter_type', '-')],
            ["PAN Number", project.get('pan_number', '-')],
            ["District", project.get('project_district', '-')],
            ["Address", project.get('project_address', '-')],
        ]

        table = Table(data, colWidths=[2.5*inch, 4*inch])
        table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
        ]))

        elements.append(table)

        elements.append(Spacer(1, 20))

        # =========================
        # FOOTER (QR + SIGNATURE)
        # =========================
        qr_img = Image(qr_path, width=1.2*inch, height=1.2*inch)

        sign_path = "app/static/signature.png"  # 👉 place signature image here
        if os.path.exists(sign_path):
            sign_img = Image(sign_path, width=2*inch, height=1*inch)
        else:
            sign_img = Paragraph("Authorized Signatory", body)

        footer = Table([
            [qr_img, "", sign_img],
            ["Scan to Verify", "", "AP RERA"]
        ], colWidths=[2*inch, 2*inch, 2*inch])

        footer.setStyle(TableStyle([
            ('ALIGN', (2,0), (2,1), 'RIGHT'),
            ('ALIGN', (0,0), (0,1), 'LEFT')
        ]))

        elements.append(footer)

        # =========================
        # BUILD PDF WITH BORDER
        # =========================
        def add_border(canvas, doc):
            canvas.saveState()

            # BORDER
            canvas.setLineWidth(2)
            canvas.rect(30, 30, A4[0]-60, A4[1]-60)

            # WATERMARK
            canvas.setFont("Helvetica", 40)
            canvas.setFillGray(0.9)
            canvas.drawCentredString(300, 400, "AP RERA")

            canvas.restoreState()

        doc.build(elements, onFirstPage=add_border)

        print("✅ Premium Certificate Generated:", file_path)
        return file_path

    except Exception as e:
        print("❌ Error:", str(e))
        return None