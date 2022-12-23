from django.urls import path, include
# from .views import CreateUserAPIView
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('signup/', views.CreateUserAPIView.as_view()),
    path('', include(router.urls))

]
