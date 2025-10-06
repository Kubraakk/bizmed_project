from django.core.management.base import BaseCommand
from core.models import Department, Doctor
from faker import Faker
import random

DEPT_DEFAULTS = [
    'Kardiyoloji','Dahiliye','Ortopedi','Nöroloji','Göz','Kulak Burun Boğaz',
    'Üroloji','Genel Cerrahi','Cildiye','Psikiyatri','Fizik Tedavi','Endokrinoloji'
]

class Command(BaseCommand):
    help = "Demo verisi: Department + Doctor doldurur."

    def add_arguments(self, parser):
        parser.add_argument('--departments', type=int, default=0,
                            help='Rastgele departman sayısı (0 ise ön tanımlılar kullanılır)')
        parser.add_argument('--min-doctors', type=int, default=3)
        parser.add_argument('--max-doctors', type=int, default=6)

    def handle(self, *args, **opts):
        fake = Faker('tr_TR')
        min_d = max(1, opts['min_doctors'])
        max_d = max(min_d, opts['max_doctors'])

        # Departmanlar
        if opts['departments'] > 0:
            names = [fake.job() for _ in range(opts['departments'])]
        else:
            names = DEPT_DEFAULTS

        deps = []
        for name in names:
            dep, _ = Department.objects.get_or_create(name=name)
            deps.append(dep)
        self.stdout.write(self.style.SUCCESS(f'Department: {len(deps)} hazır.'))

        # Doktorlar
        total_docs = 0
        for dep in deps:
            for _ in range(random.randint(min_d, max_d)):
                first = fake.first_name()
                last  = fake.last_name()
                Doctor.objects.get_or_create(
                    first_name=first,
                    last_name=last,
                    department=dep
                )
                total_docs += 1

        self.stdout.write(self.style.SUCCESS(f'Doctor toplam: ~{total_docs} eklendi.'))
