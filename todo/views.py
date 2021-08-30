from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from datetime import datetime

# Create your views here.
def home(request):
	return render(request, 'todo/home.html')

def signupuser(request):
	if request.method == 'GET':
		return render(request, 'todo/signup.html')
	else:
		# Create new user
		if(request.POST['password'] == request.POST['cpassword']):
			print("passwords match lets create new user {}\n".format(request.POST['username']))
			try:
				user = User.objects.create_user(username=request.POST['username'],password=request.POST['password'])
				user.save()
				login(request,user)
				return redirect('currenttodos')
			except IntegrityError:
				return render(request, 'todo/signup.html', {'error':'Username already taken !'})
		else:
			print("passwords don't match !")
			return render(request, 'todo/signup.html', {'error':'Passwords don\'t match, try again !'})

def loginuser(request):
	if request.method == 'GET':
		return render(request, 'todo/login.html')
	else:
		user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
		print(request.POST['username'],request.POST['password'], user)
		if user is not None:
		    # A backend authenticated the credentials
		    login(request,user)
		    return redirect('currenttodos')
		else:
		    # No backend authenticated the credentials
		    return render(request, 'todo/login.html', {'error':'Username and password did not match !'})


def logoutuser(request):
	if request.method == 'POST':
		logout(request)
		return redirect('loginuser')


def currenttodos(request):
	if request.user.is_authenticated:
		if request.method == "GET":
			todos = Todo.objects.filter(user=request.user, status=False)
			return render(request, 'todo/todo.html', {'form':TodoForm(), 'todos':todos, 'pendingList':True})
		else: #POST
			try:
				form = TodoForm(request.POST)
				newtodo = form.save(commit=False)
				newtodo.user = request.user
				newtodo.save()
				return redirect('currenttodos')
			except ValueError:
				return render(request, 'todo/todo.html', {'form':TodoForm(), 'error':'Bad input. try again !'})
	else:
		return render(request, 'todo/home.html', {'error':'Please login to view !'})

# view and create new todo
def viewtodo(request, todo_pk):
	todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
	
	if request.method == "GET":
		form = TodoForm(instance=todo)
		return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
	else:
		try:
			form = TodoForm(request.POST, instance=todo)
			form.save()
			return redirect('currenttodos')
		except ValueError:
			return render(request, 'todo/viewtodo.html', {'form':form, 'error':'Bad input. try again !'})

def completetodo(request, todo_pk):
	todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
	todo.status = True
	todo.datecompleted = datetime.now()
	todo.save()
	return redirect('currenttodos')

def deletetodo(request, todo_pk, pending):
	todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
	todo.delete()
	if pending == "current":
		return redirect('currenttodos')
	else:
		return redirect(completedtodos)

def completedtodos(request):
	if request.method == "GET":
		todos = Todo.objects.filter(user=request.user, status=True)
		return render(request, 'todo/todo.html', {'form':TodoForm(), 'todos':todos, 'pendingList':False})
	else: #POST
		try:
			form = TodoForm(request.POST)
			newtodo = form.save(commit=False)
			newtodo.user = request.user
			newtodo.save()
			return redirect('currenttodos')
		except ValueError:
			return render(request, 'todo/todo.html', {'form':TodoForm(), 'error':'Bad input. try again !'})