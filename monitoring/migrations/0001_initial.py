from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('roles', models.IntegerField(choices=[(1, 'Guru'), (2, 'Ortu'), (3, 'Admin')], default=2)),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='abstract_user', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='MataPelajaran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Murid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('jenis_kelamin', models.CharField(choices=[('Laki-Laki', 'Laki-Laki'), ('Perempuan', 'Perempuan')], max_length=20)),
                ('tanggal_lahir', models.DateField()),
                ('kelas', models.CharField(max_length=50)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='murid/')),
                ('status', models.BooleanField(default=True)),
                ('ortu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='monitoring.abstractuser')),
            ],
        ),
        migrations.CreateModel(
            name='Nilai',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nilai', models.IntegerField()),
                ('updated_year', models.IntegerField()),
                ('guru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inputted_grades', to='monitoring.abstractuser')),
                ('mapel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='monitoring.matapelajaran')),
                ('murid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nilai_set', to='monitoring.murid')),
            ],
        ),
    ]
