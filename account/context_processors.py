from account.models import KYC

def kyc_context_processor(request):
    kycCP = KYC.objects.get(user=request.user)
    return dict(kycCP=kycCP)