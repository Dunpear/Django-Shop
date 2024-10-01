from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import View
import requests
import json
from django.urls import reverse
import requests as req
from utilities import requests
from django.conf import settings


class DetailCartView(View):
    def get(self, request):

        token = request.session.get('token')

        if token is None:
            return JsonResponse({"status": "not_authorized"})
        else:
            data = requests.send(url='invoices/get_current/', method='GET', data=None,
                                 headers={'Authorization': 'Bearer ' + token})

        if data['status'] == 403:
            return JsonResponse({"status": "not_authorized"})
        elif data['status'] == 404:
            return JsonResponse({'status': 'cart_not_found'})
        else:
            data['base_url'] = settings.BASE_URL
            return JsonResponse(data)


class DeleteItemView(View):
    def post(self, request):
        token = request.session.get('token')

        if token is None:
            return JsonResponse({"status": "not_authorized"})
        else:
            data = requests.send(url='invoices/get_current/', method='GET', data=None,
                                 headers={'Authorization': 'Bearer ' + token})

        try:
            type = request.POST['type']
            id = request.POST['id']
        except:
            return JsonResponse({'status': 'page_error_parrams'})

        if type == 'mix_item':
            data = requests.delete(url=f'invoices/remove_mixed/{id}',
                                   headers={'Authorization': 'Bearer ' + token})

            return JsonResponse({'status': 'success'})

        elif type == 'product_item':
            data = requests.delete(url=f'invoices/remove/{id}',
                                   headers={'Authorization': 'Bearer ' + token})
            return JsonResponse({'status': 'success'})


class AddProductItem(View):
    def post(self, request):
        token = request.session.get('token')

        if token is None:
            return JsonResponse({"status": "not_authorized"})
        else:
            data = requests.send(url='invoices/get_current/', method='GET', data=None,
                                 headers={'Authorization': 'Bearer ' + token})

        try:
            count = request.POST['count']
            id = request.POST['id']
        except:
            return JsonResponse({'status': 'page_error_parrams'})

        data = requests.send(url=f'invoices/create/', method="POST", data={
            "product_id": id,
            "qty": count
        }, headers={'Authorization': 'Bearer ' + token})

        try:
            if data['status'] == 200:
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': data['status'], 'message': data['message']})
        except:
            request.session.pop('token', None)
            return JsonResponse({"status": "not_authorized"})


class UpdateProductItem(View):
    def post(self, request):
        token = request.session.get('token')

        if token is None:
            return JsonResponse({"status": "not_authorized"})
        else:
            data = requests.send(url='invoices/get_current/', method='GET', data=None,
                                 headers={'Authorization': 'Bearer ' + token})

        try:
            count = request.POST['count']
            id = request.POST['id']
        except:
            return JsonResponse({'status': 'page_error_parrams'})

        data = requests.send(url=f'invoices/update/{id}', method="PUT", data={
            "qty": count
        }, headers={'Authorization': 'Bearer ' + token})

        if data['status'] == 200:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': data['status'], 'message': data['message']})


class CheckOutView(View):
    def get(self, request):
        if request.session.get('token') is None:
            return redirect('/user/login')
        else:

            user = requests.send(url='account/manage/', method='GET', data=None,
                                 headers={'Authorization': 'Bearer ' + request.session['token']})

            factor = requests.send(url='invoices/get_current/', method='GET', data=None,
                                   headers={'Authorization': 'Bearer ' + request.session['token']})
            context = {
                'user': user,
                'factor': factor,
                'base_url': settings.BASE_URL
            }

            return render(request, 'invoice/checkout.html', context)

    def post(self, request):

        if request.session.get('token') is None:
            return JsonResponse({'status':'not_authenticated'})

        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone = request.POST['phone']
            address = request.POST['address']
        except:
            return JsonResponse({'status': 'parrams_error'})

        data = requests.send(url='invoices/change_invoice_information/', method='POST', data={
            "receiver_address": address,
            "received_phone": phone,
            "received_full_name": first_name + " " + last_name
        }, headers={'Authorization': 'Bearer ' + request.session['token']})

        if data['status'] == 200:
            return JsonResponse({'status': 'success'})
        elif data['status'] == 404:
            return JsonResponse({'status': 'not_found'})
        else:
            return JsonResponse({'status': 'unknown_error'})


if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "پرداخت فاکتور کافه ورکانا"  # Required

CallbackURL = 'http://127.0.0.1:8000/invoice/verify_payment/'


# check is auth or not
def send_request(request: HttpRequest):
    token = request.session.get('token')

    if token is None:
        return redirect('/user/login')
    else:
        data = requests.send(url='invoices/get_current/', method='GET', data=None,
                             headers={'Authorization': 'Bearer ' + token})

    if data['status'] == 404:
        return redirect('/')

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": data['result']['payable_amount'],
        "Description": description,
        "Phone": data['result']['received_phone'],
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    try:
        response = req.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
            print(response['Status'])
            if response['Status'] == 100:
                return redirect(ZP_API_STARTPAY + str(response['Authority']))
            else:
                return JsonResponse({'status': 'con_er'})
                # مشکل در ارتباط با درگاه
        else:
            return JsonResponse({'status': 'con_er'})
            # موشکل در درگاه همچنان
    except req.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except req.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


# check is auth or not
def verify(authority: HttpRequest):
    token = authority.session.get('token')

    if token is None:
        return redirect('/user/login')
    else:
        data_factor = requests.send(url='invoices/get_current/', method='GET', data=None,
                                    headers={'Authorization': 'Bearer ' + token})

    if data_factor['status'] == 404:
        return redirect('/')

    try:
        res = authority.GET.get('Authority')
    except:
        return redirect('/invoice/check_out/')

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": data_factor['result']['payable_amount'],
        "Authority": res,
    }

    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = req.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            payment = requests.send('payment/', method='POST', data={
                "id": data_factor['result']['id'],
                "received_phone": data_factor['result']['received_phone'],
                "received_full_name": data_factor['result']['received_full_name'],
                "postal_code": None,
                "invoice_description": "فاکتور پرداخت شده",
                "ref_id": None,
                "authority": res
            }, headers={'Authorization': 'Bearer ' + token})

            return render(authority, 'invoice/message.html', {
                'message': 'فاکتور شما با موفقیت پرداخت شد!', 'code': data_factor['result']['tracking_code']})
            # # خرید موفق
        else:
            return render(authority, 'invoice/message.html', {'message': 'خرید شما دچار مشکل شده است!'})

    else:
        # مشکل در خرید
        return render(authority, 'invoice/message.html', {'message': 'خرید شما دچار مشکل شده است!'})

    # return response
