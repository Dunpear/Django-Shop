function activa_code_tempate(value) {
    template = `
            <div class="col-xxl-6 col-xl-6 col-lg-8 col-md-10">
                <div class="reg-login-forms">
                    <h4 class="reg-login-title text-center">
                        کد تایید ارسال شده به شماره موبایل را وارد کنید!
                    </h4>
                    <div id="register-form">
                        <div class="reg-input-group">
                            <label for="fname">کد تایید</label>
                            <input type="text" id="active_code" placeholder="کد تایید را وارد کنید" >
                        </div>
                        <input type="hidden" id="mobile" name="mobile" value="${value}">
                        <div class="reg-input-group reg-submit-input d-flex align-items-center">
                            <input type="button" onclick="Activate_Account()" id="submite-btn" value="تایید">
                        </div>
                    </div>
                </div>
            </div>
        `
    return template
}


function check_mobile(number) {
    var regex = new RegExp('(0|98|0098|98)?([ ]|-|[()]){0,2}9[0-9]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}');
    var result = regex.test(number);
    if (result == true) {
        return true
    } else {
        return false
    }
}


function Register() {


    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: "json",
    });

    // region get inputs

    let f_name = $('#fname').val()
    let l_name = $('#lname').val()
    let gender = $('#gender').val()
    let password = $('#password').val()
    let re_password = $('#re_password').val()
    let mobile = $('#mobile').val()

    // endregion


    // region validate

    $("input").each(function () {
        var element = $(this);
        if (element.val() == "") {
            Swal.fire({
                title: "برای ثبت نام ابتدا مشخصات را تکمیل کنید!",
                icon: "error",
                showConfirmButton: true,
                timer: 1500
            })
            return;
        }
    });

    if (re_password != password) {
        Swal.fire({
            title: "رمز عبور و تکرار آن با یکدیگر مطابقت ندارد!",
            icon: "error",
            showConfirmButton: true,
            timer: 1500
        })
        return;
    } else if (password.length < 6 || re_password.length < 6) {
        Swal.fire({
            title: "رمز عبور نمیتواند کمتر از 6 رقم باشد!",
            icon: "error",
            showConfirmButton: true,
            timer: 1500
        })
        return;
    } else if (f_name.length < 1 || l_name.length < 1) {
        Swal.fire({
            title: "لطفا نام و نام خانوادگی را به صورت صحیح وارد کنید!",
            icon: "error",
            showConfirmButton: true,
            timer: 1500
        })
        return;
    } else if (check_mobile(mobile) == false) {

        Swal.fire({
            title: "لطفا شماره موبایل را به طور صحیح وارد کنید!",
            icon: "error",
            showConfirmButton: true,
            timer: 1500
        })
        return;
    }
    // endregion


    // send data
    else { // validated values!!
        $.post('/user/register/', { // send
            first_name: f_name,
            last_name: l_name,
            password: password,
            re_password: re_password,
            gender: gender,
            mobile: mobile
        }, function (response) {
            if (response.status == 'dosent_get_params') { // problem ( dosent send value to server )
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
            } else if (response.status == 'duplicate_user') {
                Swal.fire({
                    title: "این شماره موبایل قبلا ثبت شده است!",
                    icon: "error",
                    showConfirmButton: true,
                    timer: 1500
                })
            } else if (response.status == 'server_handling_error') {
                Swal.fire({
                    title: response.message,
                    icon: "error",
                    showConfirmButton: true,
                    timer: 1500
                })
            } else if (response.status == 'unknown_error') {
                Swal.fire({
                    title: "سرور قادر به پاسخ گویی نیست",
                    text: "لطفا این صفحه را مجددا باز کنید!",
                    icon: "error",
                    showConfirmButton: true,
                }).then(done = () => {
                    window.location.reload();
                })
                // if validate successfuly finished page change with active code
            } else if (response.status == 'success') {
                $('#temp-1554').html(activa_code_tempate(response.mobile))
            }


        });
    }
}

function Activate_Account() {

    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: "json",
    });

    let mobile = $('#mobile').val()
    let active_code = $('#active_code').val()

    if (active_code.length == 0) {
        Swal.fire({
            title: "لطفا کد تایید را وارد کنید!",
            icon: "error",
            showConfirmButton: true,
            timer: 1500
        })
    } else {
        $.post('/user/activate_account/', { // send
            active_code: active_code,
            mobile: mobile
        }, function (response) {
            if (response.status == 'success') {
                Swal.fire({
                    title: "ثبت نام با موفقیت انجام شد!",
                    icon: "success",
                    showConfirmButton: true,
                    timer: 1500
                }).then(done = () => {
                    window.location.replace('/user/login/')
                })
            } else if (response.status == 'unknown_error') {
                Swal.fire({
                    title: "صفحه دچار مشکل شده است!",
                    text: "لطفا صفحه را مجددا باز کنید!",
                    icon: "error",
                    showConfirmButton: true,
                    timer: 1500
                })
            } else if (response.status == 'not_found') {
                Swal.fire({
                    title: "شماره موبایل ثبت نشده است!",
                    text: "لطفا ابتدا ثبت نام کنید!",
                    icon: "error",
                    showConfirmButton: true,
                    timer: 1500
                })
            } else if (response.status == 'server_error') {
                Swal.fire({
                    title: "خطای اطلاعات",
                    text: response.message,
                    icon: "error",
                    showConfirmButton: true,
                })
            }
        });
    }

}