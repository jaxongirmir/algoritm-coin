from os import getenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


GMAIL = getenv("GMAIL", "")
GMAIL_PASSWORD = getenv("GMAIL_PASSWORD", "")
SMTP_HOST = getenv("SMTP_HOST", "")
SMTP_PORT = getenv("SMTP_PORT", "")


def send_email(subject, text, addresses):
    message = MIMEMultipart()
    message["From"] = GMAIL
    message["To"] = ", ".join(addresses)
    message["Subject"] = subject
    message.attach(MIMEText(text, "html"))

    smtp = smtplib.SMTP(SMTP_HOST, int(SMTP_PORT))
    try:
        smtp.starttls()
    except smtplib.SMTPHeloError:
        print("The server did not reply properly to the HELO greeting.")
    try:
        smtp.login(user=GMAIL, password=GMAIL_PASSWORD)
    except smtplib.SMTPHeloError:
        print("The server did not reply properly to the HELO greeting.")
        return
    except smtplib.SMTPAuthenticationError:
        print("The server did not accept the username/password combination.")
        return
    except smtplib.SMTPNotSupportedError:
        print("The AUTH command is not supported by the server.")
        return
    except smtplib.SMTPException:
        print("No suitable authentication method was found.")
        return

    message = message.as_string()
    smtp.sendmail(from_addr=GMAIL, to_addrs=addresses, msg=message)
    smtp.quit()


# # Example usage
# subject = "Test Email"
# body = "This is a test email."
# recipients = ["sanjar68x@gmail.com"]
# send_email(subject, body, recipients)
