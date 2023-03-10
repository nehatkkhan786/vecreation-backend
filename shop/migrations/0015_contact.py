# Generated by Django 4.1.6 on 2023-03-07 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_remove_category_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=12)),
                ('message', models.TextField()),
            ],
        ),
    ]
