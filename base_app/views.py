from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import os
import platform
import getpass
from .models import FileCategory


USER = getpass.getuser()
CATEGORIES = [d.name for d in FileCategory.objects.all()]
ROOT_DIR = f"C:\\Users\\{USER}\\Documents\\Notes"
if platform.system() == "Linux":
    ROOT_DIR = f"/home/{USER}/Documents/Notes"
directories = [os.fsencode(f"{ROOT_DIR}/{d.name}") for d in FileCategory.objects.all()]


def get_files():
    """Getting files in directories and making sure they are up to date"""
    global folder1_file_list, folder2_file_list, folder3_file_list, file_list_list, directories
    
    folder1_file_list, folder2_file_list, folder3_file_list = [], [], []
    file_list_list = [folder1_file_list, folder2_file_list, folder3_file_list]
    directories = [os.fsencode(f"{ROOT_DIR}/{d.name}") for d in FileCategory.objects.all()]

    for directory in directories:
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"):
                file_list_list[directories.index(directory)].append(filename)


# Create your views here.
def setup(request):
    try:
        get_files()
        return redirect('home')
    except:
        pass
    if request.method == "POST":
        data = request.POST
        folder1, folder2, folder3 = data.get(
            "folder1"), data.get("folder2"), data.get("folder3")
        # clear the database for FileCategories
        FileCategory.objects.all().delete()
        # create the folders using the names
        for name in [folder1, folder2, folder3]:
            if name:
                FileCategory.objects.create(name=name)
                os.makedirs(f"{ROOT_DIR}/{name.upper()}")
        get_files()
        return redirect('home')
    return render(request, "setup.html", {})


def home(request):
    try:
        get_files()
    except:
        return redirect('setup')
    open_file = request.GET.get("file")
    context = {}
    notes = []

    if open_file is not None:
        CATEGORIES = [d.name for d in FileCategory.objects.all()]
        for category in CATEGORIES:
            try:
                with open(f"{ROOT_DIR}/{category}/{open_file}", "r") as file_opened:
                    notes = file_opened.readlines()
                    context.update(
                        {"notes": notes, "file_category": f"{category.upper()}"})
                    break
            except FileNotFoundError:
                print("Exception:", category)
                print(CATEGORIES)
                if CATEGORIES.index(category) == len(CATEGORIES)-1:
                    return redirect("home")
    files = dict(zip([category.name.upper() for category in FileCategory.objects.all()], [
                 folder1_file_list, folder2_file_list, folder3_file_list]))
    context.update({"open_file": open_file, "files": files})
    return render(request, "home.html", context)


def save(request):
    if request.method == "POST":
        post_data = request.POST
        notes = post_data.get("notes")
        category = post_data.get("category")

        filename = str(post_data.get("hidden-filename")).strip()
        original_filename = str(post_data.get("original_filename")).strip()

        if original_filename != "" and original_filename != filename:
            for file_list in file_list_list:
                if original_filename in file_list:
                    os.rename(
                        f"{ROOT_DIR}/{CATEGORIES[file_list_list.index(file_list)]}/{original_filename}",
                        f"{ROOT_DIR}/{CATEGORIES[file_list_list.index(file_list)]}/{filename}",
                    )

        # If category is not None, then that means we're in a certain file or we're creating some file
        # and we've chosen a category.
        # Just double-checking that we have a category even though it's enforced using js in the frontend...
        if category is not None:
            with open(f"{ROOT_DIR}/{str(category).upper()}/{filename}", "w") as file:
                for note in notes:
                    file.write(note.rstrip("\n"))
    return redirect(f"/?file={filename}")
