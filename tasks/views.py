from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError  # los valores deben ser unicos
from .forms import TaskForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task
# Create your views here.


def home(request):
    return render(request, 'home.html')

#funcion para registrar usuario
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        # comprobar contraseñas coincidan
        if request.POST['password1'] == request.POST['password2']:
            try:
                # registrar usuario
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                )
                user.save()
                # creamos la cookie con login
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'el usuario ya existe'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'las contraseñas no coinciden '
        })


#mostrar las tareas sin completar
@login_required
def tasks(request):
    #listar tareas solo de usuarios actual logueado
    #tasks = Task.objects.filter(user=request.user)
    #mostrar tareas que falten completar
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks':tasks})

#mostrar las tareas completadas
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})


# FUNCION para crera nueva tarea
@login_required
def create_task(request):
    # si el metodo es get muestra el formulario
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })

    else:
        try:
            # se envia por el metodo post
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)#el commit false no permite que se guarde
            # obtenemos el usuario
            new_task.user = request.user
            # se guarda la tarea con el usuario obtenido
            new_task.save()
            return redirect('tasks')
        except ValueError:
             return render(request, 'create_task.html', {
            'form': TaskForm,
            'error':'Error al ingresar los Datos'
        })

# FUNCION para el detalle de las tareas
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        #print(task_id)
        #task = Task.objects.get(pk=task_id)
        task = get_object_or_404(Task, pk=task_id, user=request.user)#evita la caida del server , el usuario debe coincideir con el user actual
        form =  TaskForm(instance=task)#llenara el form con la tarea 
        return render(request, 'task_detail.html', {'task':task, 'form':form})
    else:
        try:
            #obtener los datos
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form =  TaskForm(request.POST ,instance=task)
            form.save()
            return redirect('tasks') 
        except ValueError:
            return render(request, 'task_detail.html', {
                'task':task, 
                'form':form,
                'error':'Error al actualizar los datos'
                })
            
# FUNCION para completar taraea
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks') 

# FUNCION para elimnar taraea
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks') 
    
 # funcion para cerrar la sesion del usuario
def signout(request):
    logout(request)
    return redirect('home')

# funcion para el inicio de la sesion del usuario
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            "form": AuthenticationForm
        })
    else:
        # si passan datos usar authenticate
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'], )
        # si el usuario esta vacio
        if user is None:
            # no fue valido
            return render(request, 'signin.html', {
                "form": AuthenticationForm,
                'error': 'Usuario Invalido'
            })
        else:
            # si el usuario exite entonces
            # guarddamos la sesion
            login(request, user)
            return redirect('tasks')
