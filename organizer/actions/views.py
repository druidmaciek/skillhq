from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import Action

@login_required
def action_like(request):
    action_id = request.GET.get('id')
    action_str = request.GET.get('action')
    if action_id and action_str:
        try:
            action = Action.objects.get(id=action_id)
            if action_str == 'like':
                print('action is like adding user')
                action.users_like.add(request.user)
                messages.success(request, 'Liked...')
            elif action_str == 'unlike':
                print('action is unlike removing user')
                messages.success(request, 'Unliked...')
                action.users_like.remove(request.user)

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            pass
    messages.error(request, 'Error trying to like/unlike...')
    return JsonResponse({'status': 'error'})
