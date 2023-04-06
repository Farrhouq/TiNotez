from django.shortcuts import render
import random
from password_manager.logic.shuffle import shuffle
from password_manager.logic.gen_pass import gen_pass
from password_manager.logic import farsan

# Create your views here.

def home(request):
    with open("/home/farouq/PycharmProjects/pythonProject2/haash.txt") as file:
        password_sets = file.readlines()

    password_dict = {}

    for set in password_sets:
        site = set.split(":")[0]
        password = set.split(": ")[1].strip()
        password_dict[site] = farsan.farsan_decrypt(password)

    context = {"passwords":password_dict}
    return render(request, "passwords.html", context)
    