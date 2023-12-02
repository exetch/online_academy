from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_course_update_email(user_email, course_title):
    subject = f"Обновление в курсе {course_title}"
    message = f"Уважаемый пользователь, курс '{course_title}' был обновлен. Приглашаем вас ознакомиться с новыми материалами."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email, ]
    send_mail(subject, message, email_from, recipient_list)