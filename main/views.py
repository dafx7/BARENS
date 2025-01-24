from django.shortcuts import render
from .models import TipeKamar


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


from django.db.models import Q

def tipe_kamar(request):
    # Ambil semua tipe kamar
    tipe_kamars = TipeKamar.objects.all()

    # Ambil filter dari request GET
    harga_filter = request.GET.get('harga')
    orang_filter = request.GET.get('orang')
    token_filter = request.GET.get('token')

    # Filter berdasarkan range harga (mempertimbangkan token dan non-token)
    if harga_filter:
        if harga_filter == '1':
            tipe_kamars = tipe_kamars.filter(
                Q(harga_per_bulan_1_orang__lte=1000000) | Q(harga_non_token_1_orang__lte=1000000)
            )
        elif harga_filter == '2':
            tipe_kamars = tipe_kamars.filter(
                Q(harga_per_bulan_1_orang__gt=1000000, harga_per_bulan_1_orang__lte=2000000) |
                Q(harga_non_token_1_orang__gt=1000000, harga_non_token_1_orang__lte=2000000)
            )
        elif harga_filter == '3':
            tipe_kamars = tipe_kamars.filter(
                Q(harga_per_bulan_1_orang__gt=2000000) | Q(harga_non_token_1_orang__gt=2000000)
            )

    # Filter berdasarkan jumlah penghuni (maksimal >= jumlah yang dipilih user)
    if orang_filter:
        tipe_kamars = tipe_kamars.filter(max_penghuni__gte=orang_filter)

    # Filter berdasarkan token/non-token
    if token_filter:
        if token_filter == 'token':
            # Ambil kamar yang memiliki harga token, terlepas dari apakah ada harga non-token
            tipe_kamars = tipe_kamars.filter(harga_per_bulan_1_orang__isnull=False)
        elif token_filter == 'non-token':
            # Ambil kamar yang memiliki harga non-token
            tipe_kamars = tipe_kamars.filter(harga_non_token_1_orang__isnull=False)

    # Tambahkan ini sebelum return render
    print("DEBUG: Filter Harga:", harga_filter)
    print("DEBUG: Filter Orang:", orang_filter)
    print("DEBUG: Filter Token:", token_filter)
    print("DEBUG: Queryset:", tipe_kamars.query)

    return render(request, 'main/tipe-kamar.html', {'tipe_kamars': tipe_kamars})

