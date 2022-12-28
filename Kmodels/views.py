from django.shortcuts import get_object_or_404, render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from knox.auth import TokenAuthentication



from .serializers import *
from .clientModel import *
from .models import *
 


class ClientApiView(ModelViewSet):

    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        return Client.objects.all()



class TransactionApiView(ModelViewSet):

    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        return Transaction.objects.all()

    def create(self, request, *args, **kwargs):

        trans_cost = 0
        transData = request.data

        sender = get_object_or_404(Client, phone=transData['sender'])
        recever = get_object_or_404(Client, phone=transData['recever'])
        amount = float(transData['amount'])
        currency = transData['currency']
        trans_type = transData['type']

        if trans_type == 'Retrait':
            trans_cost = amount*0.08
        else:
            trans_cost = amount*0.05

        newTrans = Transaction.objects.create(
            trans_amount = amount,
            trans_cost = trans_cost,
            desc_type = trans_type,
            currency = currency,
            sender = sender,
            recever = recever
        )
        newTrans.save()

        if currency == 'USD':
            sender.usd_balance -= (amount+trans_cost)
            sender.save()

            recever.usd_balance += amount
            recever.save()
        else:
            sender.cdf_balance -= (amount+trans_cost)
            sender.save()

            recever.cdf_balance += amount
            recever.save()

        serializer = TransactionSerializer(newTrans)
        return Response(serializer.data)
    


class AgentSupplyApiView(ModelViewSet):

    serializer_class = AgentSupplySerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        return AgentSupply.objects.all()



class BillApiView(ModelViewSet):

    serializer_class = BillSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        return Bill.objects.all()




class PhoneOTPApiView(ModelViewSet):

    serializer_class = PhoneOTPSerializer

    def get_queryset(self):
        return PhoneOTP.objects.all()
