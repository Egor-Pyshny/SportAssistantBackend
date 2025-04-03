import os
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

from pydantic import EmailStr
from sendgrid import Mail, SendGridAPIClient


class MailSender(ABC):

    @abstractmethod
    def send_email(self, to_email: EmailStr, subject: str, content: str):
        pass


class SMTPClient(MailSender):

    def send_email(self, to_email: str | EmailStr, subject: str, content: str):
        message = MIMEMultipart()
        message["From"] = os.getenv("EMAIL_HOST_USER")
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(content, "html"))
        try:
            from_email = os.getenv("EMAIL_HOST_USER")
            smtp = SMTP(str(os.environ.get("EMAIL_HOST")), int((os.environ.get("EMAIL_PORT"))))  # type: ignore
            smtp.starttls()
            smtp.login(
                str(os.environ.get("EMAIL_HOST_USER")),
                str(os.environ.get("EMAIL_HOST_PASSWORD")),
            )
            smtp.sendmail(from_email, to_email, message.as_string())
            smtp.quit()
        except Exception as e:
            try:
                smtp.quit()
            except (AttributeError, NameError):
                pass
            raise e
