# Generated by Django 4.2.5 on 2023-10-20 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('username', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
            ],
            options={
                'db_table': 'user_user_profile',
            },
        ),
    ]
