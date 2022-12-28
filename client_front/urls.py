from django.urls import path



from .views import *



urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('login/', loginView, name='login'),
    path('logout/', logOut, name='logout'),
    path('supply/', supply, name='supply'),
    path('wallet/', wallet, name='wallet'),

    path('account/', account, name='account'),
    path('client-account/', nAccount, name='clientAccount'),
    path('verifier-phone/', verifier, name='verifier-phone'),

    path('transfer/', transfer, name='transfer'),
    path('withdraw/', withdraw, name='withdraw'),
    path('send/', send, name='send'),
    path('bill/', bill, name='bill'),
    path('bill-submit/', billSubmit, name='bill-submit'),
    path('bill-detail/<int:id>/', billDetail, name='bill-detail'),
    path('bill-pay/<int:id>/', billPay, name='bill-pay'),
    path('activity/', activity, name='activity'),
    path('dashboard/', dashboard, name='dashboard'),

    path('pdf/<int:id>/', render_pdf_view, name='pdf'),
]
