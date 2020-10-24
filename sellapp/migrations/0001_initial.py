# Generated by Django 3.1.2 on 2020-10-20 18:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='Post')),
                ('phone', models.PositiveIntegerField()),
                ('category', models.CharField(choices=[('Mobile', 'Mobile'), ('Bike', 'Bike'), ('Cycle', 'Cycle'), ('Fridge', 'Fridge')], max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('Price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('commented_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellapp.post')),
            ],
        ),
    ]
