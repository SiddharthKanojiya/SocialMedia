# Generated by Django 3.2.5 on 2024-05-12 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0007_auto_20240512_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='dweet',
            name='likecount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
