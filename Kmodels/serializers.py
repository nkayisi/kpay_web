from rest_framework import serializers



from .models import *
from .clientModel import *



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        depth = 1


class AgentSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentSupply
        fields = '__all__'
        depth = 2



class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'
        depth = 2




class PhoneOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneOTP
        fields = '__all__'
