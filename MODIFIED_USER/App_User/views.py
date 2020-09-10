from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.http import HttpResponse


### authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate

### models and forms
from .models import Profile
from .forms import SignupForm,ProfileForm

##
from django.contrib import messages


def sign_up(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account is created')
            return HttpResponse("Account is Created")
    return render(request,'App_Login/sign_up.html',{'form':form})





def login_user(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            
            ## username is the email
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username,password = password)
            if user is not None:
                login(request,user)
                return HttpResponse("You are logged in")
    return render(request,'App_Login/login.html',{'form':form})


@login_required
def logout_user(request):
    logout(request)
    messages.warning(request,"You are logged out")
    return HttpResponse("User is Logged Out")



## normally in user.py we add this user to the profile
## then find it but in here we add it with the dispacher

@login_required
def user_profile(request):
    profile = Profile.objects.get(user = request.user)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST,instance=profile)
        form.save()
        messages.success(request,"change saved")
        form = ProfileForm(instance=profile)
        return HttpResponse("User is changed")

    return render(request,'App_Login/change_profile.html',{'form':form})
