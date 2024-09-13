import datetime
import json
from datetime import timedelta

import pytz
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from users.models import UserInfo, match_results, match_arrangements


def turn_to_beijing_time(received_time):
    time = received_time.isoformat()
    dt = datetime.datetime.fromisoformat(time.replace('Z', '+00:00'))
    # 将其转换为北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = dt.astimezone(beijing_tz)
    return beijing_time


@csrf_exempt
def login(request):
    print(request.body)
    info = json.loads(request.body.decode('utf-8'))
    username = info['username']
    password = info['password']
    current_user = UserInfo.objects.filter(user_name = username).first()
    if current_user is None:
        print(2)
        return JsonResponse({'errno': 100002, 'msg': '用户不存在'})
    if password != current_user.password:
        print(3)
        return JsonResponse({'errno': 100003, 'msg': '密码错误'})
    if not request.session.session_key:
        request.session.save()  # 保存之后生成session_key，之后前端以此为标头请求后端
    session_id = request.session.session_key
    print(f"Session ID: {request.session.session_key}")
    print(f"Session UID: {request.session.get('uid')}")
    data = {
        'user_id': current_user.user_id,
        'username': current_user.user_name,
        'password': current_user.password,
        'session_id': session_id,
        'role': current_user.role
    }
    return JsonResponse({'errno': 100000, 'msg': '登陆成功', 'data': data})


@csrf_exempt
def logout(request):
    return JsonResponse({'errno': 100000, 'msg': '登出成功'})


@csrf_exempt
def list_users(request):
    try:
        user_list = UserInfo.objects.all()
        user_info_list = []
        for user in user_list:
            if user.role == 1:
                continue
            match_time = 0
            match_point = 0
            results_as_player_1 = match_results.objects.filter(match__player_1=user)
            for result in results_as_player_1:
                match_time += 1
                match_point += result.player_1_result
            results_as_player_2 = match_results.objects.filter(match__player_2=user)
            for result in results_as_player_2:
                match_time += 1
                match_point += result.player_2_result
            results_as_player_3 = match_results.objects.filter(match__player_3=user)
            for result in results_as_player_3:
                match_time += 1
                match_point += result.player_3_result
            user_info = {
                'user_name': user.user_name,
                'grade': user.grade,
                'match_time': match_time,
                'match_point': match_point,
            }
            user_info_list.append(user_info)
        sorted_user_info_list = sorted(user_info_list, key=lambda k: k['match_point'], reverse=True)
        return JsonResponse({'errno': 100000, 'msg': '用户查询成功', 'data': sorted_user_info_list})
    except Exception as e:
        return JsonResponse({'errno': 100001, 'msg': str(e)})


@csrf_exempt
def list_match_result(request):
    try:
        match_result_list = match_results.objects.all()
        result_list_in_array = []
        for match_result in match_result_list:
            match_time = match_result.match.match_time
            match_time = turn_to_beijing_time(match_time)
            match_time = match_time.strftime('%Y 年 %m 月 %d 日 %H:%M:%S')
            result_json = {
                'match_id': match_result.match.match_id,
                'match_time': match_time,
                'player_1': match_result.match.player_1.user_name,
                'player_2': match_result.match.player_2.user_name,
                'player_3': match_result.match.player_3.user_name,
                'player_1_result': match_result.player_1_result,
                'player_2_result': match_result.player_2_result,
                'player_3_result': match_result.player_3_result,
                'player_1_points': match_result.player_1_points,
                'player_2_points': match_result.player_2_points,
                'player_3_points': match_result.player_3_points,
            }
            result_list_in_array.append(result_json)
        # result_list_in_array = sorted(result_list_in_array, key=lambda k: k['match_time'], reverse=True)
        return JsonResponse({'errno': 100000, 'msg': '比赛结果查询成功', 'data': result_list_in_array})
    except Exception as e:
        return JsonResponse({'errno': 100001, 'msg': str(e)})


@csrf_exempt
def list_match_arrangement(request):
    # try:
    match_arrangement_list = match_arrangements.objects.all()
    match_arrangement_list_in_array = []
    for match_arrangement in match_arrangement_list:
        player_1_points = 'none'
        player_2_points = 'none'
        player_3_points = 'none'
        player_1_result = 'none'
        player_2_result = 'none'
        player_3_result = 'none'
        match_time = match_arrangement.match_time
        match_time = turn_to_beijing_time(match_time)
        match_time = match_time.strftime('%Y 年 %m 月 %d 日 %H:%M:%S')
        if match_results.objects.filter(match=match_arrangement).exists():
            match_result = match_results.objects.filter(match=match_arrangement).first()
            player_1_points = match_result.player_1_points
            player_2_points = match_result.player_2_points
            player_3_points = match_result.player_3_points
            player_1_result = match_result.player_1_result
            player_2_result = match_result.player_2_result
            player_3_result = match_result.player_3_result
        match_arrangement_json = {
                'match_id': match_arrangement.match_id,
                'match_time': match_time,
                'player_1': match_arrangement.player_1.user_name,
                'player_2': match_arrangement.player_2.user_name,
                'player_3': match_arrangement.player_3.user_name,
                'player_1_result': player_1_result,
                'player_2_result': player_2_result,
                'player_3_result': player_3_result,
                'player_1_points': player_1_points,
                'player_2_points': player_2_points,
                'player_3_points': player_3_points,
        }
        match_arrangement_list_in_array.append(match_arrangement_json)
    # match_arrangement_list_in_array = sorted(match_arrangement_list_in_array, key=lambda k: k['match_time'], reverse=True)
    return JsonResponse({'errno': 100000, 'msg': '比赛赛程查询成功', 'data': match_arrangement_list_in_array})
    # except Exception as e:
    #     return JsonResponse({'errno': 100001, 'msg': str(e)})


@csrf_exempt
def addUser(request):
    user_name = request.POST.get('user_name')
    password = request.POST.get('password')
    role = request.POST.get('role')
    role = int(role)
    new_user = UserInfo(user_name=user_name, password=password, role=role)
    new_user.save()
    return JsonResponse({'errno': 100000, 'msg': '新用户创建成功'})


@csrf_exempt
def listUser(request):
    users = UserInfo.objects.all()
    user_list = []
    for user in users:
        user_json = {
            'user_id': user.user_id,
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
def uploadMatchArrangement(request):
    match_time = request.POST.get('match_time')
    match_time = parse_datetime(match_time)
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
    player_1_point = request.POST.get('player_1_points')
    player_1_point = int(player_1_point)
    player_1_result = request.POST.get('player_1_result')
    player_1_result = float(player_1_result)
    player_2_point = request.POST.get('player_2_points')
    player_2_point = int(player_2_point)
    player_2_result = request.POST.get('player_2_result')
    player_2_result = float(player_2_result)
    player_3_point = request.POST.get('player_3_points')
    player_3_point = int(player_3_point)
    player_3_result = request.POST.get('player_3_result')
    player_3_result = float(player_3_result)
    if match_results.objects.filter(match=match).exists():
        match_result = match_results.objects.get(match=match)
        match_result.player_1_points = player_1_point
        match_result.player_2_points = player_2_point
        match_result.player_3_points = player_3_point
        match_result.player_1_result = player_1_result
        match_result.player_2_result = player_2_result
        match_result.player_3_result = player_3_result
        match_result.save()
    else:
        match_result = match_results(
            match = match,
            player_1_points = player_1_point,
            player_2_points = player_2_point,
            player_3_points = player_3_point,
            player_1_result = player_1_result,
            player_2_result = player_2_result,
            player_3_result = player_3_result,
            paipu_id=0,
        )
        match_result.save()
    return JsonResponse({'errno': 100000, 'msg': '比赛结果上传成功'})


@csrf_exempt
def get_user_info(request):
    user_id = request.POST.get('user_id')
    current_user = UserInfo.objects.get(user_id=user_id)
    data = {
        'user_id': current_user.user_id,
        'user_name': current_user.user_name,
        'password': current_user.password,
        'role': current_user.role,
    }
    return JsonResponse({'errno': 100000, 'msg': '请求用户信息成功', 'data': data})


@csrf_exempt
def change_password(request):
    user_id = request.POST.get('user_id')
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    sure_password = request.POST.get('sure_password')
    if UserInfo.objects.filter(user_id=user_id, password=old_password).exists():
        if new_password != sure_password:
            return JsonResponse({'errno': 100001, 'msg': '两次密码不一致'})
        user = UserInfo.objects.get(user_id=user_id)
        user.password = new_password
        user.save()
        return JsonResponse({'errno': 100000, 'msg': '密码修改成功'})
    return JsonResponse({'errno': 100002, 'msg': '原始密码错误'})