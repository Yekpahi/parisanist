# Generated by Django 4.1.4 on 2024-04-04 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_payment_intent'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]