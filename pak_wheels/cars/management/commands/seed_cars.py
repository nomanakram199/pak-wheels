from django.core.management.base import BaseCommand
from pak_wheels.cars.models import CarBrand, CarModel


CAR_DATA = {
    'Toyota': ['Corolla', 'Yaris', 'Vitz', 'Prius', 'Aqua', 'Land Cruiser',
               'Fortuner', 'Hilux', 'Camry', 'Premio', 'Passo'],
    'Honda': ['Civic', 'City', 'BR-V', 'HR-V', 'Vezel', 'Accord', 'N-Wgn',
              'Freed', 'Fit'],
    'Suzuki': ['Mehran', 'Cultus', 'Wagon R', 'Alto', 'Swift', 'Bolan',
               'Ravi', 'Ciaz', 'Vitara', 'APV', 'Every'],
    'Hyundai': ['Tucson', 'Elantra', 'Sonata', 'Santa Fe', 'Porter', 'H-100'],
    'Kia': ['Sportage', 'Picanto', 'Stonic', 'Sorento', 'Carnival'],
    'MG': ['HS', 'ZS EV', 'ZS', '5'],
    'Changan': ['Alsvin', 'Karvaan', 'M9', 'Oshan X7', 'CS35 Plus'],
    'Proton': ['Saga', 'X70', 'X50'],
    'Nissan': ['Dayz', 'Moco', 'Clipper', 'Sunny', 'X-Trail'],
    'Daihatsu': ['Mira', 'Move', 'Cuore', 'Hijet', 'Tanto', 'Copen'],
    'BMW': ['3 Series', '5 Series', '7 Series', 'X1', 'X3', 'X5'],
    'Mercedes-Benz': ['C-Class', 'E-Class', 'S-Class', 'GLA', 'GLC', 'GLE'],
    'Audi': ['A3', 'A4', 'A6', 'Q3', 'Q5', 'Q7'],
}


class Command(BaseCommand):
    help = 'Seeds the database with car brands and models for Pakistan market'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding car brands and models...')

        for brand_name, models in CAR_DATA.items():
            brand, created = CarBrand.objects.get_or_create(name=brand_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created brand: {brand_name}'))

            for model_name in models:
                model, created = CarModel.objects.get_or_create(
                    brand=brand,
                    name=model_name
                )
                if created:
                    self.stdout.write(f'  + {model_name}')

        self.stdout.write(self.style.SUCCESS('\nDone! Database seeded.'))
        self.stdout.write(f'Total brands: {CarBrand.objects.count()}')
        self.stdout.write(f'Total models: {CarModel.objects.count()}')
