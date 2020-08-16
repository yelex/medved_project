$(document).ready(function(){
    

    function basketUpdating(product_id, nmb, is_delete){
        var form = $('#form-common');
        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;

        var csrf_token = $('#form-common [name="csrfmiddlewaretoken"]').val();

        data.csrfmiddlewaretoken = csrf_token;
        data.is_delete = is_delete;
        console.log(data);
        var url = form.attr("action");
        
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
//                data, посылаемая на views (basket_adding)
            cache: true,
            success: function (data) {
//                data, возвращаемая из views (basket_adding)

            $('.dropdown-product').remove();
        
            if (data.products_in_basket_total_nmb!=0){
                $('#basket_total_nmb').text(" (" + data.products_in_basket_total_nmb + ")");
                $.each(data.products, function(k, v){
                $('.dropdown-menu').prepend(
                '<p class="dropdown-item dropdown-product">' + v.name + ', ' + v.nmb + ' шт. по ' + parseFloat(v.price_per_item).toFixed(0) + ' руб.'
              + '<a href="" class="delete-item" data-product_id="' + v.id + '">x</a>'
                + '</p>');
                });
                $('#total-sum').text('Итого: '+ parseFloat(data.total_sum).toFixed(0) + ' руб.');

                console.log('TOTAL SUM' + data.total_sum);
            };
            },
            error: function(){
            console.log("error")
            }
         })
    };

    $(".form-buying-product").each(function(){
                $(this).on('submit', function(e){
                    console.log('im here2');
                    e.preventDefault();
                    var nmb = $(this).find('#number').val();
                    var submit_btn = $(this).find('#submit-btn');
                    var product_id = submit_btn.data('product_id');

                    basketUpdating(product_id, nmb, is_delete=false);
                })});

    $('.basket-container').mouseover(function(){
        if ($('#basket_total_nmb').text()!='(0)'){
            showingBasket();
        }

    });

    $('.basket-container').hover(function(){
//        console.log($('#basket_total_nmb').text()!='(0)');
//        console.log($('#basket_total_nmb').text());
        if ($('#basket_total_nmb').text()!='(0)'){
                    showingBasket();
                }
    });

    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        product_id = $(this).data("product_id");
        console.log('product_id ' + product_id);
        nmb = 0;

        basketUpdating(product_id, nmb, is_delete=true);
    });
    
    function calculatingBasketAmount(){
        var total_basket_amount = 0;
        $('.total_product_in_basket_amount').each(function(){
            total_basket_amount += parseFloat($(this).text());
        });
        $('#total_basket_amount').text(total_basket_amount.toFixed(2));
    };

    $(document).on('change', '.product-in-basket-nmb', function () {
        var current_tr = $(this).closest('tr');
        var current_nmb = $(this).val();
        var current_price = parseFloat(current_tr.find('.product-price').text());
        var total_amount = parseFloat(current_nmb * current_price).toFixed(2);
        current_tr.find('.total_product_in_basket_amount').text(total_amount);
        calculatingBasketAmount();
    });

    calculatingBasketAmount();
});