# Generated by Django 3.2.5 on 2024-04-24 06:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mygroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('member', models.ManyToManyField(related_name='mygroup', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mygroupchats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chats', models.JSONField(default=dict)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupchat', to='chatApp.mygroup')),
            ],
        ),
    ]
