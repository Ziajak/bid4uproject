from django.urls import path
from . import views

urlpatterns = [


    path('', views.start, name='start_url'),
    path('start', views.start, name='start_url'),
    path('settings', views.settings, name='settings_url'),
    path('auctions', views.auctions, name='auction_url'),
    path('check/<int:id>', views.check, name='check_url'),
    path('auctions/delete/<int:id>', views.delete_auction, name='delete_auctions'),
    path('code/<int:id>', views.code),
    path('settings/delete<int:id>', views.delete_account ,name='delete_account_allegro')

]

