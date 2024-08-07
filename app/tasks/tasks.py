import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_config import celery
from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_picture(path: str) -> None:
    large_res = (1000, 500)
    small_res = (200, 100)
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized_large = image.resize(large_res)
    image_resized_small = image.resize(small_res)
    image_resized_large.save(
        f"app/static/images/resized_{large_res[0]}_{large_res[1]}_{image_path.name}"
    )
    image_resized_small.save(
        f"app/static/images/resized_{small_res[0]}_{small_res[1]}_{image_path.name}"
    )


@celery.task
def send_booking_confirmation_email(booking: dict, email_to: EmailStr) -> None:
    msg_content = create_booking_confirmation_template(booking, email_to)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)