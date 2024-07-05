from django.shortcuts import render, redirect, get_object_or_404
from .models import Animal, Client
from agendamento.models import Agendamento
from django.contrib import messages
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ClientForm, AnimalForm
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.http import HttpResponse


def inicio(request):
    return render(request, '../templates/inicio.html')

def login(request):
    return render(request, '../templates/login.html')


# FUNCOES ---> CADASTRO E CONFIRMACAO DE USUARIO
User = get_user_model()

def register_client(request):
    if request.method == "GET":        
        return render(request, 'register_client.html')
    
    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirma_senha')

        user = User.objects.filter(email=email)

        if user.exists():            
            messages.add_message(request, messages.ERROR, 'E-mail já cadastrado em outro momento')
            return redirect(reverse('register_client'))                
        elif senha != confirma_senha:
            messages.add_message(request, messages.ERROR, 'As senhas digitadas não conferem')
            return redirect(reverse('register_client'))
        elif senha == '':
            messages.add_message(request, messages.ERROR, 'O campo senha é obrigatório')
            return redirect(reverse('register_client'))
        
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=senha, 
            first_name=nome, 
            last_name=sobrenome,
            is_active=False,  # Usuário inativo até confirmação do email
            cargo="C"
        )

        send_confirmation_email(user, request)  # Enviar email de confirmação

        messages.add_message(request, messages.SUCCESS, 'Usuário cadastrado com sucesso. Verifique seu email para confirmar o cadastro.')
        return redirect(reverse('login'))


def send_confirmation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))  # Não chame .decode() aqui
    confirm_url = reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})
    confirm_link = request.build_absolute_uri(confirm_url)

    subject = 'LOVE PETS - Confirme seu email'
    message = render_to_string('email_confirmation.html', {
        'user': user,
        'confirm_link': confirm_link
    })

    enviar_aviso(subject, message, [user.email])


def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email confirmado com sucesso!')
        return redirect('login')
    else:
        messages.error(request, 'Link de confirmação inválido ou expirado.')
        return redirect('register_client')


def enviar_aviso(subject, message, recipient_list):
    from_email = 'victor@emultec.com.br'
    
    # Cria uma mensagem de e-mail alternativa
    email = EmailMultiAlternatives(subject, message, from_email, recipient_list)
    
    # Define o conteúdo HTML da mensagem
    email.attach_alternative(message, "text/html")
    
    # Envia o e-mail
    email.send()
    return HttpResponse("E-mail de aviso enviado com sucesso.")



# FUNCOES ---> LOGIN E LOGOUT
def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            # redirect redireciona para a pagina desejada e o reverse tranforma o nome em um URL
            messages.add_message(request, messages.ERROR, 'Usuario ja logado')
            return redirect(reverse('register_client_info')) 
        return render(request, 'login.html')
    elif request.method == "POST": 
        login = request.POST.get('email')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=login, password=senha)

        if not user:
            messages.add_message(request, messages.ERROR, 'Usuario ou senha invalidos')
            return redirect(reverse('login'))
        
        auth.login(request,user)
        messages.add_message(request, messages.SUCCESS, 'Usuario logado com Sucesso')        
        return redirect(reverse('login'))
    
def logout(request):
    request.session.flush()
    messages.add_message(request, messages.WARNING, 'Logout efetuado com sucesso')
    return redirect(reverse('login'))



# FUNCOES ---> INFORMACOES ADICIONAIS CLIENTE 
@login_required
def register_client_info(request):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        client = None

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            if not validar_cpf(client.cpf):
                messages.error(request, 'CPF inválido. Por favor, verifique os dados e tente novamente.')
                return redirect('register_client_info')
            client.user = request.user
            client.save()
            messages.success(request, 'Dados complementares cadastrados com sucesso')
            return redirect('register_client_info')
    else:
        form = ClientForm(instance=client)

    estados_choices = Client._meta.get_field('estado').choices
    sexo_choices = Client._meta.get_field('sexo').choices

    context = {
        'estados_choices': estados_choices,
        'sexo_choices': sexo_choices,
        'form': form,
        'client': client
    }
    return render(request, 'register_client_info.html', context)

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10

    return digito1 == int(cpf[9]) and digito2 == int(cpf[10])



# FUNCOES ---> PET 
@login_required
def register_pet(request):
    try:
        client = get_object_or_404(Client, user=request.user)
    except:
        messages.error(request, 'Você precisa registrar suas informações de cliente antes de cadastrar um pet.')
        return redirect('register_client_info')  # Redireciona para a página de registro de informações do cliente

    if request.method == "POST":
        nome_pet = request.POST.get('nome_pet')
        raca = request.POST.get('raca')
        tipo_pelo = request.POST.get('tipo_pelo')
        porte = request.POST.get('porte')

        if not nome_pet or not raca or not tipo_pelo or not porte:
            messages.add_message(request, messages.ERROR, 'Todos os campos são obrigatórios.')
            return redirect(reverse('register_pet'))

        animal = Animal(
            nome=nome_pet,
            raca=raca,
            tipo_pelo=tipo_pelo,
            porte=porte,
            client=client
        )

        animal.save()

        messages.add_message(request, messages.SUCCESS, 'Pet cadastrado com sucesso')
        return redirect(reverse('inicio'))

    choices_pelo = Animal._meta.get_field('tipo_pelo').choices
    choices_porte = Animal._meta.get_field('porte').choices
    context = {
        'choices_pelo': choices_pelo,
        'choices_porte': choices_porte
    }
    return render(request, 'register_pet.html', context)        


@login_required
def listar_pets(request):
    try:
        client = Client.objects.get(user=request.user)
        pets = Animal.objects.filter(client=client, ativo=True)
    except Client.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('inicio')

    context = {
        'pets': pets,
    }
    return render(request, 'list_pets.html', context)


@login_required
def edit_pet(request, pet_id):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('inicio')

    animal = get_object_or_404(Animal, id=pet_id, client=client)

    if request.method == 'POST':
        pet_form = AnimalForm(request.POST, instance=animal)

        if pet_form.is_valid():
            pet_form.save()
            messages.success(request, 'Dados do pet atualizados com sucesso!')
            return redirect('listar_pets')
    else:
        pet_form = AnimalForm(instance=animal)

    context = {
        'pet_form': pet_form,
    }
    return render(request, 'edit_pet.html', context)

@login_required
def delete_pet(request, pet_id):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('inicio')

    animal = get_object_or_404(Animal, id=pet_id, client=client)

    if request.method == 'POST':
        if Agendamento.objects.filter(id_animal=animal).exists():            
            animal.ativo = False
            animal.save()
            messages.success(request, 'Pet inativado com sucesso!')
        else:
            animal.delete()
            messages.success(request, 'Pet apagado com sucesso!')
        return redirect('listar_pets')

    context = {
        'animal': animal,
    }
    return render(request, 'delete_pet.html', context)
