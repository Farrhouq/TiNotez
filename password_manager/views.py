from django.shortcuts import render, redirect
from django.contrib import messages
from github import Github, InputFileContent

from password_manager.logic.gen_pass import gen_pass
from password_manager.logic.farsan import farsan_encrypt, farsan_decrypt


my_password = "doyfiukpscutu"
auth_line = "/password-manager/auth?line="
gist_id = "78hf7898wjhfnihjgh21"


def gg():
    """Reinstantiates and resets the Github class and gist to make sure it's always up to date"""
    global g, gist
    g = Github(
        farsan_decrypt(
            "IqcOc_wA1gKmUiT8dY1iWrCUuHcF_tPobh6HZCtxEG0kKxKavRb2vYmBp3YmzZ80A_bFpah8A0bMDA1TKGhuZMwfsyzhh"
        )
    )
    gist = g.get_gist(gist_id)


def tgg():
    try:
        gg()
    except:
        return redirect("password_manager:auth")


def process(string: str):
    """You won't understand. It's meant for you not to. Yeah, you."""

    def position_of(letter):
        lc = [le for le in "abcdefghijklmnopqrstuvwxyz"]
        return lc.index(letter) + 1

    i = "2a89342090ab8219e5d5f05fd799bd6a"
    if len(string) >= 13:
        s = farsan_decrypt(string)
        i_ = [char for char in i]
        for t in range(len(i_)):
            if i_[t] == string[12]:
                i_[t] = string[2]
        t2 = position_of(string[7]) - position_of(string[0])
        i_[t2] = position_of(string[6]) - t2
        global gist_id
        gist_id = farsan_decrypt("".join([str(i) for i in i_]))


def auth(request):
    if request.method == "POST":
        password = request.POST.get("password")
        process(password)

        try:
            gg()
            return redirect("password_manager:home")
        except:
            return redirect("password_manager:auth")

    return render(request, "authe.html", {})


def wherefrom_authenticate(request, wherefrom_url, redirect_url):
    wherefrom = (
        request.META.get("HTTP_REFERER")
        if request.META.get("HTTP_REFERER") is not None
        else ""
    )
    if wherefrom_url not in wherefrom:
        return redirect(redirect_url)


# Create your views here.


def home(request):
    if tgg() is not None:
        return tgg()
    password_sets = gist.files["haash.txt"].content.split("\n")
    password_dict = {}
    for set in password_sets:
        site = set.split(":")[0]
        password = set.split(": ")[1].strip()
        password_dict[site] = len(password) * "*"
    context = {"passwords": password_dict}
    return render(request, "passwords.html", context)


def authenticate(request):
    line = request.GET.get("line")
    if request.method == "POST":
        password = request.POST.get("password")
        if password == farsan_decrypt(my_password):
            if line.isnumeric():
                return redirect("password_manager:password", line)
            elif line == "add":
                return redirect("password_manager:add")
        else:
            messages.error(request, "Wrong Password!")
    return render(request, "auth.html", {})


def password(request, line):
    if tgg() is not None:
        return tgg()
    password_set = gist.files["haash.txt"].content.split("\n")[line]
    site = password_set.split(": ")[0].strip()
    password = password_set.split(": ")[1].strip()

    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        if confirm == "on":
            if new_password != "":
                lines = gist.files["haash.txt"].content.split("\n")
                lines[line] = f"{site}: {farsan_encrypt(new_password)}\n"
                gist.edit(files={gist_id: InputFileContent("\n".join(line))})
                messages.success(request, f"Password updated")
                return redirect("password_manager:password", line)
            else:
                messages.error(request, "No password inputed")

    if "/password-manager/passwords/" not in request.META.get("HTTP_REFERER"):
        to_redirect = wherefrom_authenticate(request, auth_line, f"{auth_line}{line}")
        if to_redirect is not None:
            return to_redirect

    context = {"site": site, "password": farsan_decrypt(password)}
    return render(request, "password.html", context)


def add_password(request):
    # The function itself was just making me sad. I don't even know what it's doing...
    sites = []
    lines = gist.files["haash.txt"].content.split("\n")
    for line in lines:
        sites.append(line.split(": ")[0])

    if request.method == "POST":
        site = request.POST.get("site")
        password = farsan_encrypt(request.POST.get("password"))

        # Important: The code starting from here...
        index_found = None
        # I think this part is just like the terminal version...
        if tgg() is not None:
            return tgg()
        file_lines = gist.files["haash.txt"].content.split("\n")
        for line in file_lines:
            if site == line.split(": ")[0]:
                index_found = file_lines.index(line)
                file_lines[index_found] = f"{site}: {password}\n"
                break

        if index_found is None:
            lines = gist.files["haash.txt"].content.split("\n")
            lines.append(f"{site}: {password}\n")
            gist.edit(files={"haash.txt": InputFileContent("".join(lines))})
            messages.success(
                request, f"The password for {site} has been saved successfully"
            )
        else:
            gist.edit(files={"haash.txt": InputFileContent("".join(file_lines))})
            messages.success(request, f"The password for {site} has been updated")
        # and ends here was written once without fault and without intermittent testing (1:04AM, April 9, 2023)

    to_redirect = wherefrom_authenticate(request, auth_line, f"{auth_line}add")
    if to_redirect is not None:
        if "/password-manager/add" in request.META.get("HTTP_REFERER"):
            return redirect("password_manager:home")
        return to_redirect
    return render(request, "add.html", {"sites": sites})


def generate_password(request):
    password = None
    sites = []
    lines = gist.files["haash.txt"].content.split("\n")
    for line in lines:
        sites.append(line.split(": ")[0])
    context = {"sites": sites}
    if request.method == "POST":
        site = request.POST.get("site")
        length = int(request.POST.get("length"))
        password = gen_pass(length)
        context.update({"password": password, "length": length, "site": site})
    return render(request, "generate.html", context)


def save(request):
    if request.method != "POST":
        if request.META.get("HTTP_REFERER") is None:
            return redirect("password_manager:home")
        return redirect(request.META.get("HTTP_REFERER"))

    site = request.POST.get("site")
    save_password = request.POST.get("save-password")
    passcode = request.POST.get("password")

    sites = []
    if passcode == farsan_decrypt(my_password):
        # Let's save the password, give a message, and redirect me.
        # First of all, let's check for replacements
        replacement = False
        if tgg() is not None:
            return tgg()
        lines = gist.files["haash.txt"].content.split("\n")
        for line in lines:
            sites.append(line.split(": ")[0])
        if site in sites:
            line_found = sites.index(site)
            replacement = True
        else:
            lines = gist.files["haash.txt"].content.split("\n")
            lines.append(f"{site}: {farsan_encrypt(save_password)}\n")
            gist.edit(files={"haash.txt": InputFileContent("".join(lines))})
            messages.success(
                request, f"Your password for {site} has been saved successfully"
            )
            return redirect("password_manager:password", line)

        if replacement:
            lines[line_found] = f"{site}: {farsan_encrypt(save_password)}\n"
            gist.edit(files={"haash.txt": InputFileContent("".join(lines))})
            messages.success(request, f"Your password for {site} has been updated")
            return redirect("password_manager:home")
    else:
        # Let's check if the person is from 'save' which will mean that
        # the person just entered a wrong password
        if "/password-manager/save" in request.META.get("HTTP_REFERER"):
            messages.error(request, "Wrong Password!")
    context = {"site": site, "save_password": save_password, "page": "save"}
    return render(request, "auth.html", context)


# Reading
# content = gist.files[gist_id].content

# Writing
# gist.edit(files={gist_id: InputFileContent("new content")})
