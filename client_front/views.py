from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import permissions

from django.contrib.auth.models import AnonymousUser

from Kmodels import models as main_models
from Kmodels import clientModel

from Kmodels.forms import LoginForm

from Kmodels.userSerializers import *


from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages





def index(request):
    return render(request, 'client/pages/index.html')



def loginView(request):

    if not request.user or isinstance(request.user, AnonymousUser):

        if request.method == 'POST':

            phone = request.POST.get('phone')
            password = request.POST.get('password')

            user = authenticate(phone=phone, password=password)

            if user is not None and user.is_active:
                login(request, user)
                if user.admin:
                    return redirect('supply')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Numéro ou mot de passe incorrect ! Veillez entrer un compte valide.')

    else:
        if request.user.admin:
            return redirect('supply')
        else:
            return redirect('home')

    return render(request, 'client/pages/login.html')


@login_required
def logOut(request):
    logout(request)
    return redirect('index')


@login_required
def home(request):
    return render(request, 'client/pages/home.html')


@login_required
def account(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        phone = request.POST.get('phone')
        status = request.POST.get("status")
        password = request.POST.get('password')

        user = clientModel.Client.objects.create_user(
            phone = phone,
            name = username,
            password = password
        )


        user.active = True

        if status == str(1):
            user.client = True
        elif status == str(2):
            user.agent = True
        elif status == str(3):
            user.shop_assistant = True
        else:
            user.admin = True

        user.save()


    return render(request, 'client/pages/account.html')



def wallet(request):
    return render(request, "client/pages/wallet.html")



def nAccount(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        passsword = request.POST.get('password')

        if Client.objects.filter(phone=phone).exists():
            messages.error(request, 'Cet numéro de téléphone est déjà identifierpo dans la plateforme ou pocede déjà un compte. Veillez en choisir un autre !')
        else:
            user = clientModel.Client.objects.create_user(
                name = username,
                phone = phone,
                password = passsword
            )

            user.active = True
            user.client = True

            user.save()

            return redirect('login')

    return render(request, 'client/pages/normal-account.html')



@login_required
def supply(request):

    if request.method == 'POST':

        phone = request.POST.get('phone')
        amount = float(request.POST.get('amount'))

        if clientModel.Client.objects.filter(phone=phone).exists():

            recever = clientModel.Client.objects.get(phone=phone)

            if request.user.admin:

                if recever.agent:

                    benefit = amount*0.1

                    main_models.AgentSupply.objects.create(
                        trans_amount = amount,
                        benefit = benefit,
                        desc_type = "Recharge",
                        sender = request.user,
                        recever = recever
                    )

                    recever.usd_balance += (amount+benefit)
                    recever.save()

                else:
                    messages.warning(request, "Désolé, vous ne pouvez que recharger un compte  Agent!")

            elif request.user.agent and not recever.admin and not recever.shop_assistant:

                if request.user.usd_balance >= amount:

                    main_models.Transaction.objects.create(
                        trans_amount = amount,
                        desc_type = "Recharge",
                        sender = request.user,
                        recever = recever
                    )

                    request.user.usd_balance -= amount
                    request.user.save()

                    recever.usd_balance += amount
                    recever.save()

                else:
                    messages.warning(request, "Votre solde est issufisant pour éffectué cette opération!")
            else:
                messages.warning(request, "Verifier le type de compte avant la recharge!")


            messages.success(request, "Rechargement faite avec succès pour l'identifiant "+ phone)


        else:
            messages.warning(request, "Compte introuvable pour l'identifiant "+ phone)

    return render(request, 'client/pages/supply.html')


@login_required
def transfer(request):
    return render(request, 'client/pages/transfer.html')


@login_required
def withdraw(request):

    if request.method == 'POST':

        phone = request.POST.get('phone')
        amount = float(request.POST.get('amount'))

        if clientModel.Client.objects.filter(phone=phone).exists():

            recever = clientModel.Client.objects.get(phone=phone)
            
            if recever.agent:
                
                trans_cost = amount*0.06

                if request.user.usd_balance >= (amount+trans_cost):

                    main_models.Transaction.objects.create(
                        trans_amount = amount,
                        trans_cost = trans_cost,
                        desc_type = "Retrait",
                        sender = request.user,
                        recever = recever
                    )

                    request.user.usd_balance -= (amount+trans_cost)
                    request.user.save()

                    recever.usd_balance += amount
                    recever.save()  

                    messages.success(request, "Votre retrait de " + str(amount) + " USD chez l'Agent " + phone + " a réussit") 

                else:
                    messages.warning(request, "Désolé votre solde est issufisant pour pour éffectué cette opération!")
            
            else:
                messages.warning(request, "Veillez entrer un numéro valide d'un Agent!")

        else:
            messages.warning(request, "Compte introuvable pour l'identifiant "+ phone)

    return render(request, 'client/pages/withdraw.html')


@login_required
def send(request):

    if request.method == 'POST':

        phone = request.POST.get('phone')
        amount = float(request.POST.get('amount'))

        if clientModel.Client.objects.filter(phone=phone).exists():

            trans_cost = amount*0.05

            recever = clientModel.Client.objects.get(phone=phone)
            
            main_models.Transaction.objects.create(
                trans_amount = amount,
                trans_cost = trans_cost,
                sender = request.user,
                recever = recever
            )

            request.user.usd_balance -= (amount+trans_cost)
            request.user.save()

            recever.usd_balance += amount
            recever.save()  

            messages.success(request, "Votre transfert de " + str(amount) + " USD vers l'identifiant " + phone + " a réussit") 

        else:
            messages.warning(request, "Compte introuvable pour l'identifiant "+ phone)          

    return render(request, 'client/pages/send.html')


@login_required
def bill(request):

    bills = main_models.Bill.objects.filter(recipient=request.user, is_payed=False)


    context = {
        'bills': bills
    }

    return render(request, 'client/pages/bill.html', context)



@login_required
def billSubmit(request):

    if request.method == 'POST':

        phone = request.POST.get('phone')
        amount = float(request.POST.get('amount'))
        motif = request.POST.get('motif')

        if clientModel.Client.objects.filter(phone=phone).exists():

            recever = clientModel.Client.objects.get(phone=phone)

            main_models.Bill.objects.create(
                bill_amount = amount,
                bill_motif = motif,
                shop_assistant = request.user,
                recipient = recever
            )
            
            messages.success(request, "Votre facture de " + str(amount) + " USD a été soumit à " + phone) 
        else:
            messages.warning(request, "Compte introuvable pour l'identifiant "+ phone) 

    return render(request, 'client/pages/bill-submit.html')



@login_required
def billDetail(request, id):

    bills = main_models.Bill.objects.filter(recipient=request.user, is_payed=False)

    bill = main_models.Bill.objects.get(id=id)

    context = {
        'bill': bill,
        'bills': bills
    }

    return render(request, 'client/pages/bill-detail.html', context)



@login_required
def activity(request):
    return render(request, 'client/pages/activity.html')