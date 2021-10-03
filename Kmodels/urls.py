from django.urls import path, include

from rest_framework.routers import DefaultRouter


from .views import *



router = DefaultRouter()
router.register('client', ClientApiView, basename='client')
router.register('transaction', TransactionApiView, basename='transaction')
router.register('agent-supply', AgentSupplyApiView, basename='agent-supply')
router.register('bill', BillApiView, basename='bill')
router.register('phone-otp', PhoneOTPApiView, basename='phone-otp')



urlpatterns = [
    path('', include(router.urls)),
]
