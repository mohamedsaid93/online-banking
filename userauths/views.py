from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from userauths.models import User

# Create your views here.
def RegisterView(request):
    
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in.")
        return redirect('account:account')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        try:
            if form.is_valid:
                form.save()
                                                                                                                                            # new_user = form.save()
                username = form.cleaned_data.get('username')
                                                                                                                                            #username = request.POST.get('username')
                messages.success(request, f"Hey {username}, your account was created successfuly.")
                                                                                                                                            # new_user = authenticate(username = form.cleaned_date.get('email))
                new_user = authenticate(username = form.cleaned_data['email'], password = form.cleaned_data['password1'])

                login(request, new_user)
                return redirect('account:account')
        except:

            messages.warning(request, "You have errors. Please make sure the passwords are made up from letters and numbers and 8 digits long minimum.")
            return redirect('userauths:sign-up') 



    else:
        form = UserRegisterForm()


    context = {
        'form': form
    }

    return render(request, 'userauths/sign-up.html', context)


def LoginView(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('account:account')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged.')
                return redirect('account:account')
            
            else:
                messages.warning(request, 'Wrong password. Please try again!.')
                return redirect('userauths:sign-in')

        except:
            messages.warning(request, 'This email has not been associated with any user. Please try again!')


    return render(request, 'userauths/sign-in.html')


def LogoutView(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect("userauths:sign-in")