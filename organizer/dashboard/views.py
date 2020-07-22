from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddResourceForm
from .models import Resource, Note, Task


@login_required
def dashboard(request):
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
def note_detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.user.id != note.resource.user.id:
        redirect("/")
    return render(
        request, "dashboard/resource/note.html", {"section": "note", "note": note}
    )
