# Generated by Django 5.0.6 on 2024-07-27 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailevent',
            name='receivers',
            field=models.ManyToManyField(related_name='received_mail_events', to='mailing.user'),
        ),
    ]
