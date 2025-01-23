from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def tipe_kamar(request):
    return render(request, 'main/tipe-kamar.html')

