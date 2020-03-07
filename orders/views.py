from django.shortcuts import render
from django.http import JsonResponse
from orders.models import ProductInBasket


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    print(request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = bool(data.get("is_delete"))

    if is_delete:
        ProductInBasket.objects.filter(session_key=session_key, product_id=product_id).update(is_active=False) #TODO 1.8.4 на 8:23
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key,
                                                                     product_id=product_id, defaults={"nmb": nmb})
        if not created:
            new_product.nmb = int(new_product.nmb) + int(nmb)
            new_product.save(force_update=True)

    # common code for 2 cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    return_dict["products_total_nmb"] = products_in_basket.count()
    return_dict["products"] = []

    for product_in_basket in products_in_basket:
        dict_product = dict()
        dict_product["id"] = product_in_basket.product.id
        dict_product["name"] = product_in_basket.product.name
        dict_product["price_per_item"] = product_in_basket.price_per_item
        dict_product["nmb"] = product_in_basket.nmb
        return_dict["products"].append(dict_product)

    return JsonResponse(return_dict)



