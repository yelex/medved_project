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

   $('#note').change(function() {
        if(this.checked) {
            $('.note').removeClass('d-none');
        }
        else {
            $('.note').addClass('d-none');
        }
        });

   $('#otherPerson').change(function() {
        if(this.checked) {
              $(this).val('true');
              $('.name_other').removeClass('d-none');
              $('.phone_other').removeClass('d-none');
        }
        else {
              $(this).val('false');
              $('.name_other').addClass('d-none');
              $('.phone_other').addClass('d-none');
        }
        });

//  FIXME самовывоз
//   $('#delivery2').change(function() {
//        if(this.checked) {
//              $(this).val('true');
//              $('.name_other').removeClass('d-none');
//              $('.phone_other').removeClass('d-none');
//        }
//        else {
//              $(this).val('false');
//              $('.name_other').addClass('d-none');
//              $('.phone_other').addClass('d-none');
//        }
//        });

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
    $.datepicker.regional['ru'] = {
        closeText: 'Закрыть',
        prevText: 'Предыдущий',
        nextText: 'Следующий',
        currentText: 'Сегодня',
        monthNames: ['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'],
        monthNamesShort: ['Янв','Фев','Мар','Апр','Май','Июн','Июл','Авг','Сен','Окт','Ноя','Дек'],
        dayNames: ['воскресенье','понедельник','вторник','среда','четверг','пятница','суббота'],
        dayNamesShort: ['вск','пнд','втр','срд','чтв','птн','сбт'],
        dayNamesMin: ['Вс','Пн','Вт','Ср','Чт','Пт','Сб'],
        weekHeader: 'Не',
        dateFormat: 'dd.mm.yy',
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: ''
    };
    $.datepicker.setDefaults($.datepicker.regional['ru']);
    
    $("#delivery_date").datepicker({
        onSelect: function(dateText){
                    console.log("Selected date: " + dateText + "; input's current value: " + this.value);
                    calculateTimeDelivery(dateText);
                },
		minDate: 0
	});

	function calculateTimeDelivery(dateText){
	    var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();
        var hrs = String(today.getHours());
        console.log(hrs);
        today = dd + '.' + mm + '.' + yyyy;
        if (today==dateText){
            minTime = parseInt(hrs);
        } else {
            minTime = '0';
        };
        var i;
        $('#delivery_time').empty();
        for (i = minTime; i < 24; i++) {
        $('#delivery_time').append(
            '<option> C ' + String(i).padStart(2, '0') + ':00 до ' + String(i+1).padStart(2, '0') + ':00 </option>'
           )};

        console.log(minTime);

        };
    })


