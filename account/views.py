from django.shortcuts import render, redirect
from account.models import Account, KYC
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
from core.models import CreditCard
import datetime

# Create your views here.

@login_required
def account(request):
    
    try:
        kyc = KYC.objects.get(user=request.user)
    except:
        messages.warning(request, 'You need to submit your kyc')
        return redirect('account:kyc-reg')

    
    account = Account.objects.get(user=request.user)
        

    context= {
        'kyc': kyc,
        'account': account,
    }

    return render(request, 'account/account.html', context)

"""
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None

    if request.method = "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
        new_form = form.save(commit=False)
        new_form.user = user
        new_form.account = account
        new_form.save()

        messages.success(request, "KYC Form submitted successfully, In review now.")
        
        return redirect('core:index')

    else:    
        form = KYCForm(instance=kyc)


    context = {
        'account': account,
        'form': form,
        'kyc': kyc,
    }

    return render(request , 'account/kyc-form.html', context)
"""
#@login_required
def kyc_registration(request): 
    user = request.user
    account = Account.objects.get(user=user) 

    # if KYC.objects.get(user=user).exist():
    #     kyc = KYC.objects.get(user=user)

    #     if request.method == "POST":
    #         form = KYCForm(request.POST, request.FILES, instance=kyc)
    #         if form.is_valid():
    #             form.save(commit=False)
    #             form.user = user
    #             form.account = account
    #             form.save()

    #             messages.success(request, "You KYC details have been updated.")
    #             return redirect("account:account")
                
        
    #     else:
    #         form = KYCForm(instance=kyc)

    # else:
    #     if request.method == "POST":
    #         form = KYCForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             form.save(commit=False)
    #             form.user = user
    #             form.account = account
    #             form.save()

    #             messages.success(request, "KYC form submitted successfully. In review now.")

    #             created_day = kyc.date.day
    #             created_month = kyc.date.month
    #             created_year = kyc.date.year
    #             created_hour = kyc.date.hour

    #             verification_day = datetime.datetime.now().day
    #             verification_month = datetime.datetime.now().month
    #             verification_year = datetime.datetime.now().year
    #             verification_hour = datetime.datetime.now().hour
    
    #             if (verification_day == created_day + 1 and verification_month == created_month and verification_year == created_year and verification_hour > created_hour) \
    #             or (verification_day > created_day + 1 and verification_month == created_month and verification_year == created_year) \
    #             or (verification_month == created_month and verification_year == created_year) \
    #             or (verification_year == created_year):
                
    #                 account.account_status = "active"
    #                 account.save()

    #             return redirect("account:account")
        
    #     else:
    #         form = KYCForm()


    try:
        kyc = KYC.objects.get(user=user)
    except: 
        kyc = None


    # created_day = kyc.date.day
    # created_month = kyc.date.month
    # created_year = kyc.date.year
    # created_hour = kyc.date.hour

    # verification_day = datetime.datetime.now().day
    # verification_month = datetime.datetime.now().month
    # verification_year = datetime.datetime.now().year
    # verification_hour = datetime.datetime.now().hour


    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()

            messages.success(request, "KYC form submitted successfully. In review now.")
 
            # if (verification_day == created_day + 1 and verification_month == created_month and verification_year == created_year and verification_hour > created_hour) \
            # or (verification_day > created_day + 1 and verification_month == created_month and verification_year == created_year) \
            # or (verification_month > created_month and verification_year == created_year) \
            # or (verification_year > created_year):
            
            # print(kyc.date)
            account.account_status = "active"
            account.save()
            return redirect("account:account")
    
    else:
        if kyc == None:
            form = KYCForm(instance=kyc)

        else:
            form = KYCForm(instance=kyc)
        
            # if (verification_day == created_day + 1 and verification_month == created_month and verification_year == created_year and verification_hour > created_hour) \
            # or (verification_day > created_day + 1 and verification_month == created_month and verification_year == created_year) \
            # or (verification_month > created_month and verification_year == created_year) \
            # or (verification_year > created_year):
        
            #     print(kyc.date)
            #     account.account_status = "active"
            #     account.save()
                


    context = {
        'account': account,
        'kyc': kyc,
        'form': form,
    }

    return render(request , 'account/kyc-form.html', context)

def dashboard(request):
    if request.user.is_authenticated:
        account = Account.objects.get(user=request.user)

        if account.account_status == "active":

            try:
                kyc = KYC.objects.get(user=request.user)
            except:
                messages.warning(request, 'You need to submit your kyc')
                return redirect('account:kyc-reg')
            
            # account = Account.objects.get(user=request.user)

            credit_card = CreditCard.objects.filter(user=request.user).order_by("-date")

            if request.method == "POST":
                form = CreditCardForm(request.POST)
                if form.is_valid():
                    new_form = form.save(commit=False)
                    new_form.user = request.user
                    new_form.save()

                    card_id = new_form.card_id
                    messages.success(request, "Card Added Successfully.")
                    return redirect("account:dashboard")
            else:
                form = CreditCardForm()

        else:
            messages.warning(request, "Your account is still under review. Your account will be active once your identity is verified")
            return redirect("account:account")
    else:
        messages.warning(request, 'You need to login to access the dashboard')
        return redirect('userauths:sign-in')

    context= {
        'kyc': kyc,
        'account': account,
        'form': form,
        'credit_card': credit_card,
    }

    return render(request , 'account/dashboard.html', context)