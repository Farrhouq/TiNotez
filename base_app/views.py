from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, 'home.html')
    

def save(request):
    if request.method == 'POST':
        print(request.POST.get('notes').count('\n'))
        notes = request.POST.get('notes')
        filename = request.POST.get('hidden-filename')
        print(filename)

        with open(f'C:/Users/Farouq/Desktop/{filename}', 'w') as file:
            file.write(notes)
    return redirect('home')