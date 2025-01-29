from django.shortcuts import render, redirect
from django.views import View
from .models import TipeKamar, Pemesanan
from django.core.mail import send_mail
from django.contrib import messages



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


class PemesananView(View):
    def get(self, request):
        # Ambil parameter tipe_kamar dari query string
        tipe_kamar_id = request.GET.get('tipe_kamar')
        tipe_kamar = TipeKamar.objects.filter(id=tipe_kamar_id).first()  # Validasi jika tipe kamar tidak ditemukan

        return render(request, 'main/form_pemesanan.html', {
            'tipe_kamar': tipe_kamar,  # Kirim tipe kamar ke template
            'tipe_kamars': TipeKamar.objects.all()  # Jika ada dropdown untuk pilihan
        })

    def post(self, request):
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')
        tipe_kamar_id = request.POST.get('tipe_kamar')
        durasi = request.POST.get('durasi')
        jumlah_penghuni = request.POST.get('jumlah_penghuni')
        tanggal_mulai = request.POST.get('tanggal_mulai')

        # Validasi dan simpan data
        try:
            tipe_kamar = TipeKamar.objects.get(id=tipe_kamar_id)
            Pemesanan.objects.create(
                nama=nama,
                kontak=kontak,
                tipe_kamar=tipe_kamar,
                durasi=durasi,
                jumlah_penghuni=int(jumlah_penghuni),
                tanggal_mulai=tanggal_mulai
            )
            return redirect('success_page')  # Redirect ke halaman sukses (buat route jika belum ada)
        except TipeKamar.DoesNotExist:
            return render(request, 'main/form_pemesanan.html', {
                'error': 'Tipe kamar tidak ditemukan',
                'tipe_kamars': TipeKamar.objects.all()
            })



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
