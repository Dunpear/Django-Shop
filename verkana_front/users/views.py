from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
import requests
import json
from django.urls import reverse
from django.views.generic import DetailView
from utilities import requests
from django.conf import settings
from django.core.paginator import Paginator
from .models import User


class LgoinView(View):
    def get(self, request):

        return render(request, 'users/login.html')

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']

        if len(username) != 11:
            return JsonResponse({'status': 'invalid_params'})

        data = requests.send('account/login/', 'POST', {'user_phone': username, 'password': password})
        access = data.get('access')
        if access:
            new_user = User.objects.create(username=username, token=access, is_expired=False)
            request.session['token'] = access
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'not_found'})


class LogoutView(View):
    def get(self, request):
        request.session.pop('token', None)
        return redirect('/')


class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):

        # get params

        try:
            mobile = request.POST['mobile']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST['password']
            re_password = request.POST['re_password']
            gender = request.POST['gender']
        except:
            return JsonResponse({'status': 'dosent_get_params'})

        # validate
        if len(mobile) < 11:
            return JsonResponse({'status': 'invalid_data'})
        elif len(first_name) < 1 or len(last_name) < 1:
            return JsonResponse({'status': 'invalid_data'})
        elif password != re_password:
            return JsonResponse({'status': 'invalid_data'})

        context = {
            "user_phone": mobile,
            "name": first_name,
            "family": last_name,
            "gender": gender,
            "password": password
        }

        data = requests.send('account/register/', 'POST', context)

        if data['status'] == 400:  # 400 error handling
            return JsonResponse({'status': 'server_handling_error', 'message': data['message']})
        elif data['status'] == 200:  # if process successfuly
            return JsonResponse({'status': 'success', 'mobile': mobile})
        else:  # unknown_error
            return JsonResponse({'status': 'unknown_error'})


class ActivateAccountView(View):
    def post(self, request):
        try:
            mobile = request.POST['mobile']
            active_code = request.POST['active_code']
        except:
            return JsonResponse({'status': 'page_error_params'})

        context = {
            "active_code": active_code,
            "user_phone": mobile
        }

        data = requests.send('account/active/', 'POST', context)
        if data['status'] == 200:
            return JsonResponse({'status': 'success'})
        elif data['status'] == 400:
            return JsonResponse({'status': 'server_error', 'message': data['message']})
        elif data['status'] == 404:
            return JsonResponse({'status': 'not_found'})
        else:
            return JsonResponse({'status': 'unknown_error'})


class RecoveryPasswordView(View):
    def get(self, request):
        return render(request, 'users/forget_password.html')

    def post(self, request):

        try:
            mobile = request.POST['mobile']
        except:
            return JsonResponse({'status': 'page_error_params'})

        if len(mobile) != 11:
            return JsonResponse({'status': 'invalid_data'})

        return JsonResponse({'status': 'success'})


# region profile

class ProfileView(View):
    def get(self, request):
        if request.session.get('token'):
            data = requests.send(url='account/manage/', method='GET', data=None,
                                 headers={'Authorization': 'Bearer ' + request.session['token']})
            if data.get('code') == 'token_not_valid':
                request.session['token'] = None
                return redirect(reverse('user:login'))
            else:
                data['base_url'] = settings.BASE_URL
                return render(request, 'users/profile.html', data)
        else:
            return redirect(reverse('user:login'))

    def post(self, request):
        if request.session['token']:

            f_name = request.POST['f_name']
            l_name = request.POST['l_name']
            gender = request.POST['gender']

            if gender == 'None':
                data = requests.send(url='account/manage/', method="PUT", data={
                    "name": f_name,
                    "family": l_name,
                }, headers={'Authorization': f'Bearer {request.session["token"]}'})
            else:
                data = requests.send(url='account/manage/', method="PUT", data={
                    "name": f_name,
                    "family": l_name,
                    "gender": gender
                }, headers={'Authorization': f'Bearer {request.session["token"]}'})

            return JsonResponse(data)

        else:
            return redirect(reverse('/user/login/'))


class ChangePasswordView(View):
    def post(self, request):
        if request.session.get('token'):

            old_password = request.POST['old_password']
            new_password = request.POST['new_password']

            if old_password == new_password:
                return JsonResponse({'status': 'equl_passwod'})
            elif new_password == "" or old_password == "":
                return JsonResponse({'status': 'invalid_params'})

            data = requests.send(url='account/change_password/', method="POST", data={
                "old_password": old_password,
                "new_password": new_password
            }, headers={'Authorization': f'Bearer {request.session["token"]}'})

            return JsonResponse(data)


        else:
            return redirect(reverse('user:login'))


class UserOrders(View):
    def get(self, request):
        if request.session.get('token') is None:
            return redirect('/user/login/')

        data = requests.send(url='invoices/get_invoice_list/', method="GET", data=None,
                             headers={'Authorization': f'Bearer {request.session["token"]}'})

        return render(request, 'users/order.html', {'factors': data['result']})



class UserOrderDetail(View):
    def get(self, request, factor_id:int):
        if request.session.get('token') is None:
            return redirect('/user/login/')

        data = requests.send(url=f'invoices/get_invoice/{factor_id}', method="GET", data=None,
                             headers={'Authorization': f'Bearer {request.session["token"]}'})

        if data['status'] == 404:
            return redirect('/user/orders/')
        else:
            return render(request, 'users/order_detail.html', {'factor': data['result'], 'base_url':settings.BASE_URL})

# endregion
