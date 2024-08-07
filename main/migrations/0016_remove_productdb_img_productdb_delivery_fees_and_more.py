# Generated by Django 4.2.6 on 2024-07-13 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_order_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productdb',
            name='img',
        ),
        migrations.AddField(
            model_name='productdb',
            name='delivery_fees',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='productdb',
            name='img1',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='productdb',
            name='img2',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='productdb',
            name='img3',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='productdb',
            name='other_fees',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='productdb',
            name='percentage',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='productdb',
            name='tax',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_id',
            field=models.CharField(max_length=100),
        ),
    ]
