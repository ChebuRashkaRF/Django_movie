from django_movie.celery import app

from .service import send, send_spam
from .models import Contact


@app.task
def send_spam_mail(user_email):
    send(user_email)


@app.task
def send_beat_email():
    for contact in Contact.objects.all():
        send_spam(contact)
