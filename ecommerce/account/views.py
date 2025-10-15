from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm
# Vizualizare pentru Inregistrare

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            user = form.save()
            
            login(request, user)
            
            messages.success(request, f"You have successfully registered! Welcome {user.username}")
            
            return redirect("store")
        # else:
        #     messages.error(request, "Unsuccessful registration. Invalid information.")
            
    else:
        form = CustomUserCreationForm()
        
    return render(request=request, template_name="account/register.html", context={"form":form})


# Vizualizare pentru Authentificare
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")        
                return redirect("store")
            
            else:
                messages.error(request, "Invalid username or password.")
        
        else:
            messages.error(request, "Invalid username or password.")
            
    form = AuthenticationForm()
    return render(request, template_name="account/login.html", context={"form": form})



# Vizualizare pentru Deconectare
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("store")