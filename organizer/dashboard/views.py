from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import AddResourceForm
from .models import Resource


@login_required
def dashboard(request):
    resources = Resource.objects.filter(user=request.user)
    return render(request, 'dashboard/dashboard.html',
                  {'section': 'dashboard',
                   'resources': resources,
                   'form': AddResourceForm()})


@require_POST
@login_required()
def add_resource(request):
    # TODO implement in front-end and delete this
    # TEMPORARY, ultimately it should be called by Vue.js axios in front end
    form = AddResourceForm(request.POST)
    if form.is_valid():
        resource = form.save(commit=False)
        resource.user = request.user
        resource.save()
    print(form.errors)
    return redirect('/')


@login_required()
def resource_detail(request, rid):
    resource = get_object_or_404(Resource, pk=rid)
    if request.user.id != resource.user.id:
        redirect('/')
    return render(request, 'dashboard/resource/detail.html', {
        'section': 'detail',
        'resource': resource
    })
