from django.shortcuts import render, redirect
import random
from password_manager.logic.shuffle import shuffle
from password_manager.logic.gen_pass import gen_pass
from password_manager.logic.farsan import farsan_encrypt, farsan_decrypt
from django.contrib import messages
import json


def wherefrom_authenticate(request, wherefrom_url, redirect_url):
    wherefrom = request.META.get("HTTP_REFERER") if request.META.get(
        "HTTP_REFERER") is not None else ""

    if wherefrom_url not in wherefrom:
        return redirect(redirect_url)

# Create your views here.


my_password = "doyfiukpscutu"
auth_line = "/password-manager/auth?line="


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
        if password == farsan_decrypt(my_password):
            if line.isnumeric():
                return redirect("password", line)
            elif line == 'add':
                return redirect('add')
        else:
            messages.error(request, "Wrong Password!")
    return render(request, "auth.html", {})


def password(request, line):
    with open("/home/farouq/PycharmProjects/pythonProject2/haash.txt") as file:
        password_set = file.readlines()[line]
        # lines = file.readlines()
        file.close()

    site = password_set.split(": ")[0].strip()
    password = password_set.split(": ")[1].strip()

    if request.method == "POST":
        new_password = request.POST.get("password")
        if new_password != "":
            # Now let's actually change the password
            with open("/home/farouq/PycharmProjects/pythonProject2/haash.txt", "r") as file:
                lines = file.readlines()
                file.close()

            lines[line] = f"{site}: {farsan_encrypt(new_password)}\n"
            with open("/home/farouq/PycharmProjects/pythonProject2/haash.txt", "w") as file:
                for l in lines:
                    file.write(l)
                file.close()

            messages.success(
                request, f"The password of {site} has been updated")
            return redirect("password", line)
        else:
            messages.error(request, "No password inputed")

    if "/password-manager/passwords/" not in request.META.get("HTTP_REFERER"):
        to_redirect = wherefrom_authenticate(
            request, auth_line, f"{auth_line}{line}")
        if to_redirect is not None:
            return to_redirect

    context = {"site": site, "password": farsan_decrypt(password)}
    return render(request, "password.html", context)


def add_password(request):
    # The function itself was just making me sad. I don't even know what it's doing...
    sites = []
    with open("/home/farouq/PycharmProjects/pythonProject2/haash.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            sites.append(line.split(": ")[0])

    if request.method == "POST":
        site = request.POST.get("site")
        password = farsan_encrypt(request.POST.get("password"))

        # Important: The code starting from here...
        index_found = None
        with open("/home/farouq/PycharmProjects/pythonProject2/haash.txt", "r") as file:
            # I think this part is just like the terminal version...
            file_lines = file.readlines()
            for line in file_lines:
                if site == line.split(': ')[0]:
                    index_found = file_lines.index(line)
                    file_lines[index_found] = f"{site}: {password}\n"
                    file.close()
                    break

        if index_found is None:
            with open("/home/farouq/PycharmProjects/pythonProject2/haash.txt", "a") as file:
                file.write(f"{site}: {password}\n")
                messages.success(
                    request, f"The password for {site} has been saved successfully")
                file.close()
        else:
            with open("/home/farouq/PycharmProjects/pythonProject2/haash.txt", "w") as file:
                for line in file_lines:
                    file.write(line)
                messages.success(
                    request, f"The password for {site} has been updated")
        # and ends here was written once without fault and without intermittent testing (1:04AM, April 9, 2023)

    to_redirect = wherefrom_authenticate(request, auth_line, f"{auth_line}add")
    if to_redirect is not None:
        if "/password-manager/add" in request.META.get("HTTP_REFERER"):
            return redirect("home")
        return to_redirect

    return render(request, "add.html", {"sites": sites})
