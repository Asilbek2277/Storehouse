from django.shortcuts import render, redirect
from django.views import View

from mainApp.models import *


class BolimlarVeiw(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "bo'limlar.html")
        return  redirect('login')


class MahsulotlarView(View):

    def get(self, request):
        if request.user.is_authenticated:
            mahsulotlar=Mahsulot.objects.filter(tarqatuvchi=request.user)
            context={
                'mahsulotlar': mahsulotlar
            }
            return render(request, 'mahsulotlar.html', context)
        return redirect('login')


    def post(self, request):
        if request.user.is_authenticated:
            Mahsulot.objects.create(
                tarqatuvchi=request.user,
                nom=request.POST['nom'],
                brend=request.POST['brend'],
                narx1=request.POST['narx1'],
                narx2=request.POST['narx2'],
                miqdor=request.POST['miqdor'],
                olchov=request.POST['olchov'],
                sana=request.POST['sana']
            )
            return redirect('mahsulotlar')

        return redirect('login')





class MijozView(View):
    def get(self, request):
        if request.user.is_authenticated:
            mijozlar = Mijoz.objects.filter(tarqatuvchi=request.user)
            context={
                'mijozlar': mijozlar
            }
            return render(request, 'mijozlar.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            Mijoz.objects.create(
                ism=request.POST['ism'],
                dokon=request.POST['dokon'],
                tel=request.POST['tel'],
                manzil=request.POST['manzil'],
                tarqatuvchi=request.user
            )
            return redirect('mijozlar')
        return redirect('login')







class MahsulotTahrirlashView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            context={
                'product': Mahsulot.objects.get(id=id)
            }
            return render(request, 'mahsulot-tahrirlash.html', context)
        return redirect('login')


    def post(self, request, id):
        if request.user.is_authenticated:
            if request.method == 'POST':
                mahsulot=Mahsulot.objects.get(id=id)
                if mahsulot.tarqatuvchi==request.user:
                    mahsulot.nom=request.POST['nom']
                    mahsulot.brend=request.POST['brend']
                    mahsulot.narx1=request.POST['narx1']
                    mahsulot.narx2=request.POST['narx2']
                    mahsulot.miqdor=request.POST['miqdor']
                    mahsulot.olchov=request.POST['olchov']
                    mahsulot.sana=request.POST['sana']
                    mahsulot.save()

                    return redirect('mahsulotlar')
        return redirect('login')

def mahsulot_ochirish(request, pk):
    if request.user.is_authenticated:
        if Mahsulot.objects.get(id=pk).tarqatuvchi==request.user:
            Mahsulot.objects.get(id=pk).delete()
            return redirect('mahsulotlar')
    return redirect('login')



class MijozlarniTahrirlashView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            context={
                'client': Mijoz.objects.get(id=pk)
            }
            return render(request, 'mijoz-tahrirlash.html', context)
        return redirect('login')

    def post(self, request, pk):
        if request.user.is_authenticated:
            if request.method=='POST':
                mijoz=Mijoz.objects.get(id=pk)
                if mijoz.tarqatuvchi==request.user:
                    mijoz.ism=request.POST['ism']
                    mijoz.dokon=request.POST['dokon']
                    mijoz.tel=request.POST['tel']
                    mijoz.manzil=request.POST['manzil']
                    mijoz.save()

                    return redirect('mijozlar')

        return redirect('login')


def mijoz_ochirish(request, pk):
    if request.user.is_authenticated:
        if Mijoz.objects.get(id=pk).tarqatuvchi==request.user:
            Mijoz.objects.get(id=pk).delete()
            return redirect('mijozlar')

    return redirect('login')



