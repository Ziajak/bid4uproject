from django.shortcuts import render, redirect
from .models import Account_allegro, List_bid_allegro
from django.http import HttpResponseForbidden
from django.db.models import Avg, Min, Max, Count
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .forms import AuctionsForm, AccountForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from datetime import date
from .server import put_bid, get_access_code, sign_in, get_access_code_check
from apscheduler.schedulers.background import BackgroundScheduler
import sched
import time
import re


# Create your views here.

@login_required()
def settings(request):
    logged_user = request.user
    account_settings = Account_allegro.objects.filter(owner_id=logged_user.id)
    if account_settings.count() > 0:
        print('Masz już konto allegro i możesz mieć przypisane tylko jedno')
        context = {
            'settings': account_settings,
        }
        return render(request, 'bid4u/settings.html', context)

    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account_data = form.cleaned_data
            # print(auction_data['date_bid'])
            Account_allegro.objects.create(
                client_id=account_data['CLIENT_ID'],
                client_secret=account_data['CLIENT_SECRET'],
                owner_id=logged_user.id
            )
        else:
            print(form.errors)
            account_form = form
            context = { 'account_form': account_form
            }
            return render(request, 'bid4u/settings.html', context)

         #Account_allegro.objects.create(client_id=client_id, client_secret=client_secret, owner_id=logged_user.id)

    account_settings = Account_allegro.objects.filter(owner_id=logged_user.id)
    account_form = AccountForm()
    context = {
        'settings': account_settings,
        'account_form': account_form
    }
    return render(request, 'bid4u/settings.html', context)

scheduler = BackgroundScheduler()
@login_required()
def auctions(request):
    logged_user = request.user
    account_allegro = Account_allegro.objects.filter(owner_id=logged_user.id).first()

    #client_id = account_allegro.values_list('client_id', flat=True).first()
    client_id = Account_allegro.objects.filter(owner_id=logged_user.id).values_list('client_id').first()
    # count_first_access_code = Linked_account.objects.filter(owner_id=logged_user.id,
    #                                                         first_access_code__isnull=False).count()
    print(client_id)
    if client_id != None: #and count_first_access_code > 0:
        if request.method == 'POST':
            form = AuctionsForm(request.POST)
            valid_form = form.is_valid()
            if valid_form:
                auction_data = form.cleaned_data
                #print(auction_data['date_bid'])
                saved_auction = List_bid_allegro.objects.create(
                    link = auction_data['link'],
                    bid_date = auction_data['date_bid'],
                    amount= auction_data['amount'],
                    account_id = account_allegro
                )
                client_id = account_allegro.client_id
                client_secret = account_allegro.client_secret

                bid_date = saved_auction.bid_date
                id_bid = saved_auction.id

                bid_date = bid_date.strftime('%Y-%m-%d %H:%M:%S%z')
                bid_date = re.split(r'[-: ]', bid_date[:-5])
                year = int(bid_date[0])
                month = int(bid_date[1])
                day = int(bid_date[2])
                hour = int(bid_date[3])
                minute = int(bid_date[4])
                seconds = int(bid_date[5])
                # Tworzenie harmonogramu
                run_date = datetime(year, month, day, hour, minute, seconds)

                get_access_code_check(client_id=client_id, api_key=client_secret, id=id_bid)
                # Dodanie zadania do harmonogramu

                scheduler.add_job(get_access_code, 'date', run_date=run_date, args=[client_id, client_secret, id_bid])
                # Uruchomienie harmonogramu

                if not scheduler.running:

                    scheduler.start()
                else:
                    print("Scheduler już działa.")

            elif not valid_form:
                auctions_form = form
                list_auctions = List_bid_allegro.objects.filter(account_id=logged_user.id).all()
                context = {
                    'auctions_form': auctions_form,
                    'list_auctions': list_auctions
                }
                return render(request, 'bid4u/auctions.html', context)


    else:
        return redirect('settings_url')


    auctions_form = AuctionsForm()
    list_auctions = List_bid_allegro.objects.filter(account_id=account_allegro.id).all()
    context = {
        'auctions_form': auctions_form,
        'list_auctions': list_auctions
    }
    return render(request, 'bid4u/auctions.html', context)


def code(request, id):
    auction_allegro = List_bid_allegro.objects.get(pk=id)

    client_id = auction_allegro.account_id.client_id
    client_secret = auction_allegro.account_id.client_secret

    link = auction_allegro.link
    amount = auction_allegro.amount

    access_code = request.GET.get('code')
    print(access_code)
    token = sign_in(client_id=client_id, client_secret=client_secret, id=id, access_code=access_code)


    put_bid(token=token, link=link, amount=amount)
    auction_allegro.status = 'Wykonane'
    auction_allegro.save()
    return render(request, 'bid4u/code.html')



def delete_auction(request, id):
    List_bid_allegro.objects.get(pk=id).delete()
    jobs = scheduler.get_jobs()

    for job in jobs:
        print(f"Args: {job.args}")
        if job.args[-1] == id:
             job.remove()


    return redirect('auction_url')

def delete_account(request, id):
    Account_allegro.objects.get(pk=id).delete()

    return redirect('settings_url')

def start(request):

    return render(request, 'bid4u/start.html')


def check(request, id):
    print(id)
    access_code = request.GET.get('code')
    if access_code:
        print(access_code)
        return render(request, 'bid4u/check.html')










