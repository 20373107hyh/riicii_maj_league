# Generated by Django 5.0.3 on 2024-09-10 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_match_arrangements_player_4_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='grade',
            field=models.CharField(default='none', max_length=50),
        ),
    ]
