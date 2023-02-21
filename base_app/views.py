from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import os

# Create your views here.
def home(request):
    open_file = request.GET.get('file') # if request.GET.get('file') is not None else ''

    directory = os.fsencode("C:/Users/Farouq/Desktop/")
    file_list = []
    context = {}
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt") or filename.endswith(".py"): 
            file_list.append(filename)

    if open_file is not None:
        with open(f'C:/Users/Farouq/Desktop/{open_file}', 'r') as file_opened:
            notes = file_opened.readlines()

            context['notes'] = notes
            print(notes)
            
    context['file_list'] = file_list
    context.update({'open_file':open_file})
    return render(request, 'home.html', context)
        

def save(request):
    if request.method == 'POST':
        print(request.POST.get('notes').count('\n'))
        notes = request.POST.get('notes')
        filename = request.POST.get('hidden-filename')
        print(filename)
        print(request.POST.get('open'))

        with open(f'C:/Users/Farouq/Desktop/{filename}', 'w') as file:
            for note in notes:
                file.write(note.rstrip('\n'))
                # file.write('a')
            # print(n)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))