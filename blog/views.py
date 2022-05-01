from ast import Return
import re
from django.apps import AppConfig
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import  *
from rest_framework.views import APIView
from . import serializers
from rest_framework.response import Response
from rest_framework import status


class IndexPage(TemplateView):
    def get (self, request, **kwargs):
        article_data = []
        all_articles = Article.objects.all().order_by('-created_at')[:8]

        for article in all_articles:
            article_data.append({
                'title': article.title,
                'cover': article.cover.url,
                'created_at': article.created_at.date(),
                'category': article.category.title,

            })
        
        promote_data = []
        all_articles_promote = Article.objects.filter(promote=True)

        for article in all_articles_promote:
            promote_data.append({
                'title': article.title,
                'cover': article.cover.url if article.cover else None,
                'created_at': article.created_at.date(),
                'category': article.category.title,
                'author': article.author.user.first_name + ' ' + article.author.user.last_name,
                'avatar': article.author.avatar.url if article.author.avatar else None,

            })

        context = {
            'article_data': article_data,
            'promote_data': promote_data,
        }

        return render(request, 'index.html', context)

class ContactPage(TemplateView):
    template_name='contact.html'



class AllArticleAPIView(APIView):

    def get(self, request):
        try:
            all_articles = Article.objects.all().order_by('-created_at')[:8]
            data=[]

            for article in all_articles:
                data.append(
                    {'title': article.title,}
                )

            return Response({'data':data}, status=status.HTTP_200_OK)


        except: return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SingleArticleAPIView(APIView):
    
    def get(self, request, format=None):
        try:
            article_title = request.GET['article_title']
            article = Article.objects.filter(title__contains = article_title)
            serialized_data = serializers.SingleArticleSerializer(article, many=True)
            data = serialized_data.data

            return Response({'data': data}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchArticleAPIView(APIView):
    
    def get(self, request, format=None):
        try:
            from django.db.models import Q
            query = request.GET['query']
            articles = Article.objects.filter(Q(content__icontains=query))
            serialized_data= serializers.SearchArticleSerializer(articles, many=True)
            data= serialized_data.data
            return Response({'data': data}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SubmitArticleAPIView(APIView):
    
    def post(self, request, format=None):

        try:
            serializer = serializers.SubmitArticleSerializer(data=request.data)
            if serializer.is_valid():
                title = serializer.data.get('title')
                cover = request.FILES['cover']
                content = serializer.data.get('content')
                category_id = serializer.data.get('category_id')
                author_id = serializer.data.get('author_id')
                promote = serializer.data.get('promote')
            else:
                return Response({'status':'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(id=author_id)
            author = UserProfile.objects.get(user = user)
            category = Category.objects.get(id=category_id)

            article = Article()
            article.title = title
            article.cover = cover
            article.content = content
            article.category = category
            article.author = author
            article.promote = promote
            article.save()

            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            

class UpdateArticleAPIView(APIView):
    
    def post(self, request, format=None):
        try:
            serializer = serializers.UpdateArticleCoverSerializer(data=request.data)
            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
                cover = request.FILES['cover']
            else:
                return Response({'stats': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

            Article.objects.filter(id=article_id).update(cover=cover)
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)


        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteArticleAPIView(APIView):
    
    def post(self, request, format=None):
        try:
            serializer = serializers.DeleteArticleSerializer(data=request.data)

            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
            else:
                return Response({'status': 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

            Article.objects.filter(id=article_id).delete()

            return Response({'status':'OK'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                          