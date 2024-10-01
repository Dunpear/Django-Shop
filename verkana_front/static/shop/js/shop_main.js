const resultpriceshop = (num) => {
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


const product_by_category = (group_id, base_url) => {
    $.get(base_url + `/product/product_of_category/${group_id}`, function (response) {
        if (response.status == 200) {
            $('#show_product_category').empty();

            for (let i = 0; i < response.result.length; i++) {
                var product = response.result[i]

                if (parseInt(product.product_discount) > 0) {
                    var product_price = `
                        <div class="product-price text-center">
                            <del class="old-price">${resultpriceshop(product.sell_price)} 
                            تومان
                            </del>
                            <ins class="new-price">${resultpriceshop(product.product_after_discount)}
                                تومان
                            </ins>
                        </div>
                    `
                } else {
                    var product_price = `
                        <div class="product-price text-center">
                            <ins class="new-price">${resultpriceshop(product.product_after_discount)}
                                تومان
                            </ins>
                        </div>
                    `
                }


                var product_html = `
                    <div class="col-xxl-2 col-xl-2 col-lg-3 col-md-4 col-sm-6 col-10 mx-auto mx-sm-0">
                        <div class="product-card-l">
                            <div class="product-img">
                                <a href="/product_detail/${product.slug}" title="${product.group_image_title}">
                                    <img src="${base_url}${product.cover_picture}"
                                         alt="${product.group_image_alt}"
                                         title="${product.group_image_title}">
                                </a>
                                <div class="product-actions">
                                    <a href="/product_detail/${product.slug}"><i class="flaticon-search"></i></a>
                                    <a class="cursor-pointer" onclick="Additem(${product.id}, 1)"><i
                                            class="flaticon-shopping-cart cursor-pointer"></i></a>
                                </div>
                            </div>
                            <div class="product-body">
                                <h3 class="product-title d-flex justify-content-center">
                                    <a href="/product_detail/${product.slug}">
                                        ${product.product_name}
                                    </a>
                                </h3>
                                ${product_price}
                            </div>
                        </div>
                    </div>
                `
                $('#show_product_category').append(product_html)
            }
        } else {
            alert('err connection')
        }
    }, "json")
}


const change_order = (event, page) => {
    if(event.value){
        window.location.replace(`?orders=${event.value}&page=1`)
    }
}

const change_page = (page, event) => {
    if (event)
    {
        window.location.replace(`?orders=${event}&page=${page}`)
    }
    else{
        window.location.replace(`?page=${page}`)
    }
}