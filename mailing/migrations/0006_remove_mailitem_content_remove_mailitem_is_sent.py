# Generated by Django 5.0.6 on 2024-10-02 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0005_rawevent_chain_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailitem',
            name='content',
        ),
        migrations.RemoveField(
            model_name='mailitem',
            name='is_sent',
        ),
    ]
