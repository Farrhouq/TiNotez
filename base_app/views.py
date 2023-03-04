from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import os

directory = os.fsencode("C:/Users/Farouq/Documents/Notes/")
file_list = []
context = {}
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"): # or filename.endswith(".py") 
        file_list.append(filename)


# Create your views here.
def home(request):
    open_file = request.GET.get('file')

    directory = os.fsencode("C:/Users/Farouq/Documents/Notes/")
    file_list = []
    context = {}
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"): # or filename.endswith(".py") 
            file_list.append(filename)

    if open_file is not None:
        with open(f'C:/Users/Farouq/Documents/Notes/{open_file}', 'r') as file_opened:
            notes = file_opened.readlines()
            context['notes'] = notes
            
    context['file_list'] = file_list
    context.update({'open_file':open_file})
    return render(request, 'home.html', context)
        

def save(request):
    if request.method == 'POST':
        notes = request.POST.get('notes')

        filename = request.POST.get('hidden-filename')
        original_filename = request.POST.get('original_filename')

        if original_filename != filename:
            os.rename(f'C:/Users/Farouq/Documents/Notes/{original_filename}', f'C:/Users/Farouq/Documents/Notes/{filename}')
            
            
        with open(f'C:/Users/Farouq/Documents/Notes/{filename}', 'w') as file:
            for note in notes:
                file.write(note.rstrip('\n'))
    return redirect(f'/?file={filename}')
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# def open(request, file_name):
#     context = {}
#     with open(f'C:/Users/Farouq/Documents/Notes/{file_name}', 'r') as file_opened:
#             notes = file_opened.readlines()
#             context['notes'] = notes
#             context['file_list'] = file_list

#     return render(request, 'home.html', context)