from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('resources/', views.resources_list, name='resource_list'),
    path("resource/<int:rid>/", views.resource_detail, name="resource_details"),
    path("notes/list/", views.note_list, name='note_list'),
    path("notes/new/", views.new_note, name='new_note'),
    path("notes/<int:note_id>/", views.note_detail, name="note_detail"),
    path("discussion/", views.discussions, name='discussion_list'),
    path('discussion/new/', views.add_discussion, name='new_discussion'),
    path('discussion/<int:post_id>/newComment/', views.add_comment, name='add_comment'),
    path('discussion/<int:comment_id>/reply/', views.add_reply, name='add_reply'),
    path('discussion/<int:post_id>/', views.post_detail, name='discussion_detail'),
    path('learningLog/new/', views.add_learning_log, name='add_log'),
    path('feedback/', views.add_feedback, name='feedback'),
    path('changelog/', views.changelog, name='changelog'),

    # stripe
    # path('config/', views.stripe_config),
    # path('create-checkout-session/', views.create_checkout_session),
    # path('success/', views.SuccessView.as_view()),
    # path('cancelled/', views.CancelledView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
