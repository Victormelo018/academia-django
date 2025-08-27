from django.shortcuts import render

# Create your views here.


def base (request):
    return render(request, 'website/base.html')



def contato (request):
    return render(request, 'website/contato.html')

    
def sobre (request):
    return render(request, 'website/sobre.html')


def home (request):
    return render(request, 'website/home.html')

