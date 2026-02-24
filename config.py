import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("YOUR_EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("YOUR_EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
