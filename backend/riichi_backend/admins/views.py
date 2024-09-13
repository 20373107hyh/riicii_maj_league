import datetime

import pytz
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt

from users.models import UserInfo, match_arrangements, match_results


# Create your views here.
@csrf_exempt
def addUser(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    role = request.POST.get('role')
    role = int(role)
    new_user = UserInfo(username=username, password=password, role=role)
    new_user.save()
    return JsonResponse({'errno': 100000, 'msg': '新用户创建成功'})


@csrf_exempt
def listUser(request):
    users = UserInfo.objects.all()
    user_list = []
    for user in users:
        user_json = {
            'user_name': user.user_name,
            'password': user.password,
            'role': user.role,
            'grade': user.grade
        }
        user_list.append(user_json)
    return JsonResponse({'errno': 100000, 'msg': '用户查找成功', 'data': user_list})


@csrf_exempt
def deleteUser(request):
    user_id = request.POST.get('user_id')
    user = UserInfo.objects.filter(user_id=user_id).first()
    user.delete()
    return JsonResponse({'errno': 100000, 'msg': '用户删除成功'})


@csrf_exempt
def editUser(request):
    user_id = request.POST.get('user_id')
    user_name = request.POST.get('user_name')
    password = request.POST.get('password')
    role = request.POST.get('role')
    grade = request.POST.get('grade')
    user = UserInfo.objects.filter(user_id=user_id).first()
    user.password = password
    user.user_name = user_name
    user.role = role
    user.grade = grade
    user.save()
    return JsonResponse({'errno': 100000, 'msg': '用户修改成功'})


@csrf_exempt
def turn_to_beijing_time(received_time):
    time = received_time.isoformat()
    dt = datetime.datetime.fromisoformat(time.replace('Z', '+00:00'))
    # 将其转换为北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = dt.astimezone(beijing_tz)
    return beijing_time

@csrf_exempt
def uploadMatchArrangement(request):
    match_time = request.POST.get('match_time')
    print(match_time)
    match_time = parse_datetime(match_time)
    print(match_time)
    match_time = turn_to_beijing_time(match_time)
    player_1 = request.POST.get('player_1')
    player_1 = UserInfo.objects.filter(user_name=player_1).first()
    player_2 = request.POST.get('player_2')
    player_2 = UserInfo.objects.filter(user_name=player_2).first()
    player_3 = request.POST.get('player_3')
    player_3 = UserInfo.objects.filter(user_name=player_3).first()
    match = match_arrangements(
        match_time=match_time,
        player_1=player_1,
        player_2=player_2,
        player_3=player_3
    )
    match.save()
    return JsonResponse({'errno': 100000, 'msg': '比赛创建成功'})


@csrf_exempt
def deleteMatchArrangement(request):
    match_id = request.POST.get('match_id')
    match = match_arrangements.objects.filter(match_id=match_id).first()
    match.delete()
    return JsonResponse({'errno': 100000, 'msg': '比赛删除成功'})


@csrf_exempt
def uploadMatchResult(request):
    match_id = request.POST.get('match_id')
    match = match_arrangements.objects.filter(match_id=match_id).first()
    player_1_point = request.POST.get('player_1_point')
    player_1_point = int(player_1_point)
    player_1_result = request.POST.get('player_1_result')
    player_1_result = float(player_1_result)
    player_2_point = request.POST.get('player_2_point')
    player_2_point = int(player_2_point)
    player_2_result = request.POST.get('player_2_result')
    player_2_result = float(player_2_result)
    player_3_point = request.POST.get('player_3_point')
    player_3_point = int(player_3_point)
    player_3_result = request.POST.get('player_3_result')
    player_3_result = float(player_3_result)
    match_result = match_results(
        match = match,
        player_1_point = player_1_point,
        player_2_point = player_2_point,
        player_3_point = player_3_point,
        player_1_result = player_1_result,
        player_2_result = player_2_result,
        player_3_result = player_3_result
    )
    match_result.save()
    return JsonResponse({'errno': 100000, 'msg': '比赛结果上传成功'})
