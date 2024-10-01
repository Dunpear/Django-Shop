def response_formatter(result, status, message):
    context = {
        'status': status,
        'message': message,
        'result': result
    }

    return context


def send_sms(self, message, mobail):
    pass


def generate_code(number: int):
    from random import randint
    number = int(number)
    return randint(10 ** (number - 1), 10 ** (number))


def cal_row_amount(qty, price):
    return int(qty * price)


def total_amount(items=None, mixed=None):
    total_price = 0
    total_discount = 0
    final_price = 0
    mix_total = 0

    if mixed:
        for mixing in mixed:
            mix_total += int(mixing.total_price)


    print(items, mixed)


    if items:
        for item in items:
            total_price += cal_row_amount(item.count, item.product.sell_price)
            total_discount += (item.product.sell_price - item.product.product_after_discount) *item.count

    final_price = total_price - total_discount

    final_price = final_price + mix_total
    return {'total_price': total_price,
            'total_discount': total_discount,
            'final_price': final_price}


base_url = 'http://localhost:8000/'
