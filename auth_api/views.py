from django.shortcuts import render
from django.contrib.auth import login

# rest impots
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, status

from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView


# my imports
from Kmodels.clientModel import Client as User
from Kmodels.clientModel import PhoneOTP


from Kmodels.userSerializers import CreateUserSerializer, LoginUserSerializer


import random






class ValidatePhoneSendOTP(APIView):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''

    def post(self, request, *args, **kwargs):

        phone_number = request.data.get('phone')

        if phone_number:

            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already exists'})
                 # logic to send the otp and store the phone number and that otp in table. 
            else:

                if PhoneOTP.objects.filter(phone__iexact=phone).exists():
                    PhoneOTP.objects.get(phone=phone).delete()

                otp = send_otp(phone)
                print(phone, otp)

                if otp:

                    otp = str(otp)
               
                    PhoneOTP.objects.create(
                            phone =  phone, 
                            otp =   otp
                    )
                         
                else:
                    return Response({
                                'status': 'False', 'detail' : "OTP sending error. Please try after some time."
                            })

                return Response({
                    'status': True, 'detail': 'Otp has been sent successfully.'
                })
        else:
            return Response({
                'status': 'False', 
                'detail' : "Phone number is not given inPOST request."
            })



class ValidateOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password
    
    '''

    def post(self, request, *args, **kwargs):

        phone = request.data.get('phone', False)
        otp_sent   = request.data.get('otp', False)

        if phone and otp_sent:

            old = PhoneOTP.objects.filter(phone__iexact = phone)

            if old.exists():

                old = old.first()
                otp = old.otp

                if str(otp) == str(otp_sent):

                    old.validated = True
                    old.save()

                    return Response({
                        'status' : True, 
                        'detail' : 'OTP matched, kindly proceed to save password'
                    })

                else:
                    return Response({
                        'status' : False, 
                        'detail' : 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status' : False,
                    'detail' : 'Phone not recognized. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or otp was not received in Post request'
            })



class Register(APIView):

    '''Takes phone and a password and creates a new user only if otp was verified and phone is new'''

    def post(self, request, *args, **kwargs):

        name = request.data.get('name', False)
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)

        if phone and password and name:

            phone = str(phone)
            user = User.objects.filter(phone__iexact = phone)

            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already have account associated. Kindly try forgot password'})
            else:

                old = PhoneOTP.objects.filter(phone__iexact = phone)

                if old.exists():

                    old = old.first()

                    if old.validated:

                        Temp_data = {'name': name, 'phone': phone, 'password': password }

                        serializer = CreateUserSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.client = True
                        user.save()

                        old.delete()

                        return Response({
                            'status' : True, 
                            'detail' : 'Congrats, user has been created successfully.'
                        })

                    else:
                        return Response({
                            'status': False,
                            'detail': 'Your otp was not verified earlier. Please go back and verify otp'

                        })
                else:
                    return Response({
                    'status' : False,
                    'detail' : 'Phone number not recognized. Kindly request a new otp with this number'
                })

        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or password was not recieved in Post request'
            })




class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # if user.last_login is None :
        #     user.first_login = True
        #     user.save()
            
        # elif user.first_login:
        #     user.first_login = False
        #     user.save()
            
        login(request, user)
        return super().post(request, format=None)




def send_otp(phone):
    
    if phone:
        key = random.randint(999, 9999)
        print(key)
        return key
    else:
        return False
