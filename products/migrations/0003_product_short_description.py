# Generated by Django 3.0.3 on 2020-02-25 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.TextField(blank=True, default=True, null=True),
        ),
    ]
