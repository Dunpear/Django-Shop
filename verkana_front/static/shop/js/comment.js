function submitcomment(id) {

    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: "json",
    });


    let comment = $('#review-area').val()

    if (comment == "") {
        Swal.fire({
            title: "برای ثبت نظر لطفا ابتدا نظر خود را بنویسید!",
            icon: "error",
            showConfirmButton: true,
            timer: 2000
        })
        return;
    }

    $.post('/comment/', {product_id: id, comment: comment}, function (response) {
        if (response.status == 'success') {
            Swal.fire({
                title: "نظر شما با موفقیت ثبت شد ، با تشکر!",
                icon: "success",
                showConfirmButton: true,
                timer: 2000
            }).then(
                $('#review-area').val("")
            )
        } else if (response.status == 'parrams_error') {
            window.location.reload();
        } else if (response.status == 'not_authorized') {
            Swal.fire({
                title: "برای ثبت نظر ابتدا وارد حساب خود شوید!",
                icon: "error",
                showConfirmButton: true,
                timer: 2000
            })
        }
    })

}