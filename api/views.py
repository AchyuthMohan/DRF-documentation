from configparser import NoSectionError
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from grpc import Status
from rest_framework.parsers import JSONParser
from yaml import serialize
from .models import Article
from django.views.decorators.csrf import csrf_exempt
from .serializers import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
# Create your views here.
# Generic API View

#  The real needful view class XD
class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class=ArticleSerializer
    queryset=Article.objects.all()


# Generic Viewset

# Here basically we can read the models as list, as separate object, update individually , add a new one simply by using these two lines of code
# here we can add the required functionalities.

# class ArticleViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,
# mixins.DestroyModelMixin):
#     serializer_class=ArticleSerializer
#     queryset=Article.objects.all()


# Generic API View
class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin,mixins.CreateModelMixin,
mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    serializer_class=ArticleSerializer
    queryset=Article.objects.all()
    lookup_field='id'
    # authentication_classes=[SessionAuthentication,BasicAuthentication]   #it checks for session authentication classes initially then if its absent then it will check for BasicAuthentication
    # authentication_classes=[TokenAuthentication]
    # permission_classes=[IsAuthenticated]

    def get(self,request,id=None):
        if id:                     #for getting a specific onject by sendig id
            return self.retrieve(request)
        else:                     #for getting the list of objects
            return self.list(request)
    def post(self, request):
        return self.create(request)
    def put(self,request,id=None ):
        return self.update(request, id)
    def delete(self, request, id):
        return self.destroy(request,id)


class ArticleListAPI(APIView):
    def get(self,request):
        articles=Article.objects.all()
        serializer=ArticleSerializer(articles,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):
    def get_object(self, id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        article=self.get_object(id)
        serializer=ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request,id):
        article=self.get_object(id)
        serializer=ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        article=self.get_object(id)
        article.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)



           # Funtion Based views...
@api_view(['GET','POST'])
def article_list(request):
    if request.method=='GET':
        articles=Article.objects.all()
        serializer=ArticleSerializer(articles,many=True)
        return Response(serializer.data)

    elif request.method=="POST":
        serializer=ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def article_detail(request,pk):
    try:
        article=Article.objects.get(pk=pk)

    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method=="GET":
        serializer=ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method=="PUT":
        serializer=ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method=="DELETE":
        article.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

