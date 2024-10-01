from django.shortcuts import render
from django.views import View
import json
from django.views.generic import DetailView
from utilities import requests
from django.conf import settings
from django.core.paginator import Paginator


class BlogListView(View):
    def get(self, request):
        blog = requests.send(url=f'/blog/', method='GET', data=None)
        page_number = request.GET.get("page")

        paginator = Paginator(blog['result'], 40)

        page_obj = paginator.get_page(page_number)

        return render(request, 'blog/article-grid.html', {'page_obj': page_obj, 'base_url': settings.BASE_URL})


class CategoryDetailView(View):
    def get(self, request, category_id):
        category = requests.send(url=f'blog/category/{category_id}', method='GET', data=None)

        page_number = request.GET.get("page")

        paginator = Paginator(category['result']['blogs'], 40)

        page_obj = paginator.get_page(page_number)

        return render(request, 'blog/article-grid.html',
                      {'page_obj': page_obj, 'base_url': settings.BASE_URL, 'category': True,
                       'category_title': category['result']['title']})


class BlogDetailView(View):
    def get(self, request, blog_id):
        blog = requests.send(url=f'/blog/{blog_id}', method='GET', data=None)
        blog_category = requests.send(url=f'blog/category/', method='GET', data=None)
        last_blogs = requests.send(url='blog/', method='GET', data=None)

        last_blogs = sorted(last_blogs['result'], key=lambda blog: blog['register_date'])

        data = {
            'blog': blog['result'],
            'blog_category': blog_category['result'],
            'last_blogs': last_blogs
        }

        data['base_url'] = settings.BASE_URL

        return render(request, 'blog/article-details.html', data)
