from django.contrib import admin

from .models import Course, Lesson, Group, Subscription, CompletedLesson, SubscriptionCourse


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'created_at', 'updated_at']
    list_filter = ['author', 'created_at', 'updated_at'  ]
    search_fields = ['title', 'author', 'created_at', 'updated_at'  ]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'created_at', 'updated_at' ]
    list_filter = ['course', 'created_at', 'updated_at'  ]
    search_fields = ['title']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'created_at', 'updated_at']
    list_filter = ['course', 'created_at', 'updated_at']
    search_fields = ['name', 'course', 'created_at', 'updated_at' ]
    

@admin.register(CompletedLesson)
class CompletedLessonAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'completed_at', 'score']
    list_filter = ['lesson', 'completed_at','score']


@admin.register(SubscriptionCourse)
class SubscriptionCourseAdmin(admin.ModelAdmin):
    list_display = ['started_at', 'ended_at', 'completed_percentage']
    list_filter = ['started_at', 'ended_at', 'completed_percentage']
    

admin.site.register(Subscription)
