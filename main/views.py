from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import TipeKamar, Pemesanan, Kamar
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import logout
from .forms import RegistrationForm
from django.contrib.auth import login
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


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

    return render(request, 'main/tipe-kamar.html', {'tipe_kamars': tipe_kamars})


from django.shortcuts import render, redirect
from django.views import View
from .models import TipeKamar, Pemesanan

class PemesananView(View):
    def get(self, request):
        tipe_kamars = TipeKamar.objects.all()
        return render(request, 'main/form_pemesanan.html', {'tipe_kamars': tipe_kamars})

    def post(self, request):
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')
        tipe_kamar_id = request.POST.get('tipe_kamar')
        tipe_sewa = request.POST.get('tipe_sewa')
        durasi = request.POST.get('durasi')
        jumlah_penghuni = request.POST.get('jumlah_penghuni')
        tanggal_mulai = request.POST.get('tanggal_mulai')

        try:
            tipe_kamar = TipeKamar.objects.get(id=tipe_kamar_id)
            durasi = int(durasi)
            jumlah_penghuni = int(jumlah_penghuni)

            if jumlah_penghuni > tipe_kamar.max_penghuni:
                return render(request, 'main/form_pemesanan.html', {
                    'error': 'Jumlah penghuni melebihi kapasitas kamar!',
                    'tipe_kamars': TipeKamar.objects.all()
                })

            # Buat pemesanan tanpa kamar terlebih dahulu
            Pemesanan.objects.create(
                nama=nama,
                kontak=kontak,
                tipe_kamar=tipe_kamar,
                tipe_sewa=tipe_sewa,
                durasi=durasi,
                jumlah_penghuni=jumlah_penghuni,
                tanggal_mulai=tanggal_mulai,
                user=request.user
            )

            return redirect('success_page')

        except TipeKamar.DoesNotExist:
            return render(request, 'main/form_pemesanan.html', {
                'error': 'Tipe kamar tidak ditemukan',
                'tipe_kamars': TipeKamar.objects.all()
            })


# AJAX view to get max penghuni dynamically
def get_jumlah_penghuni(request, tipe_kamar_id):
    tipe_kamar = get_object_or_404(TipeKamar, id=tipe_kamar_id)
    return JsonResponse({"jumlah_penghuni": list(range(1, tipe_kamar.max_penghuni + 1))})



class SuccessView(View):
    def get(self, request):
        return render(request, 'main/success.html', {})


def lokasi(request):
    return render(request, 'main/lokasi.html')


def faq(request):
    return render(request, 'main/faq.html')


def hubungi_kami(request):
    if request.method == "POST":
        nama = request.POST.get("nama")
        email = request.POST.get("email")
        pesan = request.POST.get("pesan")

        subject = f"Pesan Baru dari {nama}"
        body = f"Nama: {nama}\nEmail: {email}\n\nPesan:\n{pesan}"

        try:
            send_mail(subject, body, email, ["residencebarat@gmail.com"])
            messages.success(request, "Pesan Anda berhasil dikirim! Kami akan segera menghubungi Anda.")
        except Exception as e:
            messages.error(request, f"Error saat mengirim email: {e}")

        return redirect("hubungi_kami")  # Redirect back to contact page

    return render(request, "main/hubungi_kami.html")


def custom_logout(request):
    logout(request)
    return redirect("index")  # Redirect ke halaman utama setelah logout


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Akun berhasil dibuat! Anda sekarang masuk.")
            return redirect("index")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")  # Menampilkan setiap error sebagai pesan

    else:
        form = RegistrationForm()

    return render(request, "main/registrasi.html", {"form": form})





