from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import AddResourceForm
from .models import Resource


@login_required
def dashboard(request):

    # TODO implement in front-end and delete this
    # TEMPORARY, ultimately it should be called by Vue.js axios in front end
    if request.method == "POST":
        form = AddResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.user = request.user
            resource.save()
    else:
        form = AddResourceForm()

    resources = Resource.objects.filter(user=request.user)
    return render(request, 'dashboard/dashboard.html',
                  {'section': 'dashboard',
                   'resources': resources,
                   'form': form})
