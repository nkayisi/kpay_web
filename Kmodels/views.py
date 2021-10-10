from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

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
