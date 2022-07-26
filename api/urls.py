from django.urls import path
from .views import article_list,article_detail,ArticleListAPI ,ArticleDetails,GenericAPIView
urlpatterns = [
    # path('article/',article_list),
    path('article/',ArticleListAPI.as_view()),    
    path('detail/<int:id>/',ArticleDetails.as_view()),
    path('generic/article/',GenericAPIView.as_view()),
    path('generic/article/<int:id>/',GenericAPIView.as_view())
    # path('detail/<int:pk>/',article_detail),
    

]