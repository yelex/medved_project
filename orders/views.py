from django.shortcuts import render
from django.http import JsonResponse
from orders.models import ProductInBasket


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    # print(request.POST)
    data = request.POST
    # print('data: ', data)
    product_id = int(data.get("product_id"))
    nmb = int(data.get("nmb"))
    is_delete = data.get("is_delete")
    # print('product_id: {}\nnmb: {}\nis_delete: {}'.format(product_id, nmb, is_delete))

    if is_delete == 'true':
        print('im here')
        # product_id - ProductInBasket id
        ProductInBasket.objects.filter(id=product_id).update(is_active=False, nmb=nmb)  # product_id - ProductInBasket id
    else:
        # product_id - ProductInBasket.product id
        print('now im here')
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
            print('after save new_product.nmb', new_product.nmb)

    # common code for 2 cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    # print('products_in_basket', products_in_basket)
    return_dict["products_in_basket_total_nmb"] = products_in_basket.count()
    return_dict["products"] = []

    for product_in_basket in products_in_basket:
        dict_product = dict()
        dict_product["id"] = product_in_basket.id
        dict_product["name"] = product_in_basket.product.name
        dict_product["price_per_item"] = product_in_basket.price_per_item
        dict_product["nmb"] = product_in_basket.nmb
        return_dict["products"].append(dict_product)

    return JsonResponse(return_dict)
    # return dict such as
    # {'products_total_nmb': 123, {'id':1, 'name': 'product1', .., 'nmb':3}, ..}




