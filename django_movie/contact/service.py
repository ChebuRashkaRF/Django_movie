from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Вы подписались на рассылку',
        'Мы будем присылать Вам много спама.',
        'django97.example@gmail.com',
        [user_email],
        fail_silently=False,
    )


def send_spam(contact):
    send_mail(
        'Вы подписались на рассылку',
        'Мы будем присылать Вам много спама каждые 5 минут.',
        'django97.example@gmail.com',
        [contact.email],
        fail_silently=False,
    )
