from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import os

CATEGORIES = ["ACADEMIA", "PROGRAMMING LIFE", "OTHER"]

ROOT_DIR = "/home/farouq/Documents/Notes"


# directories = [os.fsencode("/home/farouq/Documents/Notes/ACADEMIA"), 
#                 os.fsencode("/home/farouq/Documents/Notes/PROGRAMMING LIFE"), 
#                 os.fsencode("/home/farouq/Documents/Notes/OTHER"),
#                 ]

directories = [os.fsencode(f"{ROOT_DIR}/{d}") for d in CATEGORIES]

academia_file_list, programming_life_file_list, others_file_list = [], [], []
file_list_list = [academia_file_list, programming_life_file_list, others_file_list]


def get_files():
    global academia_file_list, programming_life_file_list, others_file_list, file_list_list
    academia_file_list, programming_life_file_list, others_file_list = [], [], []

    for directory in directories:
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".txt"):
                file_list_list[directories.index(directory)].append(filename)


get_files()


# Create your views here.
def home(request):
    get_files()
    open_file = request.GET.get("file")
    context = {}
    notes = []

    if open_file is not None:
        for category in CATEGORIES:
            try:
                with open(f"{ROOT_DIR}/{category}/{open_file}", "r") as file_opened:
                    notes = file_opened.readlines()
                    context.update({"notes": notes,"file_category": f"{category.capitalize()}"
                            if category != "PROGRAMMING LIFE" else "Programming Life",})
                    break
            except FileNotFoundError:
                if CATEGORIES.index(category) == 2:
                    return redirect("home")
    context.update({"open_file": open_file, "academia_file_list": academia_file_list, 
                    "programming_life_file_list": programming_life_file_list, 
                    "others_file_list": others_file_list,})
    return render(request, "home.html", context)


def save(request):
    if request.method == "POST":
        post_data = request.POST
        notes = post_data.get("notes")
        category = post_data.get("category")

        filename = post_data.get("hidden-filename")
        original_filename = post_data.get("original_filename")

        if original_filename != "" and original_filename != filename:
            # Just use a good old for-loop with an if-checker bro!!
            # But how do I link file_lists with categories?? Wait, can I use the name of a variable to 
            # do some stuff? I've been wondering about this fora  long time and other stuff like this.
            # Right now, I'm a Hungarian. STC, FEED US!!!

            # No need, I'll just use the indices
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
            with open(
                f"/home/farouq/Documents/Notes/{category.upper()}/{filename}", "w"
            ) as file:
                for note in notes:
                    file.write(note.rstrip("\n"))
    return redirect(f"/?file={filename}")
