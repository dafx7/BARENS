from django.shortcuts import render
from .models import TipeKamar


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def tipe_kamar(request):
    tipe_kamars = TipeKamar.objects.all()
    return render(request, 'main/tipe-kamar.html', {'tipe_kamars': tipe_kamars})


