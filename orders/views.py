from django.shortcuts import render
from django.http import JsonResponse
from orders.models import ProductInBasket, ProductInOrder, Order
from orders.forms import CheckoutContactForm
from django.contrib.auth.models import User


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    # print(request.POST)
    data = request.POST
    print('data : ', data)
    product_id = int(data.get("product_id"))
    nmb = int(data.get("nmb"))
    is_delete = data.get("is_delete")
    # print('product_id: {}\nnmb: {}\nis_delete: {}'.format(product_id, nmb, is_delete))

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
        print('product_in_basket.is_active', product_in_basket.is_active)
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
        if form.is_valid():
            data = request.POST
            name = data.get("name", "some_name")
            phone = data["phone"]
            # print('yes')
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            order = Order.objects.create(user=user, customer_phone=phone, customer_name=name, status_id=1)
            
            for name, value in data.items():
                if name.startswith('product_in_basket'):
                    product_in_basket_id = name.split('_')[-1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    print(type(value))
                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)
                    ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price=product_in_basket.total_price,
                                                  order=order)

            return render(request, 'orders/success_checkout.html', context=locals())
        else:
            print('Form is not valid')
            return render(request, 'orders/checkout.html', context=locals())

    else:
        return render(request, 'orders/checkout.html', context=locals())

