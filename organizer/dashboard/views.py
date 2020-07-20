from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Resource


@login_required
def dashboard(request):
    resources = Resource.objects.filter(user=request.user)
    return render(request, 'dashboard/dashboard.html',
                  {'section': 'dashboard',
                   'resources': resources})
