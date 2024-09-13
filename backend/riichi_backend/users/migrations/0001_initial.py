# Generated by Django 5.0.3 on 2024-09-10 06:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='match_arrangements',
            fields=[
                ('match_id', models.AutoField(primary_key=True, serialize=False)),
                ('match_time', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('role', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='match_results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_1_result', models.FloatField()),
                ('player_2_result', models.FloatField()),
                ('player_3_result', models.FloatField()),
                ('player_4_result', models.FloatField()),
                ('paipu_id', models.CharField(max_length=100)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.match_arrangements')),
            ],
        ),
        migrations.AddField(
            model_name='match_arrangements',
            name='player_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_1', to='users.userinfo'),
        ),
        migrations.AddField(
            model_name='match_arrangements',
            name='player_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_2', to='users.userinfo'),
        ),
        migrations.AddField(
            model_name='match_arrangements',
            name='player_3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_3', to='users.userinfo'),
        ),
        migrations.AddField(
            model_name='match_arrangements',
            name='player_4',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_4', to='users.userinfo'),
        ),
    ]
