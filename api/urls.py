from django.urls import path, include

from api import views

urlpatterns = [
    path('users/', views.EmployeeAPIView.as_view()),
    path('users/<str:id>/', views.EmployeeAPIView.as_view())

]
