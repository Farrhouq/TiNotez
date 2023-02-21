from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, 'home.html')
    

def save(request):
    if request.method == 'POST':
        print(request.POST.get('notes'))
        
    with open() as file:
        pass
    return redirect('home')