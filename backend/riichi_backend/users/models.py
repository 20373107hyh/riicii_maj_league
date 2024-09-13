from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.IntegerField()  ## admin: 1  user: 2
    grade = models.CharField(max_length=50, default='none')


class match_arrangements(models.Model):
    match_id = models.AutoField(primary_key=True)
    match_time = models.DateTimeField()
    player_1 = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='player_1')
    player_2 = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='player_2')
    player_3 = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='player_3')


class match_results(models.Model):
    match = models.ForeignKey(match_arrangements, on_delete=models.CASCADE)
    player_1_points = models.IntegerField(default=0)  # 最终得分
    player_1_result = models.FloatField(default=0)  # 打点
    player_2_points = models.IntegerField(default=0)
    player_2_result = models.FloatField(default=0)
    player_3_points = models.IntegerField(default=0)
    player_3_result = models.FloatField(default=0)
    paipu_id = models.CharField(max_length=100)


