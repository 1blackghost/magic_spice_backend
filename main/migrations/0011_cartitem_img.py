# Generated by Django 4.2.6 on 2024-07-12 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_productdb_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='img',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
