"""Send the digest over SMTP (Gmail app password works). One BCC'd message per run."""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def recipients(path="recipients.txt"):
    if not os.path.exists(path):
        raise SystemExit(f"{path} missing. Copy recipients.example.txt and add one email per line.")
    with open(path) as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]


def send(subject, html_body, text_body, to):
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "465"))
    user, pw = os.environ.get("SMTP_USER"), os.environ.get("SMTP_PASSWORD")
    if not (user and pw):
        raise SystemExit("SMTP_USER / SMTP_PASSWORD not set (see README, .env).")
    sender = os.environ.get("MAIL_FROM", user)
    msg = MIMEMultipart("alternative")
    msg["Subject"], msg["From"], msg["To"] = subject, sender, sender
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    with smtplib.SMTP_SSL(host, port) as s:
        s.login(user, pw)
        s.sendmail(sender, [sender] + to, msg.as_string())
