from django.urls import path

from . import views


urlpatterns = [
    path('<int:id>', views.CustomUserDetailAPIView.as_view(), name='customuser-detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

