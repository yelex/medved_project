# Generated by Django 3.0.3 on 2020-02-27 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200224_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comments',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]