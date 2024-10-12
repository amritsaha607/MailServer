# Generated by Django 5.0.6 on 2024-10-02 05:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_alter_mailevent_receivers'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paylaod', models.TextField()),
                ('received_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
