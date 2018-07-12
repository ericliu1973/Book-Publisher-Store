from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from hello.forms import SearchForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import  reverse
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})


# Create your views here.
@login_required
def dashboard(request):
    user=request.user.first_name
    request.session['is_login'] =True
    print('*******************************************************************')
    print(request.session.session_key)
    print (request.session.keys())
    print(request.session.items())
    print('*******************************************************************')
    if request.method=='POST':
         search_form=SearchForm(data=request.POST)
         if search_form.is_valid():
             cd= search_form.cleaned_data
             s_type = cd['search_type']
             keyword = cd['search_words']
             return HttpResponseRedirect(reverse("hello:search",kwargs={'s_type':s_type,'keyword':keyword}))

    form=SearchForm()
    return render(request, 'account/dashboard.html', {'section': 'dashboard','name':user,'form':form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})
