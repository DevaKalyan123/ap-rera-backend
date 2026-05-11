from sqlalchemy import text
from app.models.database import db
from app.utils.mail_service import send_email
from apscheduler.schedulers.background import BackgroundScheduler


def send_payment_reminders(app):
    with app.app_context():

        print("🔄 Running payment reminder job...")

        query = text("""
            SELECT 
                id,
                renewal_application_no,
                payment_status,
                email
            FROM agent_renewal_t
            WHERE payment_status = 'PENDING'
        """)

        results = db.session.execute(query).fetchall()

        print(f"Found {len(results)} pending payments")

        for row in results:
            print("📧 Sending email to:", row.email)

            subject = "Payment Reminder - AP RERA Renewal"

            message = f"""
Dear Applicant,

Your renewal application {row.renewal_application_no} is still pending payment.

Please complete your payment as soon as possible.

Regards,
AP RERA
"""

            send_email(row.email, subject, message)

            print("✅ Email sent")


def start_scheduler(app):   # ✅ accept app
    print("🚀 Scheduler started...")

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        send_payment_reminders,
        'interval',
         hours=124,
         args=[app]   # ✅ VERY IMPORTANT
    )

    scheduler.start()