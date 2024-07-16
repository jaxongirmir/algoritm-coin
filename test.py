from dataclasses import dataclass
from os import getenv
from pathlib import Path
import smtplib
from typing import Any
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template

GMAIL = getenv("GMAIL", "your_email@gmail.com")
GMAIL_PASSWORD = getenv("GMAIL_PASSWORD", "your_password")
SMTP_HOST = getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = getenv("SMTP_PORT", "587")


def send_email(subject, text, addresses):
    message = MIMEMultipart()
    message["From"] = GMAIL
    message["To"] = ", ".join(addresses)
    message["Subject"] = subject
    message.attach(MIMEText(text, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, int(SMTP_PORT)) as smtp:
            smtp.ehlo()  # Can be omitted
            smtp.starttls()
            smtp.ehlo()  # Can be omitted
            smtp.login(user=GMAIL, password=GMAIL_PASSWORD)
            smtp.sendmail(from_addr=GMAIL, to_addrs=addresses, msg=message.as_string())
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent.parent / "coin" / "static" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


# Example usage
send_email(
    "Algoritm Coin parol tiklash",
    render_email_template(
        template_name="reset_password.html",
        context={"fullname": "test", "link": f"/reset-password?token=123"},
    ),
    ["sanjar68x@gmail.com"],  # Corrected email address
)
