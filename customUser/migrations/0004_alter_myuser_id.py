# Generated by Django 4.2 on 2023-05-03 21:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customUser', '0003_myuser_groups_myuser_user_permissions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
