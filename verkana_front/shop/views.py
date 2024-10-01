from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import requests
import json

from django.views.generic import DetailView
from utilities import requests
from django.conf import settings
from django.core.paginator import Paginator


class Main(View):
    def get(self, request):
        data = requests.send(url='home/', method='GET', data=None)
        data['base_url'] = settings.BASE_URL  # append base url to data

        data['products_by_price'] = sorted(data['products'], key=lambda x: x['product_after_discount'], reverse=True)[
                                    0:15]
        data['products_by_discount'] = sorted(data['products'], key=lambda x: x['product_discount'], reverse=True)[0:15]
        data['products_by_view'] = sorted(data['products'], key=lambda x: x['product_view_count'], reverse=True)[0:15]
        data['product_by_sell_count'] = sorted(data['products'], key=lambda x: x['product_sell_count'], reverse=True)[
                                        0:15]
        data['products_by_register_date'] = sorted(data['products'], key=lambda x: x['register_date'], reverse=True)[
                                            0:20]

        return render(request, 'shop/main.html', data)


class Shop(View):
    def get(self, request):
        orders = request.GET.get('orders')
        page_number = request.GET.get("page")

        print(orders, page_number)

        data = requests.send(url='product/', method='GET', data=None)

        if orders == 'discount':
            products = sorted(data['products'], key=lambda x: x['product_discount'], reverse=True)
        elif orders == 'view':
            products = sorted(data['products'], key=lambda x: x['product_view_count'], reverse=True)
        elif orders == 'sell_count':
            products = sorted(data['products'], key=lambda x: x['product_sell_count'], reverse=True)
        elif orders == 'price_gt':
            products = sorted(data['products'], key=lambda x: x['product_after_discount'], reverse=True)
        elif orders == 'price_lt':
            products = sorted(data['products'], key=lambda x: x['product_after_discount'])
        else:
            products = sorted(data['products'], key=lambda x: x['register_date'])
            orders = None

        for i in products:
            print(i['product_name'])

        paginator = Paginator(products, 30)

        page_obj = paginator.get_page(page_number)

        selling_products = requests.send(url='product/', method='GET', data=None)
        best_selling = sorted(selling_products['products'], key=lambda x: x['product_sell_count'])[0:5]

        context = {"page_obj": page_obj, 'base_url': settings.BASE_URL, 'title_of_result': 'لیست محصولات',
                   'type': 'shop', 'orders': orders, 'best_selling': best_selling}

        return render(request, "shop/shop.html", context)


class Search(View):
    def post(self, request):
        value = request.POST.get('value')
        category_id = request.POST.get('category_id')

        data = requests.send(url='product/product_search/', method='POST',
                             data={'product_name': value, 'category_id': category_id})
        data['base_url'] = settings.BASE_URL
        data['title_of_result'] = data['message']
        data['type'] = 'search'

        products = requests.send(url='product/', method='GET', data=None)
        data['best_selling'] = sorted(products['products'], key=lambda x: x['product_sell_count'])[0:5]

        return render(request, 'shop/shop.html', data)


# region details

class CategoryDetailView(View):
    def get(self, request, category_id):
        page_number = request.GET.get("page")

        data = requests.send(url=f'product/product_of_category/{category_id}', method='GET', data=None)
        selling_products = requests.send(url='product/', method='GET', data=None)
        best_selling = sorted(selling_products['products'], key=lambda x: x['product_sell_count'])[0:5]

        paginator = Paginator(data['result'], 30)

        page_obj = paginator.get_page(page_number)

        return render(request, 'shop/shop.html',
                      {'page_obj': page_obj, 'title_of_result': data['message'], 'best_selling': best_selling,
                       'base_url': settings.BASE_URL, 'type': 'shop', 'category_detail': True})


class ProductDetailView(View):
    def get(self, request, product_slug):
        if request.session.get('token'):
            auth = True
        else:
            auth = False

        product_detail = requests.send(url=f'product/get_product/{product_slug}/', method='GET', data=None)

        context = {"product_detail": product_detail,
                   'base_url': settings.BASE_URL,
                   'auth': auth}

        return render(request, 'shop/product-detail.html', context)


# endregion


# region others

class AboutUsView(View):
    def get(self, request):
        data = requests.send(url='', method='GET', data=None)

        return render(request, 'shop/about.html', data['result'][0])


class QuestionsView(View):
    def get(self, request):
        data = requests.send(url='repetitive_questions/', method='GET', data=None)

        return render(request, 'shop/faq.html', data)


class ContactUs(View):
    def get(self, request):
        data = requests.send(url='', method='GET', data=None)

        return render(request, 'shop/contact.html', data['result'][0])


# endregion


# region Partials

class HeaderPartial(View):
    def get(self, request):
        data = requests.send(url='', method='GET', data=None)
        product_groups = requests.send(url='product/product_group/', method='GET', data=None)

        data['base_url'] = settings.BASE_URL
        data['product_groups'] = product_groups['result']

        return render(request, 'shared/header.html', data)


class SideBarPartial(View):
    def get(self, request):
        product_groups = requests.send(url='product/product_group/', method='GET', data=None)

        data = {
            'product_groups': product_groups['result']
        }
        data['base_url'] = settings.BASE_URL

        return render(request, 'shared/sidebars.html', data)


class FooterPartial(View):
    def get(self, request):
        site_setting = requests.send(url='', method='GET', data=None)
        social_media = requests.send(url='social_media/', method='GET', data=None)
        product_groups = requests.send(url='product/product_group/', method='GET', data=None)

        data = {
            'site_setting': site_setting['result'],
            'social_media': social_media['result'],
            'product_groups': product_groups['result']
        }

        data['base_url'] = settings.BASE_URL

        return render(request, 'shared/footer.html', data)


class MixinViewPartial(View):
    def get(self, request):

        data = requests.send(url='product/mixin/', method='GET', data=None, headers=None)


        return render(request, 'shared/mixin.html', {'products': data['result'], 'base_url': settings.BASE_URL})


# endregion


# region comment

class SubmitCommentView(View):
    def post(self, request):

        if request.session.get('token'):
            try:
                comment = request.POST['comment']
                product_id = request.POST['product_id']
            except:
                return JsonResponse({'status': 'parrams_error'})

            data = requests.send(url='/comment/', method='POST', data={
                "comment": comment,
                "product": product_id,
                "rate": 0
            }, headers={'Authorization': 'Bearer ' + request.session['token']})

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'not_authorized'})
# endregion
