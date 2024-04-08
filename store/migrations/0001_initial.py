# Generated by Django 4.1.4 on 2024-04-01 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('colorCode', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
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
                ('product_price', models.PositiveIntegerField()),
                ('itemNumber', models.PositiveIntegerField(blank=True, null=True)),
                ('product_stock', models.IntegerField(default=1)),
                ('product_description', models.TextField(blank=True, null=True)),
                ('product_cleaning', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variation_number', models.PositiveBigIntegerField(blank=True, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VariationImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('variation_image', models.ImageField(upload_to='stactic/variation_images/', verbose_name='variation_image')),
                ('variation_image_slug', models.SlugField(blank=True, null=True)),
                ('is_feature', models.BooleanField(default=False)),
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
