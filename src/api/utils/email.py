from fastapi import BackgroundTasks, UploadFile
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from src.config.config import settings


def send_email_background(
    background_tasks: BackgroundTasks,
    subject: str,
    email_to: str,
    body: dict,
    attachment: UploadFile,
    template_name: str | None = None,
):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype="html",
        attachments=[attachment],
    )
    config = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM="noreply@testmail.com",
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_STARTTLS=settings.MAIL_STARTTLS,
        MAIL_SSL_TLS=False,
        TEMPLATE_FOLDER="src/api/utils/templates/email",
    )
    fm = FastMail(config)
    if not template_name:
        template_name = "base_email.html"
    background_tasks.add_task(fm.send_message, message, template_name=template_name)
