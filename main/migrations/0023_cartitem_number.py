# Generated by Django 4.2.6 on 2024-07-15 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_productdb_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='number',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
