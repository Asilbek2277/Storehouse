import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .models import *

class StatsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            sotuvlar=Stats.objects.filter(tarqatuvchi=request.user)
            mahsulotlar=Mahsulot.objects.filter(tarqatuvchi=request.user)
            mijozlar=Mijoz.objects.filter(tarqatuvchi=request.user)
            foyda=0
            for sotuv in sotuvlar:
                foyda+=(sotuv.mahsulot.narx2-sotuv.mahsulot.narx1)*sotuv.miqdor
            if request.GET.get('search'):
                sotuvlar=Stats.objects.filter(
                    Q(mahsulot__nom__contains=request.GET['search'])|
                    Q(mijoz__ism__contains=request.GET['search'])|
                    Q(mijoz__dokon__contains=request.GET['search'])|
                    Q(mahsulot__brend__contains=request.GET['search'])|
                    Q(summa__contains=request.GET['search'])
                )
            context={
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
            mijoz=Mijoz.objects.get(id=request.POST['mijoz'])
            if request.POST['summa']<request.POST['tolandi']:
                return redirect('stats')
            # m=Stats.objects.get(mahsulot__id=request.POST['mahsulot'])
            # if int(request.POST['miqdor'])>m.mahsulot.miqdor :
            #     return redirect('stats')
            Stats.objects.create(
                mahsulot=Mahsulot.objects.get(id=request.POST['mahsulot']),
                mijoz=mijoz,
                sana=request.POST['sana'],
                miqdor=request.POST['miqdor'],
                summa=request.POST['summa'],
                tolandi=request.POST['tolandi'],
                qarz=int(request.POST['summa'])-int(request.POST['tolandi']),
                tarqatuvchi=request.user
            )

            if  sum(Stats.objects.filter(tarqatuvchi=request.user,
                                         mijoz__id=mijoz.id).values_list('qarz', flat=True))==0:
                mijoz.qarz=0
                mijoz.save()



            mijoz.qarz=sum(Stats.objects.filter(tarqatuvchi=request.user, mijoz__id=mijoz.id).values_list('qarz', flat=True))
            mijoz.save()

            # if stats.tolandi+stats.qarz==stats.summa:
            #     return redirect('stats')
            # return HttpResponse('Kechirasiz ')
            return redirect('stats')
        return redirect('login')


class Stats_TahrirlashView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            sotuvlar=Stats.objects.get(id=pk)
            context={
                'sotuvlar': sotuvlar,
                'mahsulot': Mahsulot.objects.filter(tarqatuvchi=request.user),
                'mijoz': Mijoz.objects.filter(tarqatuvchi=request.user)
            }

            return render(request, 'statistika_tahrirlash.html', context)
        return redirect('login')

    def post(self, request, pk):
        if request.user.is_authenticated:
            sotuvlar = Stats.objects.get(id=pk)
            if sotuvlar.tarqatuvchi==request.user:
                sotuvlar.mahsulot=Mahsulot.objects.get(id=request.POST['mahsulot'])
                sotuvlar.mijoz=Mijoz.objects.get(id=request.POST['mijoz'])
                sotuvlar.sana=datetime.datetime.now()
                sotuvlar.miqdor=request.POST['miqdor']
                sotuvlar.summa=request.POST['summa']
                sotuvlar.tolandi=request.POST['tolandi']
                sotuvlar.qarz = request.POST['qarz']
                sotuvlar.save()

                return redirect('stats')

        return redirect('login')





class SotuvDelete(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            if Stats.objects.get(id=pk).tarqatuvchi==request.user:
                sotuv=Stats.objects.get(id=pk)
                mijoz=Mijoz.objects.get(id=sotuv.mijoz.id)
                mijoz.qarz = sum(
                    Stats.objects.filter(tarqatuvchi=request.user,
                                         mijoz__id=mijoz.id).values_list('qarz', flat=True))
                mijoz.save()
                Stats.objects.get(id=pk).delete()
                return redirect('stats')
        return redirect('login')





