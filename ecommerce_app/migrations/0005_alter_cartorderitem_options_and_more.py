# Generated by Django 5.1.1 on 2025-01-30 15:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0004_cartorderproduct_item_alter_contact_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartorderitem',
            options={'verbose_name_plural': 'Cart Order Item'},
        ),
        migrations.AlterModelOptions(
            name='cartorderproduct',
            options={'verbose_name_plural': 'Cart Order Product'},
        ),
        migrations.AddField(
            model_name='address',
            name='address',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 30, 16, 46, 37, 551331)),
        ),
        migrations.AlterField(
            model_name='contact',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 30, 16, 46, 37, 551331)),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 30, 16, 46, 37, 552325)),
        ),
        migrations.AlterField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 30, 16, 46, 37, 552325)),
        ),
    ]
