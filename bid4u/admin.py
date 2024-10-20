from django.contrib import admin
from bid4u.models import Account_allegro


class Account_allegroAdmin(admin.ModelAdmin):
    list_filter = ('client_id', 'client_secret')
    #date_hierarchy = 'release_date'
    #list_display = ('original_title', 'release_date', 'statistics__vote_count')


admin.site.register(Account_allegro)
# Register your models here.
