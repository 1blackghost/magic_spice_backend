# Generated by Django 4.2.6 on 2024-07-12 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_order_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
