# Generated by Django 4.1.6 on 2023-02-20 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_order_customid'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipping',
            name='first_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='country',
            field=models.CharField(blank=True, default='India', max_length=100, null=True),
        ),
    ]
