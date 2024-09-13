from django.urls import path
from . import views

urlpatterns = [
    path('addUser/', views.addUser, name='addUser'),
    path('listUser/', views.listUser, name='listUser'),
    path('editUser/', views.editUser, name='editUser'),
    path('deleteUser/', views.deleteUser, name='deleteUser'),
    path('uploadMatchArrangement/', views.uploadMatchArrangement, name='uploadMatchArrangement'),
    path('uploadMatchResul/', views.uploadMatchResult, name='uploadMatchResult'),
    path('deleteMatchArrangement/', views.deleteMatchArrangement, name='deleteMatchArrangement'),
]
