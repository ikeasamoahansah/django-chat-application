from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from .forms import *

# Create your views here.


def lobby(request):
    return render(request, 'chat/lobby.html')

@login_required(login_url='/login')
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user
            room.save()
            return redirect('/')
        else:
            form = RoomForm()
    return render(request, 'chat/create_room.html', {"form":form})



@login_required(login_url='/login')
def room(request, pk):

    room_get = Room.objects.get(id=pk)

    if room_get:
        return render(request, 'chat/room.html', {
            "rooms": Room.objects.all()
        })
        

def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'chat/signup.html', {"form":form})


def login(request):
    if request.method == 'GET':
        return render(request, 'chat/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/home')
        else:
            return render(request, "registration/login.html", {
                "msg": "Invalid login credentials"
            })
    else:
        return HttpResponse('<h1>Failed attempt to login</h1>')


def logout_view(request):
    logout(request)
    return redirect("login")