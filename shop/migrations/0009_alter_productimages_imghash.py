# Generated by Django 4.1.6 on 2023-02-19 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_productimages_imghash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimages',
            name='imgHash',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]
