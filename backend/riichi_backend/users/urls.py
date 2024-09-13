from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('list_users/', views.list_users, name='list_users'),
    path('list_match_result/', views.list_match_result, name='list_match_result'),
    path('list_match_arrangement/', views.list_match_arrangement, name='list_match_arrangement'),
    path('addUser/', views.addUser, name='addUser'),
    path('listUser/', views.listUser, name='listUser'),
    path('editUser/', views.editUser, name='editUser'),
    path('deleteUser/', views.deleteUser, name='deleteUser'),
    path('uploadMatchArrangement/', views.uploadMatchArrangement, name='uploadMatchArrangement'),
    path('uploadMatchResult/', views.uploadMatchResult, name='uploadMatchResult'),
    path('deleteMatchArrangement/', views.deleteMatchArrangement, name='deleteMatchArrangement'),
    path('get_user_info/', views.get_user_info, name='get_user_info'),
    path('change_password/', views.change_password, name='change_password'),
]
