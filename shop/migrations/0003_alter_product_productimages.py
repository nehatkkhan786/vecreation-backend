# Generated by Django 4.1.6 on 2023-02-02 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_productimages_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productImages',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.productimages'),
        ),
    ]
