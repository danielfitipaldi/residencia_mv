from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_med/', views.cadastrar_med, name='cadastrar_med'),
    path('login_med/', views.login_med, name='login_med'),
    path('logout_med', views.logout_med, name='logout_med'),
    path('editar_med/<int:med_id>', views.editar_med, name='editar_med'),
    path('dash_med/', views.dash_med, name='dash_med'),
    path('deletar_med/<int:med_id>', views.deletar_med, name='deletar_med'),
    path('meu_perfil/', views.visualizar_perfil_med, name='visualizar_perfil_med'),


    path('adicionar_paciente/', views.adicionar_paciente, name='adicionar_paciente'),
    path('lista_pacientes', views.lista_pacientes, name='lista_pacientes'),
    path('excluir_paciente/<int:paciente_id>', views.excluir_paciente, name='excluir_paciente'),
]