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
    path('transfer/', transfer, name='transfer'),
    path('withdraw/', withdraw, name='withdraw'),
    path('send/', send, name='send'),
    path('bill/', bill, name='bill'),
    path('bill-submit/', billSubmit, name='bill-submit'),
    path('bill-detail/<int:id>', billDetail, name='bill-detail'),
    path('activity/', activity, name='activity'),
]
