# Generated by Django 3.0.2 on 2020-10-24 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellapp', '0007_auto_20201024_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='posts/images/'),
        ),
    ]
