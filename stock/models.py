from django.db import models

# Create your models here.
class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    localisation = models.CharField(max_length=256)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name
    
class Product(models.Model):

    class Etat(models.TextChoices):
        DISPONIBLE = "disponible", "Disponible"
        RESERVE = "reserve", "Réservé"
        PERIME = "perime", "Périmé"

    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    expiration_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Etat.choices,
        default=Etat.DISPONIBLE,
    )

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name