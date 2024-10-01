function change_information() {

    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: "json",
    });

    let f_name = $('#fname').val()
    let l_name = $('#lname').val()
    let gender = $('#gender').val()


    if (f_name == "" || l_name == "") {
        Swal.fire({
            title: "برای تغییر اطلاعات لطفا مشخصات را وارد کنید!",
            icon: "error",
            showConfirmButton: true,
            timer: 4000
        })
    }


    $.post('/user/profile/', {f_name: f_name, l_name: l_name, gender: gender}, function (response) {
        if (response.status == 200) {
            icon = 'success'
        } else {
            icon = 'error'
        }
        Swal.fire({
            title: response.message,
            icon: icon,
            showConfirmButton: true,
            timer: 1500
        })
        $("#submite-btn").prop('disabled', true);
    })
}

function change_password() {

    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: "json",
    });

    let old_password = $('#old_password').val()
    let new_password = $('#new_password').val()

    if (old_password == "" || new_password == "") {
        Swal.fire({
            title: "فیلد های پسورد خالی است!",
            icon: "error",
            showConfirmButton: true,
            timer: 4000
        })
        return;
    } else if (new_password.length < 6) {
        Swal.fire({
            title: "رمز عبور جدید باید بیشتر از 6 رقم باشد!",
            icon: "error",
            showConfirmButton: true,
            timer: 4000
        })
        return;
    } else if (new_password == old_password) {
        Swal.fire({
            title: "رمز عبور جدید نمیتواند با رمز عبور فعلی یکسان باشد!",
            icon: "error",
            showConfirmButton: true,
            timer: 4000
        })
        return
    }

    $.post('/user/change_password/', {new_password: new_password, old_password: old_password}, function (response) {
        if (response.status == 'equl_passwod') {
            Swal.fire({
                title: "رمز عبور جدید نمیتواند با رمز عبور فعلی یکسان باشد!",
                icon: "error",
                showConfirmButton: true,
                timer: 4000
            })
            return;
        }
        else if(response.status == 'invalid_params'){
            Swal.fire({
                title: "فیلد های پسورد خالی است!",
                icon: "error",
                showConfirmButton: true,
                timer: 4000
            })
            return
        }

        if (response.status == 400){
            var icon = 'error'
        }
        else{
            var icon = 'success'
        }

        Swal.fire({
            title: response.message,
            icon: icon,
            showConfirmButton: true,
            timer: 4000
        })
    })


}