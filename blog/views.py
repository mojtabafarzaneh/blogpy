import re
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import  *


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