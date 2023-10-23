from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import CreditCard
from account.models import Account
from decimal import Decimal
from django.template.defaulttags import register


@register.filter()
def nounderscore(value):
    value = value.replace('_', ' ')
    return value.title()

def card_detail(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    context = {
        'account': account,
        'credit_card': credit_card,
    }

    return render(request, "credit_card/card-detail.html", context)

def withdraw_fund(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")

        if credit_card.amount >= Decimal(amount) and credit_card.amount != 0.00:
            account.account_balance += Decimal(amount)
            account.save()

            credit_card.amount -= Decimal(amount)
            credit_card.save()

            messages.success(request, "Withdrawal Success.")
            return redirect("core:card-detail", credit_card.card_id)
        
        elif credit_card.amount == 0.00:
            messages.warning(request, "Insufficient Fund.")
            return redirect("core:card-detail", credit_card.card_id)
        
        else:
            messages.warning(request, "Insufficient Fund.")
            return redirect("core:card-detail", credit_card.card_id)

def delete_card(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    if credit_card.amount > 0:
        account.account_balance += credit_card.amount
        account.save()

        credit_card.delete()
        messages.warning(request, "Card Deleted Sussessfully.")
        return redirect("account:dashboard")
    
    credit_card.delete()
    messages.warning(request, "Card Deleted Sussessfully.")
    return redirect("account:dashboard")


def fund_credit_card(request, card_id):
    account = Account.objects.get(user=request.user)                        # account = request.user.account
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    if request.mthod == "POST":
        amount = request.POST.get("funding_amount")

        if Decimal(amount) <= account.account_balance:
            account.account_balance -= Decimal(amount)
            account.save()

            credit_card.amount += Decimal(amount)
            credit_card.save()

            messages.success(request, "Funding Sussessfully.")
            return redirect("core:credit-detail", credit_card.card_id)
        
        else:
            messages.warning(request, "Insufficient Fund.")
            return redirect("core:credit-detail", credit_card.card_id)
        


        


