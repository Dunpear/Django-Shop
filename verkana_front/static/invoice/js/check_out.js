function check_out() {

    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: "json",
    });

    let address = $('#address').val()
    let first_name = $('#first-name').val()
    let last_name = $('#last-name').val()
    let phone = $('#phone').val()


    if (address == "" || first_name == "" || last_name == "" || phone == "") {
        Swal.fire({
            title: "لطفا مقادیر را برای ثبت سفارش پر کنید!",
            icon: "error",
            showConfirmButton: true,
            timer: 1800
        })
        return;
    } else {
        $.post('/invoice/check_out/', {
            first_name: first_name,
            last_name: last_name,
            phone: phone,
            address: address
        }, function (response) {
            if (response.status == 'parrams_error') {
                Swal.fire({
                    title: "لطفا مقادیر را برای ثبت سفارش پر کنید!",
                    icon: "error",
                    showConfirmButton: true,
                    timer: 1800
                }).then(x = () => {
                    window.location.reload();
                })
            } else if (response.status == 'not_authenticated') {
                window.location.replace('/user/login/')
            } else if (response.status == 'not_found') {
                Swal.fire({
                    title: "این سبد خرید قابل پرداخت نمیباشد!",
                    icon: "error",
                    showConfirmButton: true,
                    timer: 1800
                })
            } else if (response.status == 'success') {
                window.location.replace('/invoice/payment/')
            }

        })

    }


}