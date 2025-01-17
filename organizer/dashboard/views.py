from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .forms import AddResourceForm, AddDiscussionForm, AddCommentForm, AddCommentReplyForm, AddLearningLogForm, AddFeedbackForm
from .models import Note, Resource, Task, Subject, Post, Comment, LearningLog
from actions.models import Action
from actions.utils import create_action


@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.first_login:
        profile.first_login = False
        profile.save()
        create_action(request.user, 'joined SkillHQ')
        return redirect(reverse_lazy('account:edit'))


    if request.user.profile.private:
        actions = Action.objects.filter(user=request.user)
    else:
        actions = Action.public.all()
    actions = actions[:300]

    resources = Resource.objects.filter(user=request.user)
    tasks = Task.objects.filter(resource__user=request.user)
    subjects = Subject.objects.all()
    recent_posts = Post.objects.all()[:5]
    return render(
        request,
        "dashboard/dashboard.html",
        {
            "section": "dashboard",
            "resources": resources,
            "tasks": tasks,
            "form": AddResourceForm(),
            "all_subjects": subjects,
            'actions': actions,
            'recent_posts': recent_posts,
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


@login_required
def note_list(request):
    notes = Note.objects.filter(resource__user=request.user)
    subjects = request.user.subjects.all()

    subject_filter = request.GET.get('subject')
    subject = None
    if subject_filter:
        subject = Subject.objects.get(name=subject_filter)
        notes = notes.filter(resource__subject=subject.name)

    return render(request, 'dashboard/dashboard_notes.html', {
        'section': 'notes',
        'notes': notes,
        'subjects': subjects,
        'selected_subject': subject.name if subject else None,
    })


@login_required
def resources_list(request):
    tasks = Task.objects.filter(resource__user=request.user)
    resources = Resource.objects.filter(user=request.user)

    subject_filter = request.GET.get('subject')
    subject = None
    if subject_filter:
        subject = Subject.objects.get(name=subject_filter)
        resources = resources.filter(subject=subject.name)

    resources_paused = resources.filter(status='Not Started/On Hold')
    resources_in_progress = resources.filter(status='In Progress')
    resources_completed = resources.filter(status="Completed")



    subjects = request.user.subjects.all()
    return render(
        request,
        "dashboard/dashboard_resources.html",
        {
            "section": "resources",
            "resources_paused": resources_paused,
            "resources_in_progress": resources_in_progress,
            "resources_completed": resources_completed,
            "tasks": tasks,
            "form": AddResourceForm(),
            'subjects': subjects,
            'selected_subject': subject.name if subject else None,
            "all_subjects": Subject.objects.all()
        },
    )


@login_required
def discussions(request):
    posts = Post.objects.all()
    return render(request, 'dashboard/dashboard_discussion.html', {
        'section': 'discussion',
        'posts': posts,
    })


@login_required
def add_discussion(request):
    error = None
    if request.method == "POST":
        form = AddDiscussionForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, f'"{post.title}" added.')
            create_action(request.user, 'started discussion', post)
            return redirect(reverse_lazy('dashboard:discussion_list'))
        else:
            error = "Error adding post"
    return render(request, 'dashboard/posts/new.html', {
        'form': AddDiscussionForm(),
        'error': error
    })


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'dashboard/posts/detail.html', {
        'post': post
    })


@login_required
@require_POST
def add_comment(request, post_id):
    form = AddCommentForm(data=request.POST)
    post = get_object_or_404(Post, pk=post_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        form.save()
        messages.success(request, 'comment added.')
    else:
        messages.error(request, "Can't add comment.")
    return redirect(reverse_lazy("dashboard:discussion_detail", args=(post.id,)))


@login_required
@require_POST
def add_reply(request, comment_id):
    form = AddCommentReplyForm(data=request.POST)
    comment = get_object_or_404(Comment, pk=comment_id)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.user = request.user
        reply.comment = comment
        form.save()
        messages.success(request, 'comment added.')
    else:
        messages.error(request, "Can't add comment.")
    return redirect(reverse_lazy("dashboard:discussion_detail", args=(comment.post.id,)))


@login_required
@require_POST
def add_learning_log(request):
    form = AddLearningLogForm(data=request.POST)
    if form.is_valid():
        log = form.save(commit=False)
        log.user = request.user
        log.save()
        messages.success(request, 'Learning achievement logged')
        create_action(request.user, 'learned today:', log)
    else:
        messages.error(request, "Can't add to log")
    return redirect(reverse_lazy('dashboard:dashboard'))


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    if user.profile.private and request.user != user:
        return redirect(reverse_lazy('dashboard:dashboard'))
    return render(request, 'dashboard/profile/profile.html', {
        'user': user
    })



@login_required
@require_POST
def add_feedback(request):
    form = AddFeedbackForm(data=request.POST)
    if form.is_valid():
        feedback = form.save(commit=False)
        feedback.user = request.user
        feedback.save()
        messages.success(request, 'Feedback submitted! Thank you!')
    else:
        messages.error(request, 'Error while submitting feedback.')
    return redirect(reverse_lazy('dashboard:dashboard'))


def changelog(request):
    return render(request, 'info/changelog.html')
