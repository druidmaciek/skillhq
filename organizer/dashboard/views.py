from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import AddResourceForm, AddDiscussionForm, AddCommentForm, AddCommentReplyForm, AddLearningLogForm
from .models import Note, Resource, Task, Subject, Post, Comment, LearningLog
from actions.models import Action
from actions.utils import create_action

@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.first_login:
        profile.first_login = False
        profile.save()
        return redirect(reverse_lazy('account:edit'))

    # actions
    actions = Action.objects.all()
    actions = actions[:10]

    resources = Resource.objects.filter(user=request.user)
    tasks = Task.objects.filter(resource__user=request.user)
    subjects = Subject.objects.all()
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
    return render(request, 'dashboard/dashboard_notes.html', {
        'section': 'notes',
        'notes': notes,
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

    subjects = request.user.subjects.all()
    print(subject.name if subject else None)
    return render(
        request,
        "dashboard/dashboard_resources.html",
        {
            "section": "resources",
            "resources": resources,
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
    return render(request, 'dashboard/dashboard_discussion.html',{
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
    else:
        messages.error(request, "Can't add to log")
    return redirect(reverse_lazy('dashboard:dashboard'))
