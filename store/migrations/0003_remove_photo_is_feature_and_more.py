# Generated by Django 4.1.4 on 2024-04-13 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='is_feature',
        ),
        migrations.RemoveField(
            model_name='variationimages',
            name='is_feature',
        ),
    ]
