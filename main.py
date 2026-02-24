"""
Email Automation System
-----------------------
This script automates bulk email sending using:

✔️SMTP email sending
✔️CSV-based recipient management
✔️File attachment support
✔️Logging system for monitoring
✔️Daily scheduling automation

"""


import smtplib
import csv
from pathlib import Path
import logging
from email.message import EmailMessage
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT
import schedule
import time

# Logging Configuration
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(filename=LOGS_DIR / "email.log", level=logging.INFO,
                    format='%(asctime)s * %(levelname)s * %(message)s')

# Email sending function


def send_email(to_email, subject, body, html_body, attachment_path=None):

    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    # Email body content
    msg.set_content(body)
    msg.add_alternative(html_body, subtype="html")

    # Attachment Handling
    # If attachment path is provided, check if file exists before attaching

    if attachment_path:
        file_path = Path(attachment_path)

        if file_path.exists():
            with open(file_path, "rb") as file:
                file_data = file.read()
                msg.add_attachment(file_data, maintype="application",
                                   subtype="octet-stream", filename=file_path.name)

        else:
            logging.warning(f"⚠Attachment not found {attachment_path}")
            print(f"⚠️Attachment missing for {to_email}: {attachment_path}")

    # SMTP Server connection
    # Uses TLS encryption for secure communication

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            logging.info("Email sent successfully")
            print(f"✅Email sent to {to_email}")

    except Exception as e:
        logging.error(f"Failed to send email to {to_email}")
        print(f"❌Error sending email to {to_email} -> {e}")


def load_html_template(template_path, replacements):
    with open(template_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    for key, value in replacements.items():
        html_content = html_content.replace("{{" + key + "}}", value)

    return html_content


# Bulk Email Sender (CSV Driven)
# Reads recipient data from CSV file.
# Expected CSV format: name, email, attachment

def send_bulk_emails(csv_file):
    print("🚀Starting bulk email sending.....")
    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["name"].strip()
            email = row["email"].strip()

            # Personalized email content
            subject = f"Hello {name}, your automated message"
            attachment_path = row["attachment"].strip()
            body = f"Hi {name}, \n\nThis is a personalized automated email. \n\nBest regards, \nBrayo"
            html_body = load_html_template("template.html", {"name": name})
            send_email(email, subject, body, html_body,  attachment_path)

# Scheduler Job
# Function executed automatically by scheduler.


def scheduled_job():
    logging.info("Scheduled Job Started. ")
    send_bulk_emails("contacts.csv")
    logging.info("Scheduled Job Finished. ")

# Scheduler Starter
# Runs the automation system daily at a specified time.


def start_scheduler():

    schedule.every().day.at("00:00").do(scheduled_job)
    print("⏱️Scheduler started waiting for scheduled time...")
    logging.info("Scheduler started waiting for scheduled time...")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    start_scheduler()
