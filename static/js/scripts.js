$(document).ready(function(){
    var form = $('#form-buying-product');

    function basketUpdating(product_id, nmb, is_delete){

        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;
        var csrf_token = $('#form-buying-product [name="csrfmiddlewaretoken"]').val();
        data.csrfmiddlewaretoken = csrf_token;
        data.is_delete = is_delete

        var url = form.attr("action");
        console.log(data);
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
//                data, посылаемая на views (basket_adding)
            cache: true,
            success: function (data) {
//                data, возвращаемая из views (basket_adding)
            console.log("OK");
//            console.log(data.products_in_basket_total_nmb);
            $('#basket_total_nmb').text("(" + data.products_in_basket_total_nmb + ")");
            $('.basket-items ul').empty();
            if (data.products_in_basket_total_nmb!=0){
//                $('#basket_total_nmb').text("(" + data.products_in_basket_total_nmb + ")");
                console.log(data.products);
//                $('.basket-items ul').empty();
                $.each(data.products, function(k, v){
                $('.basket-items ul').append('<li>' + v.name + ', ' + v.nmb + ' шт. по ' + v.price_per_item + 'руб.  '
              + '<a href="" class="delete-item" data-product_id="' + v.id + '">x</a>'
                + '</li>');
                })
            };

            $('.basket-items').addClass('d-none');

            },
            error: function(){
            console.log("error")
            }
         })
    };

    form.on('submit', function(e){
        e.preventDefault();
        var nmb = $('#number').val();
        var submit_btn = $('#submit-btn');
        var product_id = submit_btn.data('product_id');
//        var product_name = submit_btn.data('name');
//        var product_price =submit_btn.data('price');
        console.log(nmb);
//        console.log(product_id);
//        console.log(product_name);
//        console.log(product_price);
        basketUpdating(product_id, nmb, is_delete=false);

    });


    function showingBasket(){
        $('.basket-items').removeClass('d-none');
    }

//    $('.basket-container').click(function(e){
//        e.preventDefault();
//        showingBasket();
//    });

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

    $('.basket-container').mouseout(function(){
//        console.log($('#basket_total_nmb').text());
        if ($('#basket_total_nmb').text()!='(0)'){
        $('.basket-items').addClass('d-none');
        }
    });

    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        product_id = $(this).data("product_id");
        console.log('product_id ' + product_id);
        nmb = 0;

        basketUpdating(product_id, nmb, is_delete=true);
    });
});