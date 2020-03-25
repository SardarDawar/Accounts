from django.shortcuts import render,redirect
# from django.contrib.auth.decorators import lo
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
from .forms import EditProfileForm

@login_required
def profile_view(request):
    return render(request, 'webaccount/profile.html', {})

def index_view(request):
    # if request.user.is_authenticated and request.user.is_superuser:
    if request.user.is_authenticated:
        return redirect(reverse('profile_url'))
    else:
        if request.method != "POST":
            return render(request, 'webaccount/login.html', {})
        # elif request.method == "GET":
        else:
        # if authenticate
            try:
                user = authenticate(username=request.POST['username'], password = request.POST['password'])
            except:
                messages.error(request, "Credentials are invalid.")
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('profile_url'))
                else:
                    messages.error(request, "User account has been deactivate")
            else:
                if request.POST['username'] == '' and request.POST['password'] == '':
                    messages.error(request, "Both username and password are empty.")
                elif request.POST['username'] == '':
                    messages.error(request, "Username is empty.")
                elif request.POST['password'] == '':
                    messages.error(request, "Password is empty.")
        return render(request, 'webaccount/login.html', {})

# @login_required
# def logout_view(request):
#     logout()

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "User has been logout successfully.")
    return redirect(reverse("index_url"))

# # Password Set View By The User...
# def password_set_user(request):
#     return render(request, 'webaccount/password_set_user.html', {})


@login_required()
def change_password(request):
    if request.method != 'POST':
        form = PasswordChangeForm(user=request.user)
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password has been updated.')
            if request.user.is_superuser:
                logout(request)
                return redirect(reverse('admin:login'))
            else:
                logout(request)
                return redirect(reverse('index_url'))
    return render(request, 'webaccount/change_password.html', {'form': form, 'section': "editProfile"})




@login_required()
def edit_profile(request):
    if request.method!='POST':
        form = EditProfileForm(instance = request.user)
    else:
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            # return redirect('profile', username = request.user.username)
            # return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
            return redirect(reverse('index_url'))
    return render(request, 'webaccount/edit_profile.html',{'form' : form})
