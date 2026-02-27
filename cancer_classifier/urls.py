from django.urls import path
from . import views
from .views import (
    SkinConditionListView,
    SkinConditionDetailView,
    ChatListView, UserImagesView ,
    HealthTopicListView,
    HealthTopicDetailView,
    )
urlpatterns = [
     path('', views.dashboard, name='dashboard'),
    path('cancer-detect/', views.predict_cancer, name='index'),
    path('user-images/', UserImagesView.as_view(), name='user_images'),
    path('bot/', ChatListView.as_view(), name='bot'),  
    path('about-us/', views.AboutUs, name='about-us'),
    path('skin-condition/', SkinConditionListView.as_view(), name='skincondition_list'),
    path('skin-condition/<int:pk>/', SkinConditionDetailView.as_view(), name='skincondition_detail'),
    path('health-topics/', HealthTopicListView.as_view(), name='healthtopic_list'),
    path('health-topics/<int:pk>/', HealthTopicDetailView.as_view(), name='healthtopic_detail'),
]
