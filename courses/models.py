from django.db import models

from accounts.models import CustomUser


class Course(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.title} | {self.author} | {self.price}'
    
    @property
    def get_student_count(self):
        return self.enrollments.count()
    
    @property
    def get_lessons_count(self):
        return self.lessons.count()



class Lesson(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.title} | {self.course} |'


class Group(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name} | {self.course} | {self.members.count()} members'


class Subscription(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, through='SubscriptionCourse', related_name='enrollments')
    

class SubscriptionCourse(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)
    completed_lessons = models.ManyToManyField(Lesson, through='CompletedLesson')
    completed_percentage = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    class Meta:
        ordering = ['-id']


class CompletedLesson(models.Model):
    subscription_course = models.ForeignKey(SubscriptionCourse, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-id']
