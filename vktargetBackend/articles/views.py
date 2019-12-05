from django.shortcuts import render
from rest_framework import mixins, generics
from articles.models import ArticleModel
from articles.serializers import PostSerializer


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = PostSerializer


class ArticlesList(generics.ListCreateAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = PostSerializer

