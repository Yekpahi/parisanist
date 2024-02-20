# Generated by Django 4.1.4 on 2024-02-20 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('product_image', models.ImageField(upload_to='stactic/photos/', verbose_name='image')),
                ('photo_slug', models.SlugField(blank=True, null=True)),
                ('is_feature', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=500)),
                ('product_slug', models.SlugField()),
                ('product_price', models.FloatField()),
                ('product_stock', models.IntegerField(default=True)),
                ('product_discountprice', models.FloatField(blank=True, null=True)),
                ('product_description', models.TextField(blank=True, null=True)),
                ('product_cleaning', models.TextField(blank=True, null=True)),
                ('product_home_carousel_image', models.ImageField(upload_to='static/cover/')),
                ('is_active', models.BooleanField(default=False)),
                ('is_active_active_on_home_carousel', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variation_category', models.CharField(choices=[('color', 'color'), ('size', 'size')], max_length=100)),
                ('variation_value', models.CharField(max_length=100)),
                ('is_available', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
            ],
            options={
                'verbose_name_plural': 'wishlists',
            },
        ),
    ]
