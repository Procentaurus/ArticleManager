# Generated by Django 4.2 on 2023-05-03 21:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('internalAPI', '0005_remove_text_markedasfinal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='text',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
