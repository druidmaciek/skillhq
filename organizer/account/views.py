from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from .forms import ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Profile



def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(data=request.POST)
        profile_form = ProfileEditForm(data=request.POST, files=request.FILES)
        if user_form.is_valid(): #and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            if profile_form.cleaned_data['private'] == '1':
                profile.private = True
            else:
                profile.private = False
            profile.save()
            messages.success(request, "Profile Updated...")
        else:
            # TODO more verbose error
            messages.error(request, 'Error updating profile...')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required()
def delete(request):
    request.user.delete()
    return render(request, 'account/delete_confirm.html')