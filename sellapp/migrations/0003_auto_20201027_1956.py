# Generated by Django 3.0.2 on 2020-10-27 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellapp', '0002_auto_20201027_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Mobile', 'Mobile'), ('Bike', 'Bike'), ('Cycle', 'Cycle'), ('Electronics', 'Electronics'), ('Furnitures', 'Furnitures')], max_length=20),
        ),
    ]
