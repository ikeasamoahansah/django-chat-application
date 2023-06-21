from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.


def lobby(request):
    return render(request, 'chat/lobby.html')

@login_required(login_url='/admin')
def create_room(request):
    if request.method == 'GET':
        return render(request, 'chat/create_room.html')
    elif request.method == 'POST':
        name = request.POST['name']
        
        room = Room(name=name, creator=request.user)
        room.save()

        return redirect('')

@login_required(login_url='/admin')
def room(request, pk):

    room_get = Room.objects.get(id=pk)

    if room_get:
        return render(request, 'chat/room.html', {
            "rooms": Room.objects.all()
        })
        