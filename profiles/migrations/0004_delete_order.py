# Generated by Django 3.2 on 2023-10-08 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_remove_userprofile_order_history'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
