function check_mobile(number) {
    var regex = new RegExp('(0|98|0098|98)?([ ]|-|[()]){0,2}9[0-9]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}');
    var result = regex.test(number);
    if (result == true) {
        return true
    } else {
        return false
    }
}

function Recovery() {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: "json",
    });

    let mobile = $('#mobile').val()

    if (check_mobile(mobile) == false) {
        Swal.fire({
            title: "شماره موبایل صحیح وارد نشده است!",
            icon: "error",
            showConfirmButton: true,
            timer: 1500
        })
        return;
    }
    if (mobile == "") {
        Swal.fire({
            title: "شماره موبایل وارد نشده است!",
            icon: "error",
            showConfirmButton: true,
            timer: 1500
        })
        return;
    }

    $.post('/user/forget_password/', {mobile: mobile}, function (response) {
        if (response.status == 'page_error_params') {
            Swal.fire({
                title: "خطای دریافت اطلاعات",
                text: "لطفا این صفحه را مجددا باز کنید!",
                icon: "error",
                showConfirmButton: true,
            }).then(done = () => {
                window.location.reload();
            })
        } else if (response.status == 'invalid_data') {
            Swal.fire({
                title: "اطلاعات به درستی وارد نشده است!",
                icon: "error",
                showConfirmButton: true,
                timer: 1500
            })
        }
        else if(response.status == 'success'){
            Swal.fire({
                title: "رمز عبور جدید برای شما ارسال شد",
                text: 'یک پیام حاوی رمز عبور جدید برای شما ارسال شد ' +
                    ' پس از ورود میتوانید رمز عبور را به دلخواه تغییر دهید!',
                icon: "success",
                showConfirmButton: true,
            }).then(done = () => {
                window.location.replace('/user/login/');
            })
        }


    })

}