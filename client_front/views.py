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

from datetime import date
from decimal import *


# for PDF
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import context, pisa


def render_pdf_view(request, id):

    transaction = get_object_or_404(main_models.Transaction, id=id)

    template_path = 'client/layouts/invoice.html'
    context = {'transaction': transaction}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reçu-{transaction.trans_date}.pdf"'
    # if display
    # response['Content-Disposition'] = f'filename="reçu-{transaction.trans_date}.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


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
                    return redirect('dashboard')
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

    usd = Decimal(request.user.usd_balance)
    cdf = Decimal(request.user.cdf_balance)

    context = {
        'usd': usd.quantize(Decimal('.01'), rounding=ROUND_HALF_UP),
        'cdf': cdf.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    }

    return render(request, "client/pages/wallet.html", context)



def nAccount(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        phone = request.POST.get('phone')
        passsword = request.POST.get('password')

        if Client.objects.filter(phone=phone).exists():
            messages.warning(request, 'Cet numéro de téléphone est déjà identifierpo dans la plateforme ou pocede déjà un compte. Veillez en choisir un autre !')
        else:

            # return render(request, 'client/pages/verifier.html', {'user':{
            #     'name': username,
            #     'phone': phone,
            #     'password': passsword,
            #     'active': True,
            #     'client': True
            # }})

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


def verifier(request):

    code = request.POST.get('code')
    user = request.POST.get('user')

    print(code, user)

    return render(request, 'client/pages/verifier.html')


@login_required
def supply(request):

    if request.method == 'POST':

        balance = False

        phone = request.POST.get('phone')
        amount = float(request.POST.get('amount'))
        currency = request.POST.get('currency')

        if clientModel.Client.objects.filter(phone=phone).exists():

            recever = clientModel.Client.objects.get(phone=phone)

            if request.user.admin:

                if recever.agent:

                    benefit = amount*0.1

                    main_models.AgentSupply.objects.create(
                        trans_amount = amount,
                        desc_type = "Recharge",
                        benefit = benefit,
                        currency = currency,
                        sender = request.user,
                        recever = recever
                    )

                    if currency == 'USD':

                        request.user.usd_balance += (amount+benefit)
                        request.user.save()

                        recever.usd_balance += (amount+benefit)
                        recever.save()
                    else:

                        request.user.cdf_balance += (amount+benefit)
                        request.user.save()

                        recever.cdf_balance += (amount+benefit)
                        recever.save()

                else:
                    messages.warning(request, "Désolé, vous ne pouvez que recharger un compte  Agent!")

            elif request.user.agent and not recever.admin and not recever.shop_assistant:

                if currency == 'USD':
                    if request.user.usd_balance >= amount:
                        balance = True
                else:
                    if request.user.cdf_balance >= amount:
                        balance = True


                if balance:

                    main_models.Transaction.objects.create(
                        trans_amount = amount,
                        desc_type = "Recharge",
                        currency = currency,
                        sender = request.user,
                        recever = recever
                    )

                    if currency == 'USD':

                        request.user.usd_balance -= amount
                        request.user.save()

                        recever.usd_balance += amount
                        recever.save()
                    else:
                        request.user.cdf_balance -= amount
                        request.user.save()

                        recever.cdf_balance += amount
                        recever.save()
                    
                    messages.success(request, "Votre recharge de " + str(amount) + currency + " vers l'identifiant " + phone + " a réussit") 

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

        balance = False

        phone = request.POST.get('phone')
        amount = float(request.POST.get('amount'))
        currency= request.POST.get('currency')

        if clientModel.Client.objects.filter(phone=phone).exists():

            recever = clientModel.Client.objects.get(phone=phone)
            
            if recever.agent:

                trans_cost = amount*0.06

                if currency == 'USD':
                    if request.user.usd_balance >= (amount+trans_cost):
                        balance = True
                else:
                    if request.user.cdf_balance >= (amount+trans_cost):
                        balance = True
                

                if balance:

                    main_models.Transaction.objects.create(
                        trans_amount = amount,
                        trans_cost = trans_cost,
                        currency = currency,
                        desc_type = "Retrait",
                        sender = request.user,
                        recever = recever
                    )


                    if currency == 'USD':
                        request.user.usd_balance -= (amount+trans_cost)
                        request.user.save()

                        recever.usd_balance += amount
                        recever.save()  
                    else:
                        request.user.cdf_balance -= (amount+trans_cost)
                        request.user.save()

                        recever.cdf_balance += amount
                        recever.save() 

                    messages.success(request, "Votre retrait de " + str(amount) + currency + " chez l'Agent " + phone + " a réussit") 

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

        balance = False

        phone = request.POST.get('phone')
        amount = float(request.POST.get('amount'))
        currency = request.POST.get('currency')

        if clientModel.Client.objects.filter(phone=phone).exists():

            if currency == 'USD':
                if request.user.usd_balance >= amount:
                    balance = True
            else:
                if request.user.cdf_balance >= amount:
                    balance = True

            if balance:

                trans_cost = amount*0.05

                recever = clientModel.Client.objects.get(phone=phone)
                
                main_models.Transaction.objects.create(
                    trans_amount = amount,
                    trans_cost = trans_cost,
                    currency = currency,
                    sender = request.user,
                    recever = recever
                )

                if currency == 'USD':

                    request.user.usd_balance -= (amount+trans_cost)
                    request.user.save()

                    recever.usd_balance += amount
                    recever.save()  
                else:
                    request.user.cdf_balance -= (amount+trans_cost)
                    request.user.save()

                    recever.cdf_balance += amount
                    recever.save() 

                messages.success(request, "Votre transfert de " + str(amount) + currency + " vers l'identifiant " + phone + " a réussit") 

            else:
                messages.warning(request, "Votre solde est insufisant pour éffectué cette opération!") 

        else:
            messages.warning(request, "Compte introuvable pour l'identifiant "+ phone)          

    return render(request, 'client/pages/send.html')


@login_required
def bill(request):

    bills = main_models.Bill.objects.filter(recipient=request.user)


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
        currency = request.POST.get('currency')

        if clientModel.Client.objects.filter(phone=phone).exists():

            recever = clientModel.Client.objects.get(phone=phone)

            main_models.Bill.objects.create(
                bill_amount = amount,
                bill_motif = motif,
                currency = currency,
                shop_assistant = request.user,
                recipient = recever
            )
            
            messages.success(request, "Votre facture de " + str(amount) + " USD a été soumit à " + phone) 
        else:
            messages.warning(request, "Compte introuvable pour l'identifiant "+ phone) 

    return render(request, 'client/pages/bill-submit.html')



@login_required
def billDetail(request, id):

    bills = main_models.Bill.objects.filter(recipient=request.user)

    bill = get_object_or_404(main_models.Bill, id=id)

    context = {
        'bill': bill,
        'bills': bills
    }

    return render(request, 'client/pages/bill-detail.html', context)


@login_required
def billPay(request, id):

    balance = False
    today = date.today()

    bills = main_models.Bill.objects.filter(recipient=request.user)

    bill = get_object_or_404(main_models.Bill, id=id)

    if bill.currency == 'USD':
        if request.user.usd_balance >= bill.bill_amount:
            balance = True
    else:
        if request.user.cdf_balance >= bill.bill_amount:
            balance = True

    if balance:

        amount = float(bill.bill_amount)

        trans = main_models.Transaction.objects.create(
            trans_amount = amount,
            desc_type = "Paiement facture",
            currency = bill.currency,
            sender = request.user,
            recever = bill.shop_assistant
        )

        if bill.currency == 'USD':

            request.user.usd_balance -= amount
            request.user.save()

            bill.shop_assistant.usd_balance += amount
            bill.shop_assistant.save()
        else:
            request.user.cdf_balance -= amount
            request.user.save()

            bill.shop_assistant.cdf_balance += amount
            bill.shop_assistant.save()


        bill.is_payed = True
        bill.transation = trans
        bill.bill_payed_date = today
        bill.save()

        # messages.success(request, "Votre paiement de facture pour le montant de " + str(amount) + bill.currency + " vers l'identifiant " + bill.shop_assistant + " a réussit") 
    # else:
        # messages.warning(request, "Votre paiement de facture pour le montant de " + str(bill.bill_amount) + bill.currency + " vers l'identifiant " + bill.shop_assistant + " a échoué, cause d'insuffisance de solde !")

    context = {
        'bill': bill,
        'bills': bills
    }

    return render(request, 'client/pages/bill-detail.html', context)


@login_required
def activity(request):

    transactions = main_models.Transaction.objects.filter(sender=request.user)

    context={
        'transactions': transactions
    }

    return render(request, 'client/pages/activity.html', context)



@login_required
def dashboard(request):

    transactions = main_models.Transaction.objects.all()

    users = clientModel.Client.objects.all()

    admins = users.filter(admin=True)
    agents = users.filter(agent=True)
    shop_assistants = users.filter(shop_assistant=True)
    clients = users.filter(client=True)

    context = {
        'admins': admins,
        'agents': agents,
        'assistants': shop_assistants,
        'clients': clients,
        'transactions': transactions
    }

    return render(request, 'client/pages/dashboard.html', context)