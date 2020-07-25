from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import AddResourceForm
from .models import Note, Resource, Task


@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.first_login:
        profile.first_login = False
        profile.save()
        return redirect(reverse_lazy('account:edit'))

    resources = Resource.objects.filter(user=request.user)
    tasks = Task.objects.filter(resource__user=request.user)
    return render(
        request,
        "dashboard/dashboard.html",
        {
            "section": "dashboard",
            "resources": resources,
            "tasks": tasks,
            "form": AddResourceForm(),
        },
    )


@login_required
def resource_detail(request, rid):
    resource = get_object_or_404(Resource, pk=rid)
    if request.user.id != resource.user.id:
        redirect("/")
    return render(
        request,
        "dashboard/resource/detail.html",
        {"section": "detail", "resource": resource, "form": AddResourceForm()},
    )


@login_required
def new_note(request):
    return render(request, 'dashboard/resource/note.html',
                  {'section': 'note',
                   'note': None})


@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.user.id != note.resource.user.id:
        redirect("/")
    return render(
        request, "dashboard/resource/note.html", {"section": "note",
                                                  "note": note}
    )
