$(function() {
    var rangeSlider = $(".price-range"),
    minamount = $("#minamount"),
    maxamount = $("#maxamount"),
    minPrice = rangeSlider.data('min'),
    maxPrice = rangeSlider.data('max');
    $(".price-range").slider({
        range: true,
        min: minPrice,
        max: maxPrice,
        values: [minPrice, maxPrice],
        slide: function(event, ui) {
            $("#minamount").val(ui.values[0]);
            $("#maxamount").val(ui.values[1]);
            fetchProducts(ui.values[0], ui.values[1]);
        }
    });
    
function fetchProducts(minPrice, maxPrice) {
    // Send AJAX request to fetch products based on price range
    $.ajax({
        url: "product_price_filter/",
        data: {
            min_price: minPrice,
            max_price: maxPrice
        },
        success: function(response) {
            // Replace the product list with the fetched products
            var filter = $('#product_container'),
            product_count = $('#product_count')
            d = `<span id="product_count">${response.product_count}</span> `
            product_count.replaceWith(d)
            filter.html(response.data)
            
        }
    });
}
});


$(document).ready(function(){
    var csrftoken = getCookie('csrftoken');
    $('.cart').click(function(){
        var productId = $(this).data("product-id");
        $.ajax({
            url: "addToCart/",
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken  // Include the CSRF token in the headers
            },
            data: { productId: productId },
            success: function(response) {
                // Handle success response
                console.log("Order line created successfully.", response.message);
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.error("Error creating order line:", error);
            }
        });
    })
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
  
  });