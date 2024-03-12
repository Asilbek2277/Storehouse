from django.core.validators import MinValueValidator
from django.db import models

from userApp.models import Tarqatuvchi


class Mahsulot(models.Model):
    nom = models.CharField(max_length=255)
    brend = models.CharField(max_length=255, blank=True, null=True)
    narx1 = models.FloatField(validators=[MinValueValidator(0)])
    narx2 = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    miqdor = models.PositiveIntegerField(default=1)
    olchov = models.CharField(max_length=50)
    tarqatuvchi = models.ForeignKey(Tarqatuvchi, on_delete=models.CASCADE)
    sana = models.DateField()

    def __str__(self):
        return f"{self.tarqatuvchi.username}: {self.nom}"


class Mijoz(models.Model):
    ism = models.CharField(max_length=255)
    dokon = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=14)
    manzil = models.TextField()
    tarqatuvchi = models.ForeignKey(Tarqatuvchi, on_delete=models.CASCADE)
    qarz = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.tarqatuvchi.username}: {self.ism}"
