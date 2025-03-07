(function ($) {

    const month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    $(".review-form").submit(function (e) {
        e.preventDefault();
        let date = new Date();
        let time = date.getDay() + " " + month_names[date.getUTCMonth()] + ", " + date.getFullYear();


        $.ajax({
            data: $(this).serialize(),

            method: $(this).attr("method"),
            url: $(this).attr("action"),
            dataType: 'json',

            success: function (response) {
                console.log('Comment saved');
                console.log(response.context);


                if (response.bool == true) {
                    $("#review-rsp").html("Review Added Successfully")
                    $(".hide-review").hide();
                    $(".add-review").hide();

                    let _html = '<div class="media mb-4">'
                    _html += '<img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIAJQAqAMBIgACEQEDEQH/xAAbAAEAAgMBAQAAAAAAAAAAAAAABQYCAwQBB//EADgQAAICAQEEBgcGBwEAAAAAAAABAgMEEQUSITEGIkFRYXETFDJCkcHhUmJygaHRFSMzNEOSsVT/xAAUAQEAAAAAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8A+4gAAAAAAAAanDl7UxMXVTs3pr3YcWB3Arl3SKctfQURiu+b1/Q5LNtZ0+Vqh+GKAtwKb/Ftof8Aql/qv2NkNtZ8Odql+KKAtwK5R0isXC+iMl2uD0f6krh7VxMrSMbFCb9yfBgdwGoAAAAAAAAAAAAAABz5mZTh1Oy+Wncu2T8DXtLPrwad+XGb9iHeypZORblWu26W9J/BeCA68/a+Rltxg3XV9mL4vzZHHoAAAAAAB4egCRwNr5GJpGbdtX2ZPivJllw8ynMr36Za98e1FJNuNkW4tqtpluyXwa7gLyDj2bnwzqN6PCceE49zOwAAAAAAAAAasm+GNRO6x6RitTaVrpHmekvjiwfVr4y8Zd35ARmZk2Zd8rbO32V9ldxpAAAAAAk20ktW+SXaSGNsfJuW9PdqX3+fwAjwTP8AAXp/dLX8H1ObI2NlUrWG7avuc/gBHgPg9Gmn3MAAABuw8mzEyI21vlwa713Fzxb4ZNELa/ZkvgUYmejmZ6O94s31bOMdeyQFlAAAAAAABryLY0U2WzfVhFyZRrJytnKyftTe8y09IrXXs6UV/kko/P5FVAAAAEm2tFq+SB37FoV2apS4xrW9p3vsAldl7OjjQVliTva5/Z8ESAAAAAR+1NnRya3ZVHS5Lhp73gVtrRtPmXQrW26FTnScV1bFvLz7QOAAADKucq7I2Q9qLTRiAL1j2xvphbD2ZxTRsIvo7a7NmpP3JOPz+ZKAAAAAAEF0pk/R48exyk/gvqV4n+lS4Y3nL5EAAAAAl+jmnpb127qIc7dkX+gzI6vSM1uv5fqBaAa956PXmN56LmBsGphq9GuOp49U+0DKMlLXVEL0j/q0d+6+H5kvxS4eZXNsZHp82Wj1jWtxfP8AUDjB5qegAABYeisn6PJj2KUX8V9CdIDoouGV5x+ZPgAAAAAEP0nr3sKE9PYsXwaKyXPadPrGDdWlq3HVea4lLT1A9AAAeXMACwbJ2lG6EaL5btq4Rb976kp8ip1YWTfDeqom4rjry18jdVtHNxP5UpN6e5auQFm4aaggf47du/0K9fNnPdtLMy+pCTSfu1ICS2rtONEXTRJStfBtco/Ur50XYOVTBSsomo6a689PPuOcDw9AAAACzdGK93Csm+c7P0SX1Jg5NmUer4NNTXFR1fmzrAAAAAABTtr4vqudOKXUn14/mXEj9s4PruK91L0sOMPHwAqIDWj00a8zKquVtkK4LWUnokB7RTZfYq6YuUmWHB2VTjpTt0tt72uqvJG/Aw4YdO6uM3xlLvf7HSAMZ112LSyEZL7y1MgBz+o4mv8AbU/6I3V1wqWlUIwX3VoZAB2EfnbJpyNZUpVW969l+aJAAU6+iyix12xcZIwLXn4UMylxfVmuMJdz/Yq1tc6bJV2R3ZRejQGJ27HxfWs2EWtYR60vJfU4uPBJa68EW7Y+C8PFW+v5s+M/DwAkAAAAAAAAAABAbd2W25ZWNHV87IL/AKjDo/i7sJZUkt6XCHgvqWI1SqSWkEl4JcANQD4cwAAAAAAAAAIfb+IpVrJgutHhN967CYXHkbY1Ra0sipeDXACE2Fstpxy8mOj/AMcH2eLLAAAAAAAAAAAAAAAAYyipLijVKprlxN4A5WtOYOoxcIvsA5wdHo49wUYrsA0JN8jONTfPgbgBjGKjyRkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAf/2Q==" alt="Image" class="img-fluid mr-3 mt-1" style="width: 45px;">'

                    _html += '<div class="media-body">'
                    _html += '<h6>' + response.context.user + '<small> - <i>' + time + '</i></small></h6>'

                    _html += '<div class="text-primary mb-2">'
                    for (let i = 1; i <= response.context.rating; i++) {
                        _html += '<i class="fas fa-star text-warning"></i>'
                    }
                    _html += '</div>'

                    _html += '<p>' + response.context.review + '</p>'
                    _html += '</div>'

                    _html += '</div>'
                    console.log(_html);
                    $(".comment-list").prepend(_html)
                }

            }
        })
    })



    // Add to Cart Function
    $("#add-to-cart-btn").on("click", function () {
        let quantity = $("#product-quantity").val();
        let product_image = $(".product-image").val();
        let product_title = $(".product-title").val();
        let product_id = $(".product-id").val();
        let product_price = $(".product-price").text();
        let this_val = $(this);

        console.log("Quantity:", quantity);
        console.log("Product Title:", product_title);
        console.log("Product ID:", product_id);
        console.log("Price:", product_price);
        console.log("Image:", product_image);
        console.log("Current Element:", this_val);
        console.log("Olayinka");

        // Function to get the CSRF token from cookies
        function getCSRFToken() {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.startsWith('csrftoken=')) {
                        cookieValue = decodeURIComponent(cookie.substring('csrftoken='.length));
                        break;
                    }
                }
            }
            console.log("CSRF Token from cookies:", cookieValue); // For debugging
            return cookieValue;
        }


        // Send AJAX request
        $.ajax({
            url: '/add-to-cart/',
            type: "POST",
            data: {
                "id": product_id,
                "quantity": quantity,
                "title": product_title,
                "price": product_price,
                "image": product_image
            },
            dataType: "json",
            beforeSend: function (xhr) {
                // Set CSRF Token in the request header
                xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
                console.log("Adding Product to Cart...");
                console.log("CSRF Token:", getCSRFToken());
            },
            success: function (response) {
                // Change button text to indicate success
                this_val.html("Item added to cart");
                console.log("Added Product to Cart");

                // Update the cart items count
                $(".cart-items-count").text(response.totalcartItems);
            },
            error: function (xhr, status, error) {
                // Handle errors
                console.error("Error:", error);
                alert("An error occurred while adding the product to the cart.");
            }
        });
    });








    $(document).on('click', '.add-to-cart-btn', function () {
        let productId = $(this).data('index');
        let productTitle = $('#product-title-' + productId).val();
        let productPrice = $('#product-price-' + productId).val();
        let productImage = $('#product-image-' + productId).val();
        let productQuantity = $('#product-quantity-' + productId).val();
        let this_val = $(this);

        // Now, use these variables to add the product to the cart
        console.log('Product ID:', productId);
        console.log('Product Title:', productTitle);
        console.log('Product Price:', productPrice);
        console.log('Product Image:', productImage);
        console.log('Product Quantity:', productQuantity);

        // CSRF token handling
        function getCSRFToken() {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.startsWith('csrftoken=')) {
                        cookieValue = decodeURIComponent(cookie.substring('csrftoken='.length));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        // Send AJAX request
        $.ajax({
            url: '/add-to-cart/',
            type: "POST",
            data: {
                "id": productId,
                "quantity": productQuantity,
                "title": productTitle,
                "price": productPrice,
                "image": productImage
            },
            dataType: "json",
            beforeSend: function (xhr) {
                let csrfToken = getCSRFToken();
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                console.log("Setting CSRF Token:", csrfToken);  // Debug CSRF token
            },
            success: function (response) {
                // Change button text to indicate success
                this_val.html("Item added to cart");
                console.log("Added Product to Cart");

                // Update the cart items count
                $(".cart-items-count").text(response.totalcartItems);
            },
            error: function (xhr, status, error) {
                // Handle errors
                console.error("Error:", error);
                alert("An error occurred while adding the product to the cart.");
            }
        });
    });



    $(document).ready(function () {
        // Event listener for the update button
        $(document).on('click', '.update-product', function (event) {
            console.log("Update button clicked");
            event.preventDefault();

            let product_id = $(this).attr("data-product");
            let this_val = $(this);
            let product_quantity = $(".product-quantity[data-product='" + product_id + "']").val();

            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            $.ajax({
                url: "/update-cart/",  // Ensure this matches the path in your urls.py
                data: {
                    'id': product_id,
                    'quantity': product_quantity
                },
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')  // Make sure you're sending the CSRF token
                },

                dataType: "json",
                beforeSend: function () {
                    this_val.hide();
                },
                success: function (response) {
                    this_val.show();
                    if (response.data) {
                        // Update cart list if data exists
                        $('#cart-list').html(response.data);
                    }
                    $(".cart-items-count").text(response.totalcartItems);
                },
                error: function (xhr, status, error) {
                    console.error("Error updating cart: ", error);
                }
            });
        });

        // Event listener for the delete button
        $(document).on('click', '.delete-product', function (event) {
            console.log("Delete button clicked");
            event.preventDefault();

            let product_id = $(this).attr("data-product");
            let this_val = $(this);

            console.log("Product-Id: " + product_id);


            $.ajax({
                url: "/delete-from-cart/",
                data: {
                    'id': product_id
                },
                dataType: "json",
                beforeSend: function () {
                    this_val.hide();  // Hide the delete button while processing
                },
                success: function (response) {
                    this_val.show();  // Show the button again after request is processed

                    // Ensure the response contains the updated HTML, item count, and total amount
                    if (response.data) {
                        // Update the cart list with the new HTML
                        $('#cart-list').html(response.data);

                        // Update the total number of items in the cart
                        $(".cart-items-count").text(response.totalcartItems);

                        // Update the total amount if you're displaying it
                        $(".cart-total-amount").text('₦' + response.cart_total_amount.toFixed(2));
                    } else {
                        alert('Error: ' + response.error);  // Handle errors (e.g., product not found)
                    }
                },
                error: function () {
                    alert("An error occurred while deleting the product.");
                    this_val.show();  // Show the delete button again if there's an error
                }
            });
        });

    });

    $(document).on('click', '.add-to-wishlist', function () {
        let product_id = $(this).attr('data-product-item');
        let this_val = $(this)

        console.log("Product ID:" + product_id);

        $.ajax({
            url: '/add-to-wishlist',
            data: {
                'id': product_id,

            },
            dataType: "json",
            beforeSend: function () {

                console.log("Adding to Wishlist ...");

            },
            success: function (response) {
                if (response.bool === true) {
                    this_val.html("Added to wishlist")
                    console.log("Added to Wishlist")
                }
            }

        })



    })

    // Delete From Wishlist
    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    $(document).on('click', '.delete-wishlist', function () {
        console.log('Clicked');
        let wishlist_id = $(this).attr('data-wishlist-product');
        let this_val = $(this)
        console.log('Wishlist ID: ' + wishlist_id);

        $.ajax({
            url: '/delete-from-wishlist',
            data: {
                'id': wishlist_id,
            },
            dataType: "json",
            beforeSend: function () {
                this_val.html('<i class="fas fa-spinner fa-spin"></i> ');
                console.log("Deleting product from Wishlist ...");

            },
            success: function (response) {
                $("#wishlist-list").html(response.data)
                console.log("Deleted product from Wishlist ");

            }


        })
        // $.ajax({
        //     url: '/delete-from-wishlist/',
        //     method: 'POST',
        //     data: {
        //         'id': wishlist_id,
        //         'csrfmiddlewaretoken': csrfToken,
        //         // 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        //     },
        //     dataType: "json",
        //     beforeSend: function () {
        //         this_val.html('<i class="fas fa-spinner fa-spin"></i> Deleting...');
        //     },
        //     success: function (response) {
        //         if (response.success) {
        //             // Only replace the wishlist list section
        //             $("#wishlist-list").html(response.data);
        //         } else {
        //             alert(response.message);  // Show error message if deletion failed
        //         }
        //     },
        //     complete: function () {
        //         this_val.html('<i class="fa fa-times"></i> Delete');
        //     }
        // });


    })



})(jQuery);
