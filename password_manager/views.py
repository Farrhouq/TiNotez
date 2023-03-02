from django.shortcuts import render, redirect
import random
from password_manager.logic.shuffle import shuffle
from password_manager.logic.gen_pass import gen_pass
from password_manager.logic.farsan import farsan_encrypt, farsan_decrypt
from django.contrib import messages

# Create your views here.

my_password = "doyfiukpscutu"


def home(request):
    with open("/home/farouq/PycharmProjects/pythonProject2/haash.txt") as file:
        password_sets = file.readlines()
        file.close()

    password_dict = {}

    for set in password_sets:
        site = set.split(":")[0]
        password = set.split(": ")[1].strip()
        password_dict[site] = len(password)*'*'

    context = {"passwords": password_dict}
    return render(request, "passwords.html", context)


def authenticate(request):
    line = request.GET.get("line")
    if request.method == "POST":
        password = request.POST.get("password")
        print(password)
        if password == farsan_decrypt(my_password):
            return redirect("password", line)
        else:
            messages.error(request, "Wrong Password!")

    return render(request, "auth.html", {})


def password(request, line):
    with open("/home/farouq/PycharmProjects/pythonProject2/haash.txt") as file:
        password_set = file.readlines()[line]
        file.close()

    wherefrom = request.META.get("HTTP_REFERER") if request.META.get(
        "HTTP_REFERER") is not None else ""
    # print("wherefrom?:", wherefrom)
    if "http://127.0.0.1:10000/password-manager/auth?line=" not in wherefrom:
        return redirect(f"http://127.0.0.1:10000/password-manager/auth?line={line}")

    site = password_set.split(": ")[0].strip()
    password = password_set.split(": ")[1].strip()
    context = {"site": site, "password": farsan_decrypt(password)}
    return render(request, "password.html", context)
