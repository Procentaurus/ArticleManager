# Generated by Django 4.2 on 2023-05-03 10:35

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
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('title', models.CharField(max_length=60, unique=True)),
                ('isAvailable', models.BooleanField(blank=True, default=True)),
                ('addingDate', models.DateField(auto_now_add=True)),
                ('numberOfDownloads', models.IntegerField(blank=True, default=0)),
                ('manager', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]