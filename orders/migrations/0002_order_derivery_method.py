# Generated by Django 4.1.4 on 2024-02-14 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='derivery_method',
            field=models.CharField(choices=[('1', 'Colissimo'), ('2', 'Chronopost')], default='1', max_length=10),
        ),
    ]
