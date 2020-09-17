from django.urls import path

from day05 import views

urlpatterns = [
    path('books/', views.BookAPIView.as_view()),
    path('books/<str:id>', views.BookAPIView.as_view()),

    path('gen/', views.BookGenericsAPIView.as_view()),
    path('gen/<str:id>/', views.BookGenericsAPIView.as_view()),

    path("mix/", views.BookGenericMixinView.as_view()),
    path("mix/<str:id>/", views.BookGenericMixinView.as_view()),

    # path("set/", views.BookModelViewSet.as_view()),
    # path("set/<str:id>/", views.BookModelViewSet.as_view()),

    path("em/", views.EmpGenericsAPIView.as_view()),
    path("em/<str:id>/", views.EmpGenericsAPIView.as_view()),

    path("emp/", views.EmpModelViewSet.as_view({"post": "user_login"})),
    # path("emp/<str:id>/", views.EmpModelViewSet.as_view({"post": "user_login"})),

    path("emp/re/", views.EmpModelViewSet.as_view({"post": "register", })),
    # path("emp/<str:id>/", views.EmpModelViewSet.as_view({"post": "register",})),

]
