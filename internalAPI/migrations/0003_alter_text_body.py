# Generated by Django 4.2 on 2023-04-30 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internalAPI', '0002_alter_text_author_alter_text_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='body',
            field=models.TextField(),
        ),
    ]
