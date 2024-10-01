function login() {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: "json",
    });

    username = $('#fname').val()
    password = $('#password').val()


    if (username.length != 11 || password == "") {
        Swal.fire({
            title: "اطلاعات به درستی وارد نشده است!",
            icon: "error",
            showConfirmButton: true,
            timer: 1500
        })
        return;
    } else {
        $.post('/user/login/', {username: username, password: password}, function (response) {
            if (response.status == 'invalid_params') {
                Swal.fire({
                    title: "اطلاعات به درستی وارد نشده است!",
                    icon: "error",
                    showConfirmButton: true,
                    timer: 1500
                })
            } else if (response.status == 'not_found') {
                Swal.fire({
                    title: "کاربری با این مشخصات یافت نشد!",
                    icon: "error",
                    showConfirmButton: true,
                    timer: 1500
                })

            } else if (response.status == 'success') {
                window.location.replace('/')
            } else if (response.status == 'error_not_logged_in') {
                Swal.fire({
                    title: `${response.message}`,
                    icon: "error",
                    showConfirmButton: true,
                    timer: 1500
                })
            }
        })
    }
}


