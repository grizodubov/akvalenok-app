from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr,
) -> EmailMessage:
    email = EmailMessage()
    email["Subject"] = "Подтверждение"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Подтвердите запись на занятие</h1>
            Вы забронировали бассейн с {booking["date_from"]} по {booking["date_to"]}
        """,
        subtype="html",
    )
    return email
