from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('siswa/', views.siswa_view, name='siswa'),
    path('buat-anak/', views.buat_anak, name='buat_anak'),
    path('nilai-akademik/', views.nilai_akademik_view, name='nilai_akademik'),
    path('buat-nilai/', views.buat_nilai, name='buat_nilai'),
]
