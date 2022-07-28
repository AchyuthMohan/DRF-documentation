from django.urls import path,include
from .views import article_list,article_detail,ArticleListAPI ,ArticleDetails,GenericAPIView,ArticleViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('article',ArticleViewSet, basename='article')
urlpatterns = [
    # path('article/',article_list),
    path('',include(router.urls)),  #the required one as per the current situation
    # path('article/',ArticleListAPI.as_view()),    
    path('detail/<int:id>/',ArticleDetails.as_view()),
    path('generic/article/',GenericAPIView.as_view()),
    path('generic/article/<int:id>/',GenericAPIView.as_view())
    # path('detail/<int:pk>/',article_detail),
    

]