# Generated by Django 5.0.4 on 2024-06-03 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0002_alter_lectures_crawleddate_alter_users_fcmtoken_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='centers',
            name='centerrealname',
            field=models.CharField(db_column='centerRealName', default='null', max_length=90, unique=True),
        ),
    ]
