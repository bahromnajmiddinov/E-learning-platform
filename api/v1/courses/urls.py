from django.urls import path

from . import views


urlpatterns = [
    path('', views.CourseAPIView.as_view(), name='course-list'),
    path('<int:pk>/', views.CourseDetailAPIView.as_view(), name='course-detail'),
    path('<int:pk>/lessons/', views.LessonAPIView.as_view(), name='lesson-list'),
    path('<int:pk>/lessons/<int:lesson_pk>/', views.LessonDetailAPIView.as_view(), name='lesson-detail'),
    path('<int:pk>/groups/', views.GroupAPIView.as_view(), name='group-list'),
    path('<int:pk>/groups/<int:group_id>/', views.GroupDetailAPIView.as_view(), name='group-detail'),
    path('<int:pk>/enroll/', views.enroll_course, name='enroll-course'),
    path('<int:pk>/lessons/<int:lesson_pk>/complete/', views.lesson_complete, name='lesson-complete'),
]

