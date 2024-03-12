from django.db import models

from mainApp.models import *
from userApp.models import Tarqatuvchi


class Stats(models.Model):
    mahsulot=models.ForeignKey(Mahsulot, on_delete=models.SET_NULL, null=True)
    mijoz=models.ForeignKey(Mijoz, on_delete=models.SET_NULL, null=True)
    sana=models.DateField()
    miqdor=models.FloatField(validators=[MinValueValidator(0)])
    summa=models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)])
    tolandi=models.FloatField(default=0, validators=[MinValueValidator(0)])
    qarz=models.FloatField(default=0, validators=[MinValueValidator(0)])
    tarqatuvchi=models.ForeignKey(Tarqatuvchi, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mahsulot.nom}-{self.mijoz.ism}"
