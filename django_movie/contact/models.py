from django.db import models

class Contact(models.Model):
    """Подписка на email"""

    email = models.EmailField()
    data = models.DateTimeField("Дата подписки", auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
