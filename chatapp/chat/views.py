from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from .forms import *

# Create your views here.

@login_required(login_url='/login')
def lobby(request):
    return render(request, 'chat/lobby.html', {"rooms": Room.objects.all()})


@login_required(login_url='/login')
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user
            room.save()
            return redirect('/lobby')
    else:
        form = RoomForm()
    return render(request, 'chat/create_room.html', {"form": form})



@login_required(login_url='/login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = Message.objects.filter(room=room)[0:25]
    return render(request, 'chat/room.html', {"room_id": pk, "user": request.user, "sender":request.user.username,"messages": messages})
        

def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/lobby')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {"form":form})


def login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/lobby')
        else:
            return render(request, "registration/login.html", {
                "msg": "Invalid login credentials"
            })
    else:
        return HttpResponse('<h1>Failed attempt to login</h1>')
        

@login_required(login_url='/login')
def search(request):
    query = request.GET.get('q')

    rooms = Room.objects.filter(name__icontains=query)

    context = {
        'query': query,
        'rooms': rooms
    }

    return render(request, 'chat/search.html', context)


def logout_view(request):
    logout(request)
    return redirect("login")