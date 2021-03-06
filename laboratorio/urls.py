from django.urls import path
from . import views

urlpatterns = [

    path('cadastro_laboratorio/', views.cadastrar_lab, name='cadastrar_lab'),
    path('login_lab/', views.login_lab, name='login_lab'),
    path('', views.dash_lab, name='dash_lab'),
    path('logout', views.logout_lab, name='logout_lab'),
    path('editar_lab/<int:lab_id>', views.editar_lab, name='editar_lab'),
    path('exames/', views.listar_exames_laboratorio, name='listar_exames_laboratorio')
]