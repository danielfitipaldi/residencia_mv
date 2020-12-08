from django.urls import path
from . import views

urlpatterns = [
    # CORPO
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dash_user, name='dash_user'),
    path('logout', views.logout, name='logout'),

    # USUÁRIO
    path('cadastro/', views.cadastrar, name='cadastrar'),
    path('editar/<int:usuario_id>', views.editar, name='editar'),
    path('deletar/<int:usuario_id>', views.deletar_usuario, name='deletar_usuario'),
    path('lista/', views.listar, name='listar'),


    # Dashboard
    path('dashboard/cadastrar_exame/', views.novo_exame, name='novo_exame'),
    path('dashboard/meus_exames/', views.listar_exames_usuario, name='listar_exames_usuario'),
    path('dashboard/meus_exames/<int:exame_id>', views.detalhe_exame, name='detalhe_exame'),
    path('dashboard/meu_perfil/<int:perfil_id>', views.detalhe_perfil, name='detalhe_perfil'),
    path('dashboard/meus_exames/graficos/', views.graficos_exames, name='graficos_exames')
]
