import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kindegarten.settings')
django.setup()

from monitoring.models import MataPelajaran

subjects = [
    "Bahasa Inggris",
    "Bahasa Mandarin",
    "Fisika Dasar",
    "Matematika Dasar",
    "Kimia Dasar",
    "Coding"
]

print("Seeding subjects...")
for name in subjects:
    obj, created = MataPelajaran.objects.get_or_create(nama=name)
    if created:
        print(f"Created subject: {name}")
    else:
        print(f"Subject already exists: {name}")

print("Seeding finished successfully!")
