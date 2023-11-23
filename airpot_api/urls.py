from django.urls import path, include
from airpot_api import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('7DaysForcast', views.SevenDaysForcastViewSet, basename='7 Days Forcast')
router.register('PollutantsForcast', views.PollutantsForcastViewSet, basename='PollutantsForcast')
router.register('GetForcast', views.GetForcastViewSet, basename='GetForcast')
router.register('AfordUserProfile', views.UserProfileViewSet)


urlpatterns = [
    path('prediction/', views.AirpotAfordApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls))
]