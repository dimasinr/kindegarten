from django.db import models
from django.contrib.auth.models import User

class AbstractUser(models.Model):
    ROLE_CHOICES = (
        (1, 'Guru'),
        (2, 'Ortu'),
        (3, 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='abstract_user')
    name = models.CharField(max_length=255)
    roles = models.IntegerField(choices=ROLE_CHOICES, default=2)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.get_roles_display()})"

class Murid(models.Model):
    GENDER_CHOICES = (
        ('Laki-Laki', 'Laki-Laki'),
        ('Perempuan', 'Perempuan'),
    )
    name = models.CharField(max_length=255)
    jenis_kelamin = models.CharField(max_length=20, choices=GENDER_CHOICES)
    tanggal_lahir = models.DateField()
    kelas = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='murid/', blank=True, null=True)
    status = models.BooleanField(default=True)
    ortu = models.ForeignKey(AbstractUser, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.name

    @property
    def rata_rata_nilai(self):
        grades = self.nilai_set.all()
        if not grades.exists():
            return 0
        total = sum(g.nilai for g in grades)
        return round(total / grades.count(), 2)

class MataPelajaran(models.Model):
    nama = models.CharField(max_length=255)

    def __str__(self):
        return self.nama

class Nilai(models.Model):
    guru = models.ForeignKey(AbstractUser, on_delete=models.CASCADE, related_name='inputted_grades')
    murid = models.ForeignKey(Murid, on_delete=models.CASCADE, related_name='nilai_set')
    mapel = models.ForeignKey(MataPelajaran, on_delete=models.CASCADE, related_name='grades')
    nilai = models.IntegerField()
    updated_year = models.IntegerField()

    def __str__(self):
        return f"{self.murid.name} - {self.mapel.nama}: {self.nilai}"
