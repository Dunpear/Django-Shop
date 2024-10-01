// region detail cart

const resultprice = (num) => {
    let number = num.toString();
    if (number == "0")
        return number;

    let result = "", count = 0;
    for (var i = number.length - 1; i >= 0; i--) {
        result = number[i] + result;
        count++;
        if ((count % 3 === 0 || i === 0) && number >= 0) {
            if (i !== 0)
                result = "," + result;
            count == 0;
        }
    }

    return result;
}

function create_item(item_list, base_url) {

    let item = ''

    for (let i = 0; i < item_list.length; i++) {
        let new_item = item_list[i]
        item += `
            <li title="${new_item.product.group_image_title}" class="single-cart-product s4">
                <div class="cart-product-info d-flex align-items-center">
                    <div class="product-img">
                        <img src="${base_url}${new_item.product.cover_picture}"
                             alt="${new_item.product.group_image_alt}"
                             class="img-fluid"/>
                    </div>
                    <div class="product-info">
                        <a href="/product_detail/${new_item.product.slug}/">
                            <h5 class="product-title">${new_item.product.product_name}
                            </h5>
                        </a>
                        
                        <div style="display: flex">
                            <input type="number" min="1" max="90" step="10" value="${new_item.count}" id="count" class="input-check-style"
                             onchange="Updateitem(${new_item.id}, this.value)">
                            <p class="product-price text-center">
                                                    x <span class="p-price"> تومان 
                                                    ${resultprice(new_item.product.product_after_discount)}</span>
                            </p>
                        </div>                                                
                    </div>
                </div>
                <div class="cart-product-delete-btn">
                    <a><i class="flaticon-letter-x" onclick="delete_productitem(${new_item.id})"></i></a>
                </div>
            </li>
        `
    }


    return item

}


function create_mixed_item(mixed_items) {
    let item = ''

    for (let i = 0; i < mixed_items.length; i++) {
        let new_item = mixed_items[i]
        let name = ''
        for (let i = 0; i < new_item.mix_items.length; i++) {
            index = new_item.mix_items[i]
            if (i + 1 == new_item.mix_items.length)
                name += index.product.product_name
            else
                name += index.product.product_name + " ,"
        }
        item += `
            <li title="${name}" class="single-cart-product s4" style="border: none;
    background: linear-gradient(to right, #000000, #b5010114);" id="mix_item${new_item.id}">
                <div class="cart-product-info d-flex align-items-center">
                    <div class="product-info">
                        <a>
                            <h5 class="product-title">ترکیب ( ${name} )
                            </h5>
                        </a>
                        <p class="product-price text-center">
                        <span>قیمت نهایی ترکیب :</span>
                        <span> 
                         ${resultprice(new_item.total_price)} ریال</span> 
                        </p>
                    </div>
                </div>
                <div class="cart-product-delete-btn">
                    <a onclick="onclick(delete_mix_item(${new_item.id}))"><i class="flaticon-letter-x"></i></a>
                </div>
            </li>
        `
    }


    return item
}


function render_template(result) {

    if (result == 'not_auth') {
        let template = `
        <div class="cart-bottom">
            <div class="cart-total d-flex justify-content-between">
                <label>برای افزودن محصول به سبد خرید وارد شوید!</label>

            </div>
            <div class="cart-btns">
                <a href="/user/login/" class="cart-btn cart">ورود / ثبت نام</a>
            </div>
        </div>`
        $('.cart-count').html(0)

        return template
    } else if (result == 'cart_not_found') {
        let template = `
        <div class="cart-bottom">
            <div class="cart-total d-flex justify-content-between">
                <label>محصولی در سبد خرید وجود ندارد</label>
            </div>
            <div class="cart-btns">
                <a href="/" class="cart-btn cart">فروشگاه</a>
            </div>
        </div>`
        $('.cart-count').html(0)

        return template
    } else {

        let top_template = `
        <div class="cart-top">
            <div class="cart-close-icon">
                <i class="flaticon-letter-x" onclick="$('.cart-sidebar-wrappper').removeClass('cart-active')"></i>
            </div>
            <ul class="cart-product-grid">
                ${create_item(result.result.invoice_items, result.base_url)}
                ${create_mixed_item(result.result.mixed_item)}
            </ul>
        </div>
        `

        let bottom_template = `
        <div class="cart-bottom">
            <div class="cart-total d-flex justify-content-between">
                <label>جمع کل:</label>
                <span><span class="subPrice" id="total_cart_price">${resultprice(result.result.payable_amount)}</span> تومان</span>
            </div>
            <div class="cart-btns">
                <a href="/invoice/check_out/" class="cart-btn cart">ثبت فاکتور</a>
            </div>
        </div>`

        let template = top_template + bottom_template
        return template
    }


}


function get_detail() {
    $.get('/invoice/', function (response) {
        if (response.status == 'not_authorized') {
            let template = render_template('not_auth')
            $('#cart_body').html(template)
        } else if (response.status == 'cart_not_found') {
            let template = render_template('cart_not_found')
            $('#cart_body').html(template)
        } else {
            let template = render_template(response)
            let len = 0
            for (let i = 0; i < response.result.invoice_items.length; i++) {
                len++;
            }
            for (let i = 0; i < response.result.mixed_item.length; i++) {
                len++;
            }
            $('.cart-count').html(len)
            $('#cart_body').html(template)
        }
    })
}


// endregion


// region delete Item ( Mix Item and product Item )
function delete_productitem(pk) {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: "json",
    });

    $.post('/invoice/delete_item/', {id: pk, type: 'product_item'}, function (response) {

        if (response.status == 'page_error_parrams') {
            window.location.reload();
        } else if (response.status == 'not_authorized') {
            window.location.replace('/user/login/')
        } else if (response.status == 'success') {
            get_detail();
        }


    });

}


function delete_mix_item(pk) {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: "json",
    });

    $.post('/invoice/delete_item/', {id: pk, type: 'mix_item'}, function (response) {

        if (response.status == 'page_error_parrams') {
            window.location.reload();
        } else if (response.status == 'not_authorized') {
            window.location.replace('/user/login/')
        } else if (response.status == 'success') {
            get_detail();
        }

    });
}

// endregion


// region Add Item

function Additem(id, count, type = NaN) {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: "json",
    });

    if (type == 'input') {
        count = $('#count').val()
    }

    if (parseInt(count) < 1) {
        Swal.fire({
            title: "تعداد محصول صحیح وارد نشده است!",
            icon: "error",
            showConfirmButton: true,
            timer: 1000
        })
        return;
    } else if (count == "") {
        Swal.fire({
            title: "تعداد محصول صحیح وارد نشده است!",
            icon: "error",
            showConfirmButton: true,
            timer: 1000
        })
        return;
    }

    $.post('/invoice/add_productitem/', {id: id, count: count}, function (response) {
        if (response.status == 'success') {
            Swal.fire({
                title: "سبد خرید با موفقیت اپدیت شد!",
                icon: "success",
                showConfirmButton: true,
                timer: 1000
            })
            get_detail();
        } else if (response.status == 'page_error_parrams') {
            window.location.reload();
        } else if (response.status == 'not_authorized') {
            Swal.fire({
                title: "امکان افزودن وجود ندارد!",
                text: 'برای افزودن محصول ابتدا وارد حساب کاربری خود شوید!',
                icon: "error",
                showConfirmButton: true,
                confirmButtonText: 'باشه!',
            })
        }
    })
}

// endregion


// region Update Item
function Updateitem(id, event) {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: "json",
    });

    console.log(id, event)

    if (event < 1) {
        Swal.fire({
            title: "تعداد محصول صحیح وارد نشده است!",
            icon: "error",
            showConfirmButton: true,
            timer: 1000
        })
        event = 1;
        return;
    } else if (event == "") {
        Swal.fire({
            title: "تعداد محصول صحیح وارد نشده است!",
            icon: "error",
            showConfirmButton: true,
            timer: 1000
        })
        event = 1;
        return;
    }

    $.post('/invoice/update_productitem/', {id: id, count: event}, function (response) {
        get_detail();
    });
}

// endregion
