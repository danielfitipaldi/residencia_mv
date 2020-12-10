from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from laboratorio.views import is_not_lab
from .form import FormUsuario, UserForm, FormExames
from django.contrib import auth, messages
from django.core.validators import validate_email
from .models import Usuario, Exames


def home(request):
    return render(request, 'usuario/home.html')


def login(request):
    if request.method != 'POST':
        return render(request, 'usuario/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha não encontrados')
        return render(request, 'usuario/login.html')
    else:
        auth.login(request, user)
        messages.success(request, f'Você está logado como {user}')
        return redirect('dash_user')


@login_required(redirect_field_name='login', login_url='login')
@user_passes_test(lambda user: is_not_usuario(user), redirect_field_name='login',
                  login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


def is_not_usuario(user):
    """
    Verifica se o usuário não pertence a um determinado grupo
    e retorna True caso pertença.
    """
    if user:
        return user.groups.filter(name='usuarios').exists()
    return False


@login_required(redirect_field_name='login', login_url='login')
@user_passes_test(lambda user: is_not_usuario(user), redirect_field_name='login',
                  login_url='login')
def dash_user(request):
    current_user = request.user.id
    usuario = get_object_or_404(Usuario, usuario_id=current_user)
    contexto = {'usuario': usuario}

    return render(request, 'usuario/dash.html', contexto)


def cadastrar(request):
    Group.objects.get_or_create(name='usuarios')

    form1 = UserForm(request.POST or None)
    form2 = FormUsuario(request.POST or None)
    if request.method != 'POST':
        form1 = UserForm()
        form2 = FormUsuario()
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    username = request.POST.get('username')
    senha = request.POST.get('senha')
    confirmar_senha = request.POST.get('confirmar_senha')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    cpf = request.POST.get('cpf')
    email = request.POST.get('email')

    # Validações

    # USUÁRIO

    if not username or not senha or not confirmar_senha or not first_name or not last_name or not cpf or not email:
        messages.error(request, 'Todos os campos devem ser preenchidos')
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Nome de usuário já existe')
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    # CPF

    if len(cpf) != 11:
        messages.error(request, 'CPF inválido')
        form1 = UserForm()
        form2 = FormUsuario()
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    # SENHA

    if senha != confirmar_senha:
        messages.error(request, 'Senhas não coincidem')
        form1 = UserForm()
        form2 = FormUsuario()
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    if len(senha) < 8:
        messages.error(request, 'As senhas devem ter 8 dígitos')
        form1 = UserForm()
        form2 = FormUsuario()
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    # E-MAIL
    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já cadastrado')
        return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})

    if form1.is_valid():
        user = form1.save(commit=False)
        raw_password = form1.cleaned_data['senha']
        user.set_password(raw_password)
        form1.save()
        grupo = Group.objects.get(name='usuarios')
        user.groups.add(grupo)
        if form2.is_valid():
            usuario = form2.save(commit=False)
            usuario.usuario = user
            form1.save()
            form2.save()
            messages.success(request, 'Usuário cadastrado com sucesso')
            return redirect('login')

    return render(request, 'usuario/pag_cadastro.html', {'form1': form1, 'form2': form2})


# Editar cadastro
@login_required(redirect_field_name='login', login_url='login')
@user_passes_test(lambda user: is_not_usuario(user), redirect_field_name='login',
                  login_url='login')
def editar(request, usuario_id):
    obj = get_object_or_404(Usuario, id=usuario_id)

    user = request.POST.get('usuario')
    email = request.POST.get('email')
    cpf = request.POST.get('cpf')

    form1 = UserForm(request.POST or None, instance=obj.usuario)
    form2 = FormUsuario(request.POST or None, instance=obj)

    if form1.is_valid() and form2.is_valid():
        try:
            validate_email(email)
        except:
            messages.error(request, 'E-mail inválido')
            form1 = UserForm()
            form2 = FormUsuario()
            return render(request, 'usuario/editar_cadastro.html', {'form1': form1, 'form2': form2})

        if len(cpf) != 11:
            messages.error(request, 'CPF inválido')
            form1 = UserForm()
            form2 = FormUsuario()
            return render(request, 'usuario/editar_cadastro.html', {'form1': form1, 'form2': form2})

        user = form1.save(commit=False)
        raw_password = form1.cleaned_data['senha']
        user.set_password(raw_password)
        if form2.is_valid():
            usuario = form2.save(commit=False)
            usuario.usuario = user
            form1.save()
            form2.save()

        messages.success(request, 'Cadastro atualizado')
        return HttpResponseRedirect('dash')

    return render(request, 'usuario/editar_cadastro.html', {'form1': form1, 'form2': form2})


@login_required(redirect_field_name='login', login_url='login')
@user_passes_test(lambda user: is_not_usuario(user), redirect_field_name='login',
                  login_url='login')
def listar(request):
    usuarios = Usuario.objects.order_by('-id')

    return render(request, 'usuario/lista_usuarios.html', {
        'usuarios': usuarios
    })


@login_required(redirect_field_name='login', login_url='login')
@user_passes_test(lambda user: is_not_usuario(user), redirect_field_name='login',
                  login_url='login')
def deletar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == "GET":
        usuario.delete()
        messages.success(request, 'Usuário apagado com sucesso')
        return redirect('home')

    return render(request, "usuario/delete_usuario.html")


@login_required(redirect_field_name='login', login_url='login')
@user_passes_test(lambda user: is_not_usuario(user), redirect_field_name='login',
                  login_url='login')
def detalhe_perfil(request, perfil_id):
    usuario = get_object_or_404(Usuario, id=perfil_id)

    return render(request, 'usuario/detalhe_perfil.html', {
        'usuario': usuario
    })


# EXAMES
@login_required(redirect_field_name='login', login_url='login')
@user_passes_test(lambda user: is_not_usuario(user), redirect_field_name='login',
                  login_url='login')
def novo_exame(request):
    form = FormExames(request.POST or None)
    current_user = request.user.id
    user = get_object_or_404(User, id=current_user)

    if request.method != 'POST':
        return render(request, 'usuario/cadastrar_exame.html', {'form': form})

    if form.is_valid():
        exame = form.save(commit=False)
        exame.paciente = user
        form.save()
        messages.success(request, 'Exame cadastrado com sucesso')
        return redirect('dash_user')

    return render(request, 'usuario/cadastrar_exame.html', {'form': form})


@login_required(redirect_field_name='login', login_url='login')
@user_passes_test(lambda user: is_not_usuario(user), redirect_field_name='login',
                  login_url='login')
def listar_exames_usuario(request):
    current_user = request.user.id
    exames = Exames.objects.filter(paciente_id=current_user)

    return render(request, 'usuario/exames_por_usuario.html', {
        'exames': exames
    })


@login_required(redirect_field_name='login', login_url='login')
@user_passes_test(lambda user: is_not_usuario(user) or is_not_lab(user), redirect_field_name='login',
                  login_url='login')
def detalhe_exame(request, exame_id):
    exame = get_object_or_404(Exames, id=exame_id)

    return render(request, 'usuario/detalhe_exame.html', {
        'exame': exame
    })


@login_required(redirect_field_name='login', login_url='login')
@user_passes_test(lambda user: is_not_usuario(user), redirect_field_name='login',
                  login_url='login')
def graficos_exames(request):
    return render(request, 'usuario/area_grafica.html')


@login_required(redirect_field_name='login', login_url='login')
@user_passes_test(lambda user: is_not_usuario(user) or is_not_lab(user), redirect_field_name='login',
                  login_url='login')
def excluir_exame(request, exame_id):
    exame = get_object_or_404(Exames, id=exame_id)

    if request.method == 'GET':
        exame.delete()
        messages.success(request, 'Exame apagado com sucesso')
        return HttpResponseRedirect('/dashboard/meus_exames/')

    return render(request, 'usuario/delete_exame.html')
