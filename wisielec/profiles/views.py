from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


def login_view(request, template="game/login.html"):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/game/new")
        else:
            error = "Invalid username or password"

    return render(request, template, locals())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/game/new")