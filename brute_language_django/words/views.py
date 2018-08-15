from django.shortcuts import render
from rest_framework import generics
from .models import Article, Pos, Definition
from .serializers import WordDetailsSerializer


class WordDetails(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = WordDetailsSerializer

    def get_queryset(self):
        query_word = self.request.query_params.get('q', None)
        return Article.objects.filter(word=query_word)
