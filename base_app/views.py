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


directory = os.fsencode("C:/Users/Farouq/Documents/Notes/")
    
directories = [os.fsencode("C:/Users/Farouq/Documents/Notes/ACADEMIA"), 
                os.fsencode("C:/Users/Farouq/Documents/Notes/PROGRAMMING LIFE"), 
                os.fsencode("C:/Users/Farouq/STs"),
                ]
file_list = []
academia_file_list = []
programming_life_file_list = []
sts_file_list = []

file_list_list = [academia_file_list, programming_life_file_list, sts_file_list]

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"): # or filename.endswith(".py")
        file_list.append(filename)
        
for directory in directories:
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            file_list_list[directories.index(directory)].append(filename)
            
            
# Create your views here.
def home(request):
    open_file = request.GET.get('file')
    context = {}

    if open_file is not None:
        try:
            with open(f'C:/Users/Farouq/Documents/Notes/ACADEMIA/{open_file}', 'r') as file_opened:
                notes = file_opened.readlines()
                context.update({"notes":notes, 'file_category': "Academia"})
        except FileNotFoundError:
            try:
                with open(f'C:/Users/Farouq/STs/{open_file}', 'r') as file_opened:
                    notes = file_opened.readlines()
                    context.update({"notes":notes, 'file_category': "Shower Thoughts"})
            except:
                with open(f'C:/Users/Farouq/Documents/Notes/PROGRAMMING LIFE/{open_file}', 'r') as file_opened:
                    notes = file_opened.readlines()
                    context.update({'notes':notes ,'file_category': 'Programming Life'})
            
    context.update({'open_file':open_file, 
                    'file_list':file_list, 
                    'academia_file_list':academia_file_list,
                    'programming_life_file_list':programming_life_file_list, 
                    'sts_file_list':sts_file_list})
    return render(request, 'home.html', context)
        

def save(request):
    if request.method == 'POST':
        notes = request.POST.get('notes')
        category = request.POST.get('category')

        filename = request.POST.get('hidden-filename')
        print(filename)
        original_filename = request.POST.get('original_filename')
        
        if original_filename != '' and original_filename != filename :
            if original_filename in academia_file_list:
                os.rename(f'C:/Users/Farouq/Documents/Notes/ACADEMIA/{original_filename}', f'C:/Users/Farouq/Documents/Notes/ACADEMIA/{filename}')
            elif original_filename in programming_life_file_list:
                os.rename(f'C:/Users/Farouq/Documents/Notes/PROGRAMMING LIFE/{original_filename}', f'C:/Users/Farouq/Documents/Notes/PROGRAMMING LIFE/{filename}')
            elif original_filename in sts_file_list:
                os.rename(f'C:/Users/Farouq/STs/{original_filename}', f'C:/Users/Farouq/STs/{filename}')
            
            
        if category == "Academia":
            with open(f'C:/Users/Farouq/Documents/Notes/ACADEMIA/{filename}', 'w') as file:
                for note in notes:
                    file.write(note.rstrip('\n'))
        elif category == "Programming Life":
            with open(f'C:/Users/Farouq/Documents/Notes/PROGRAMMING LIFE/{filename}', 'w') as file:
                for note in notes:
                    file.write(note.rstrip('\n'))
        elif category == "Shower Thoughts":
            with open(f'C:/Users/Farouq/STs/{filename}', 'w') as file:
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