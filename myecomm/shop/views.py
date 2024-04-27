from django.shortcuts import render, HttpResponseRedirect
from product.models import Product, Category
from django.http import JsonResponse
from django.template.loader import render_to_string
from home.models import OrderLines, SaleOrder
from django.contrib.auth.models import User
# Create your views here.

def shop(request, slug=None):
    context = {
        'categories':Category.objects.all(),
    }
    if slug:
        cate = Category.objects.filter(slug=slug)[0]
        context['products'] = Product.objects.filter(category = cate)
    else:
        context['products'] = Product.objects.all()

    return render(request, 'shop/shop.html',context=context)

def product_price_filter(request):
    context = {}
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price is not None and max_price is not None:
        data = context['products'] = Product.objects.filter(price__range=(min_price, max_price))
    html = render_to_string('product/product_price_filter.html',context=context)
    return JsonResponse({'data':html, 'product_count':len(data)})


def addToCart(request):
    if request.method == 'POST':
        if request.user.is_anonymous:
            try:
                user = User.objects.get(username='anon')
            except User.DoesNotExist as e:
                user = User.objects.create(username='anon',)
            request.user = user
           
        order = SaleOrder.objects.create(user=request.user)
        product_id = request.POST.get('productId')
        product = Product.objects.filter(uid=product_id).first()
        print("======================",product)
        line = OrderLines.objects.create(product=product, order=order, name=product.product_name, price=product.price)
        line.qty+=1
        line.save()
        print("============Float", float(line.price * line.qty))
        order.totalPrice+= float(line.price * line.qty)
        order.save()
        print("============Total", order.totalPrice)

        # Perform the necessary actions (e.g., create order lines)
        # Replace this with your actual logic
        
        # For demonstration purposes, let's just return a success response
        response_data = {'message': 'Order line created successfully for product ID {}'.format(product_id)}
        return JsonResponse(response_data)
    else:
        # Return a bad request response if the request method is not POST or it's not an AJAX request
        return JsonResponse({'error': 'Bad request'}, status=400)
