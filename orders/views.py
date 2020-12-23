from django.shortcuts import render
from django.http import JsonResponse
from orders.models import ProductInBasket, ProductInOrder, Order
from orders.forms import CheckoutContactForm
from django.contrib.auth.models import User
import dateutil.parser
import json
from orders.tools.telegram_handler import send_message
from datetime import datetime

def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    print(request.POST)
    data = request.POST
    print('data : ', data)
    product_id = int(data.get("product_id"))
    nmb = int(data.get("nmb"))
    is_delete = data.get("is_delete")
    # print('product_id: {}\nmb: {}\nis_delete: {}'.format(product_id, nmb, is_delete))

    if is_delete == 'true':
        # print('im here')
        # product_id - ProductInBasket id
        ProductInBasket.objects.filter(id=product_id).update(is_active=False, nmb=nmb)  # product_id - ProductInBasket id
    else:
        # product_id - ProductInBasket.product id
        # print('now im here')
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key,
                                                                     product_id=product_id,
                                                                     defaults={"nmb": nmb, "is_active": True})

        if not created:
            new_product.is_active = True
            # print('not created')
            # print('int(new_product.nmb):', int(new_product.nmb))
            # print('int(nmb):', int(nmb))
            # print('new_product.is_active', new_product.is_active)
            new_product.nmb = int(new_product.nmb) + int(nmb)
            new_product.save(force_update=True)
            # print('after save new_product.nmb', new_product.nmb)

    # common code for 2 cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    # print('products_in_basket', products_in_basket)
    return_dict["products_in_basket_total_nmb"] = products_in_basket.count()
    return_dict["products"] = []
    total_cart_sum = 0

    for product_in_basket in products_in_basket:
        dict_product = dict()
        dict_product["id"] = product_in_basket.id
        dict_product["name"] = product_in_basket.product.name
        dict_product["price_per_item"] = product_in_basket.price_per_item
        dict_product["nmb"] = product_in_basket.nmb
        if product_in_basket.is_active:
            total_cart_sum += product_in_basket.price_per_item * product_in_basket.nmb
        return_dict["products"].append(dict_product)
    return_dict["total_sum"] = total_cart_sum
    # print('return_dict', return_dict)
    return JsonResponse(return_dict)
    # return dict such as
    # {'products_total_nmb': 123, {'id':1, 'name': 'product1', .., 'nmb':3}, ..}


def checkout(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print('im in checkout')
        print(request.POST)
        if form.is_valid():
            data = request.POST

            name = data["name"]
            phone = data["phone"]
            delivery_date = dateutil.parser.parse(data["delivery_date"])
            note = data["note"]
            is_delivery = json.loads(data["is_delivery"])
            is_another_person = data.get('is_another_person', False)
            if is_another_person != False:
                is_another_person = True
            name_other = data["name_other"]
            phone_other = data["phone_other"]
            delivery_address = data["delivery_address"]
            comments = data["comments"]
            print('is_delivery:', is_delivery, '\nis_another_person:', is_another_person)
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})
        
            order = Order.objects.create(user=user, customer_phone=phone, customer_name=name, 
                                        delivery_date=delivery_date, note=note, is_delivery=is_delivery, 
                                        is_another_person=is_another_person, recipient_name = name_other, recipient_phone=phone_other, 
                                        delivery_address=delivery_address, comments=comments, status_id=1)
        
            for name, value in data.items():
                if name.startswith('product_in_basket'):
                    product_in_basket_id = name.split('_')[-1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
        
                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)
                    ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price=product_in_basket.total_price,
                                                  order=order)
            if is_delivery:
                pickup_method = 'Доставка'
            else:
                pickup_method = 'Самовывоз'
            
            if is_another_person:
                pickup_person = 'Другой человек'
            else:
                pickup_person = 'Сам заказчик'
            
            

            all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

            positions_description = ''
            for item in all_products_in_order:
                positions_description += f"""\n{item.product.name} - {item.nmb} шт. по {item.price_per_item} руб. =  {item.total_price} руб."""

            send_message(f"""Новый заказ!\nИмя заказчика: {data["name"]}
            \nСумма заказа: {order.total_order_price} руб.
            \nПозиции: {positions_description}
            \nТелефон заказчика: {phone}
            \nСпособ получения: {pickup_method}
            \nПолучатель: {pickup_person}
            \n{"Имя получателя: %".format(name_other) if is_another_person else ""}
            \n{"Номер телефона получателя: %".format(phone_other) if is_another_person else ""}
            \n{"Адрес доставки: %".format(delivery_address) if is_delivery else ""}
            \nДата получения: {delivery_date}
            \n{"Комментарий: %".format(comments) if comments!="" else ""}""")

            return render(request, 'orders/success_checkout.html', context=locals())
        # return render(request, 'orders/checkout.html', context=locals())
        else:
            print('Form is not valid')
            return render(request, 'orders/checkout.html', context=locals())

    else:
        return render(request, 'orders/checkout.html', context=locals())


