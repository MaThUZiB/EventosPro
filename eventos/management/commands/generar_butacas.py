from django.core.management.base import BaseCommand
from eventos.models import Sala, Butaca

class Command(BaseCommand):
    help = "Genera butacas para una sala"

    def add_arguments(self, parser):
        parser.add_argument('sala_id', type=int, help="ID de la sala")
        parser.add_argument('--filas', type=int, default=8, help="Número de filas")
        parser.add_argument('--columnas', type=int, default=12, help="Número de asientos por fila")

    def handle(self, *args, **kwargs):
        sala_id = kwargs['sala_id']
        filas = kwargs['filas']
        columnas = kwargs['columnas']

        try:
            sala = Sala.objects.get(id=sala_id)
        except Sala.DoesNotExist:
            self.stdout.write(self.style.ERROR("La sala no existe"))
            return

        Butaca.objects.filter(sala=sala).delete()
        filas_letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for i in range(filas):
            for num in range(1, columnas + 1):
                Butaca.objects.create(
                    sala=sala,
                    fila=filas_letras[i],
                    numero=num,
                    disponible=True
                )

        self.stdout.write(self.style.SUCCESS(f"✅ {filas*columnas} butacas creadas para la sala {sala.id}"))
