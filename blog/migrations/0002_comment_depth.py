# Generated by Django 3.2.6 on 2021-08-08 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='depth',
            field=models.PositiveIntegerField(blank=True, default=1, verbose_name='Глубина вложенности'),
            preserve_default=False,
        ),
    ]
