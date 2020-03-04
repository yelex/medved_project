$(document).ready(function(){
    var form = $('#form-buying-product');

    form.on('submit', function(e){
        e.preventDefault();
        var nmb = $('#number').val();
        var submit_btn = $('#submit-btn');
        var product_id = submit_btn.data('product_id');
        var product_name = submit_btn.data('name');
        var product_price =submit_btn.data('price');
//        console.log(nmb);
//        console.log(product_id);
//        console.log(product_name);
//        console.log(product_price);

            var data = {};
            data.product_id = product_id;
            data.nmb = nmb;
            var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
            data["csrfmiddlewaretoken"] = csrf_token;

            var url = form.attr("action");
            console.log(data)
            $.ajax({
                url: url,
                type: 'POST',
                data: data,
                cache: true,
                success: function (data) {
                console.log("OK");}}

        $('.basket-items ul').append('<li>' + product_name + ', ' + nmb + ' шт. по ' + product_price + 'руб.  '
        + '<a href="" class="delete-item">x</a>' +
        '</li>');
    });

    function showingBasket(){
        $('.basket-items').toggleClass('d-none');
    }

    $('.basket-container').click(function(e){
        e.preventDefault();
        showingBasket();
    });

    $('.basket-container').mouseover(function(){
        showingBasket();
    });

    $('.basket-container').mouseout(function(){
        showingBasket();
    });

    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        $(this).closest('li').remove();
    });
});