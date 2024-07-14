# Generated by Django 4.2.6 on 2024-07-14 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_productdb_customer_care_productdb_fssai_info_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdb',
            name='customer_care',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='productdb',
            name='fssai_info',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='productdb',
            name='key_features',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='productdb',
            name='return_policy',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='productdb',
            name='seller_details',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='productdb',
            name='shelf_life',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
    ]
