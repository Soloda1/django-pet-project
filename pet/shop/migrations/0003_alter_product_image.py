# Generated by Django 5.1 on 2024-08-24 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='images/products/%Y/%m/%d', verbose_name='Изображение'),
        ),
    ]
