from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import AbstractUser, Murid, MataPelajaran, Nilai
from datetime import datetime

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                abstract_user = AbstractUser.objects.get(user=user)
                if abstract_user.status:
                    auth_login(request, user)
                    request.session['user_id'] = abstract_user.id
                    request.session['name'] = abstract_user.name.upper()
                    if int(abstract_user.roles) == 1:
                        request.session['roles'] = "GURU"
                    elif int(abstract_user.roles) == 2:
                        request.session['roles'] = "ORTU"
                    else:
                        request.session['roles'] = "ADMIN"
                    messages.success(request, 'Login Berhasil')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Akun Anda belum disetujui oleh admin, silakan tunggu persetujuan.')
            except AbstractUser.DoesNotExist:
                messages.error(request, 'Pengguna tidak ditemukan dalam sistem.')
                return redirect('login')
        else:
            messages.error(request, 'Username atau password salah')
            return redirect('login')
            
    return render(request, 'monitoring/login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        name = request.POST.get('name')
        role = request.POST.get('role')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Password dan konfirmasi password tidak cocok.')
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah terdaftar.')
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar.')
            return redirect('signup')
            
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=name
        )
        
        abstract = AbstractUser()
        abstract.user = user
        abstract.name = name
        abstract.roles = int(role)
        if int(role) == 2: # Ortu auto approved
            abstract.status = True
        abstract.save()
        
        if abstract.status:
            user = authenticate(request, username=username, password=password)
            auth_login(request, user)
            request.session['user_id'] = abstract.id
            request.session['name'] = abstract.name.upper()
            request.session['roles'] = "ORTU"
            messages.success(request, 'Akun berhasil dibuat.')
            return redirect('dashboard')
        else:
            messages.success(request, 'Pendaftaran berhasil. Tunggu persetujuan admin.')
            return redirect('login')
            
    return render(request, 'monitoring/signup.html')

def logout_view(request):
    auth_logout(request)
    request.session.flush()
    return redirect('login')

@login_required
def dashboard_view(request):
    # Default redirection based on roles
    return redirect('siswa')

@login_required
def siswa_view(request):
    role = request.session.get('roles')
    user_id = request.session.get('user_id')
    
    # If the user is ORTU, show only their children, otherwise show all
    if role == 'ORTU':
        murids = Murid.objects.filter(ortu_id=user_id)
    else:
        murids = Murid.objects.all()
        
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        murids = murids.filter(name__icontains=search_query)
        
    return render(request, 'monitoring/siswa.html', {
        'murids': murids,
        'search_query': search_query,
    })

@login_required
def buat_anak(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        jenis_kelamin = request.POST.get('jenis_kelamin')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        kelas = request.POST.get('kelas')
        foto = request.FILES.get('foto')
        ortu_id = request.session.get('user_id')
        
        try:
            ortu = AbstractUser.objects.get(id=ortu_id)
            Murid.objects.create(
                name=name,
                jenis_kelamin=jenis_kelamin,
                tanggal_lahir=tanggal_lahir,
                kelas=kelas,
                foto=foto,
                status=True,
                ortu=ortu
            )
            messages.success(request, 'Murid berhasil ditambahkan.')
            return redirect('siswa')
        except Exception as e:
            messages.error(request, f'Gagal menambahkan murid: {str(e)}')
            return redirect('siswa')
            
    return redirect('siswa')

@login_required
def nilai_akademik_view(request):
    role = request.session.get('roles')
    user_id = request.session.get('user_id')
    
    if role == 'ORTU':
        # Show grades for their children only
        grades = Nilai.objects.filter(murid__ortu_id=user_id)
    else:
        grades = Nilai.objects.all()
        
    search_query = request.GET.get('search', '')
    if search_query:
        grades = grades.filter(murid__name__icontains=search_query)
        
    # Data for the tambah nilai form
    murids = Murid.objects.all()
    mapels = MataPelajaran.objects.all()
    
    return render(request, 'monitoring/nilai_akademik.html', {
        'grades': grades,
        'search_query': search_query,
        'murids': murids,
        'mapels': mapels,
    })

@login_required
def buat_nilai(request):
    if request.method == 'POST':
        murid_id = request.POST.get('murid_id')
        mapel_id = request.POST.get('mapel_id')
        nilai = request.POST.get('nilai')
        
        nil = Nilai.objects.filter(murid_id=murid_id, mapel_id=mapel_id, updated_year=datetime.now().year)
        if nil.exists():
            messages.error(request, 'Data Nilai Sudah ada di mapel yang sama.')
            return redirect('nilai_akademik')
            
        try:
            murid = Murid.objects.get(pk=murid_id)
            mapel = MataPelajaran.objects.get(pk=mapel_id)
            Nilai.objects.create(
                guru_id=request.session.get('user_id'),
                murid=murid,
                mapel=mapel,
                nilai=int(nilai),
                updated_year=datetime.now().year
            )
            messages.success(request, 'Data nilai berhasil ditambahkan.')
            return redirect('nilai_akademik')
        except Exception as e:
            messages.error(request, f'Gagal menambahkan nilai: {str(e)}')
            return redirect('nilai_akademik')
            
    return redirect('nilai_akademik')
