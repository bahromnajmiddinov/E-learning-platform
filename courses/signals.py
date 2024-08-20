from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from accounts.models import CustomUser
from .models import Subscription, Lesson


@receiver(post_save, sender=CustomUser)
def post_save_subscription(sender, instance: CustomUser, created, **kwargs):
    if created:
        subscription = Subscription.objects.create(user=sender)


@receiver(post_save, sender=Lesson)
def post_save_course(sender, instance: Lesson, created, **kwargs):
    if created:
        for obj in instance.course.subscriptioncourse.all():
            obj.completed_percentage = (obj.completed_lessons.count() / obj.course.lessons.count) * 100
            obj.save()
    