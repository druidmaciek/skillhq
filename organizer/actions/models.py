from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class PublicManager(models.Manager):
    def get_queryset(self):
        return super(PublicManager,
                     self).get_queryset()\
    .filter(user__profile__private=False)


class Action(models.Model):
    user = models.ForeignKey(User,
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    users_like = models.ManyToManyField(User,
                                        related_name='actions_liked',
                                        blank=True)

    objects = models.Manager()
    public = PublicManager()

    class Meta:
        ordering = ('-created',)
