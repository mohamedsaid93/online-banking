from django.shortcuts import render, redirect
from account.models import Account, KYC
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from core.models import Transaction
from decimal import Decimal 

@login_required
def search_users_account_numbers(request):
    account = Account.objects.all()

    query = request.POST.get("account_number")
    
    if query:
        account = Account.objects.exclude(user=request.user).filter(
            Q(account_status="active") &
            (Q(account_number=query) | Q(account_id=query))
            ).distinct()

    context = {
        'account': account,
        'query': query
    }
    return render(request, 'transfer/search-user-by-account-number.html', context)

def AmountTransfer(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except:
        messages.warning(request, 'Account does not exist.')
        return redirect("core:account-search")
    
    context = {
        'account': account,
    }

    return render(request, 'transfer/amount-transfer.html', context)

@login_required
def AmountTransferProcess(request, account_number):
    account = Account.objects.get(account_number=account_number) # account that the money would be sent to
    sender = request.user # person than is logged in
    reciever = account.user # person that is going to recieve the money

    sender_account = request.user.account # user's account that would send the money
    reciever_account = account # person account that would recieve the money

    if request.method == "POST":
        amount = request.POST.get("amount-send")
        description = request.POST.get("description")

        if sender_account.account_balance >= Decimal(amount):
            new_transaction = Transaction.objects.create(
                user = request.user,
                amount = amount,
                description = description,
                reciever = reciever,
                sender = sender,
                sender_account = sender_account,
                reciever_account = reciever_account,
                status = "processing",
                transaction_type = "transfer"
            )
            new_transaction.save()

            # Get the id of the transaction that was created now
            transaction_id = new_transaction.transaction_id
            return redirect("core:transfer-confirmation", account.account_number, transaction_id)
        
        else:
            messages.warning(request, "Insufficient Fund.")
            return redirect("core:amount-transfer", account.account_number)
        
    else:
        messages.warning(request, "Error Occured, Try again later")
        return redirect("account:account")
    
@login_required
def TransferConfirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number = account_number)
        transaction = Transaction.objects.get(transaction_id = transaction_id)
    except:
        messages.warning(request, "Transaction does not exist")
        return redirect("account:account") 

    context = {
        'account': account,
        'transaction': transaction,
    }

    return render(request, 'transfer/transfer-confirmation.html', context)

@login_required
def TransferProcess(request, account_number, transaction_id):
    account = Account.objects.get(account_number = account_number)
    transaction = Transaction.objects.get(transaction_id = transaction_id)

    sender = request.user # person than is logged in
    reciever = account.user # person that is going to recieve the money

    sender_account = request.user.account # user's account that would send the money
    reciever_account = account # person account that would recieve the money

    #completed = False

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")

        if pin_number == sender_account.pin_number:
            transaction.status = "completed"
            transaction.save()

            # Remove amount that was sent from the sender account balance
            sender_account.account_balance -= transaction.amount
            sender_account.save()

            # Add the amount that was sent to the reciever account balance
            account.account_balance += transaction.amount
            account.save()

            messages.success(request, "Transfer Successful.")
            return redirect("core:transfer-completed", account.account_number, transaction.transaction_id)
        
        else:
            messages.warning(request, "Incorrect Pin.")
            return redirect("core:transfer-confirmation", account.account_number, transaction.transaction_id)
        
    else:
        messages.warning(request, "An error occured, Try again later")
        return redirect("account:account")
    
@login_required
def TransferCompleted(request, account_number, transaction_id):
    
    try:
        account = Account.objects.get(account_number = account_number)
        transaction = Transaction.objects.get(transaction_id = transaction_id)

    except:
        messages.warning(request, "Transfar does not exist")
        return redirect("account:account") 

    context = {
        'account': account,
        'transaction': transaction,
    }

    return render(request, 'transfer/transfer-completed.html', context)




        