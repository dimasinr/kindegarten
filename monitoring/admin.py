from django.contrib import admin
from .models import AbstractUser, Murid, MataPelajaran, Nilai

@admin.register(AbstractUser)
class AbstractUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'roles', 'status')
    list_filter = ('roles', 'status')
    search_fields = ('name', 'user__username')
    list_editable = ('status',)

@admin.register(Murid)
class MuridAdmin(admin.ModelAdmin):
    list_display = ('name', 'jenis_kelamin', 'kelas', 'ortu', 'status')
    list_filter = ('jenis_kelamin', 'kelas', 'status')
    search_fields = ('name', 'ortu__name')

@admin.register(MataPelajaran)
class MataPelajaranAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ('nama',)

@admin.register(Nilai)
class NilaiAdmin(admin.ModelAdmin):
    list_display = ('murid', 'mapel', 'nilai', 'guru', 'updated_year')
    list_filter = ('mapel', 'updated_year')
    search_fields = ('murid__name', 'guru__name')
