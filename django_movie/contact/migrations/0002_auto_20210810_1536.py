# Generated by Django 3.2.6 on 2021-08-10 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'Контакт', 'verbose_name_plural': 'Контакты'},
        ),
        migrations.AlterField(
            model_name='contact',
            name='data',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки'),
        ),
    ]