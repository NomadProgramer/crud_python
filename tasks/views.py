from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {
                        "form": UserCreationForm
                        })

    else:
        if request.POST["password1"] == request.POST["password2"]:
            # registrer user
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"])
                user.save()
                login(request, user)
                print("------------------------------")
                print(request.POST)
                print(type(request.POST))
                print("---------------------------------")
                return redirect("tasks")
            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": "User exist"
                })

        print(request.POST)
        print("Obteniendo datos")

        return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": "Password deosent match"
                })


def tasks(request):
    tasks = Task.objects.all()
    return render(request, "Tasks.html", {"tasks": tasks})


def signout(request):
    logout(request)
    return redirect("home")


def login_in(request):
    if request.method == "GET":
        return render(request, "sign_in.html", {
            "form": AuthenticationForm
        })
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"])
        print(request.POST)
        if user is None:
            return render(request, "sign_in.html", {
                "form": AuthenticationForm,
                "error": "Username or password is incorrect"
            })
        else:
            login(request, user)
            return redirect("tasks")


def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {
            "form": TaskForm,
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            # print(new_task)
            new_task.user = request.user
            new_task.save()
            return render(request, "create_task.html", {
                "form": TaskForm,
                "info": "Tarea creada"
            })
        except ValueError:
            return render(request, "create_task.html", {
                "form": TaskForm,
                "error": "Introduce valid data"
            })
