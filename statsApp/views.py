import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import *


class StatsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            sotuvlar = Stats.objects.filter(tarqatuvchi=request.user)
            mahsulotlar = Mahsulot.objects.filter(tarqatuvchi=request.user)
            mijozlar = Mijoz.objects.filter(tarqatuvchi=request.user)
            foyda = 0
            for sotuv in sotuvlar:
                foyda += (sotuv.mahsulot.narx2 - sotuv.mahsulot.narx1) * sotuv.miqdor
            if request.GET.get('search'):
                sotuvlar = Stats.objects.filter(
                    Q(mahsulot__nom__contains=request.GET['search']) |
                    Q(mijoz__ism__contains=request.GET['search']) |
                    Q(mijoz__dokon__contains=request.GET['search']) |
                    Q(mahsulot__brend__contains=request.GET['search']) |
                    Q(summa__contains=request.GET['search'])
                )
            context = {
                'sotuvlar': sotuvlar,
                'tarqatuvchi': request.user,
                'mahsulotlar': mahsulotlar,
                'mijozlar': mijozlar,
                'summa': sum(Stats.objects.filter(tarqatuvchi=request.user).values_list('summa', flat=True)),
                'qarz': sum(Stats.objects.filter(tarqatuvchi=request.user).values_list('qarz', flat=True)),
                'foyda': foyda
            }
            return render(request, 'statistikalar.html', context)

        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            mijoz = Mijoz.objects.get(id=request.POST['mijoz'])

            if request.POST['summa']:
                summa=request.POST['summa']
            else:
                summa=float(request.POST['miqdor'])*Mahsulot.objects.get(id=request.POST['mahsulot']).narx2
            if request.POST['tolandi']:
                tolash=request.POST['tolandi']

            else:
                tolash=0
            if summa < tolash:
                return HttpResponse(
                    """
                    <h2>Kechirasiz Summa ustunidagi qiymat tolandi ustunidagi qiymatdan kichik bolishi mumkun emas!!!</h2>
                    <a href='/stats/stats/'>Ortga</a>
                    """
                )



            Stats.objects.create(
                mahsulot=Mahsulot.objects.get(id=request.POST['mahsulot']),
                mijoz=mijoz,
                sana=request.POST['sana'],
                miqdor=request.POST['miqdor'],
                summa=summa,
                tolandi=tolash,
                qarz=summa - tolash,
                tarqatuvchi=request.user
            )
            mahsulotlar = Mahsulot.objects.get(id=request.POST['mahsulot'])
            mahsulotlar.miqdor -= int(request.POST['miqdor'])
            mahsulotlar.save()

            if sum(Stats.objects.filter(tarqatuvchi=request.user,
                                        mijoz__id=mijoz.id).values_list('qarz', flat=True)) is None:
                mijoz.qarz = 0
                mijoz.save()

            mijoz.qarz = sum(
                Stats.objects.filter(tarqatuvchi=request.user, mijoz__id=mijoz.id).values_list('qarz', flat=True))
            mijoz.save()
            return redirect('stats')
        return redirect('login')


class Stats_TahrirlashView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            sotuvlar = Stats.objects.get(id=pk)
            context = {
                'sotuvlar': sotuvlar,
                'mahsulot': Mahsulot.objects.filter(tarqatuvchi=request.user),
                'mijoz': Mijoz.objects.filter(tarqatuvchi=request.user)
            }

            return render(request, 'statistika_tahrirlash.html', context)
        return redirect('login')

    def post(self, request, pk):
        if request.user.is_authenticated:
            sotuvlar = Stats.objects.get(id=pk)
            miqdor1 = sotuvlar.miqdor
            if sotuvlar.tarqatuvchi == request.user:
                sotuvlar.mahsulot = Mahsulot.objects.get(id=request.POST['mahsulot'])
                sotuvlar.mijoz = Mijoz.objects.get(id=request.POST['mijoz'])
                sotuvlar.sana = datetime.datetime.now()
                sotuvlar.miqdor = request.POST['miqdor']
                sotuvlar.summa = request.POST['summa']
                sotuvlar.tolandi = request.POST['tolandi']
                sotuvlar.qarz = request.POST['qarz']
                sotuvlar.save()

                mahsulot = Mahsulot.objects.get(id=sotuvlar.mahsulot.id)
                farq = float(request.POST['miqdor']) - miqdor1

                mahsulot.miqdor -= farq
                mahsulot.save()

                return redirect('stats')

        return redirect('login')


class SotuvDelete(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            if Stats.objects.get(id=pk).tarqatuvchi == request.user:
                sotuv = Stats.objects.get(id=pk)
                mijoz = Mijoz.objects.get(id=sotuv.mijoz.id)
                Stats.objects.get(id=pk).delete()

                mijoz.qarz = sum(
                    Stats.objects.filter(tarqatuvchi=request.user, mijoz__id=mijoz.id).values_list('qarz', flat=True)
                )
                mijoz.save()
                return redirect('stats')
        return redirect('login')
