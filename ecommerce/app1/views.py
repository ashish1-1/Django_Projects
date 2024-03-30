from django.shortcuts import render, HttpResponse, redirect
from .models import Product, Order, OrderUpdate
from math import ceil
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from PayTm import paytm_checksum

# Create your views here.

def home(request):
    current_user = request.user
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides =  n//4+ceil((n/4)-(n//4))
        allProds.append([prod, range(1,nSlides), nSlides])
    params = {
        'allprods':allProds
    }
    return render(request, 'index.html', context=params)


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login And Try Again")
        return redirect('/auth/login')
    
    if request.method == 'POST':
        item_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        amt = request.POST.get('amt','')
        email = request.POST.get('email','')
        address1 = request.POST.get('address1','')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')


        order = Order(item_json=item_json, name=name, amount=amt, email=email, address1=address1, address2=address2, city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update =  OrderUpdate(order_id=order.order_id, update_desc="The Order Has Been Placed")
        update.save()
        thank = True

        # PAYMENT INTIGRATION
        # Request Paytm to transfer the amount to your account after payment by user
        param_dict = {
            'MID':'VMLsKh3337413176987',
            'ORDER_ID': str(order.order_id)+"amazonshop",
            'TXN_AMOUNT':str(amt),
            'CUST_ID':email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/'
        }
        param_dict['CHECKSUMHASH'] = paytm_checksum.generate_checksum(param_dict=param_dict,merchant_key='xxxxxxxxxxxxxxxx')
        return render(request,'paytm.html',{'param_dict':param_dict})

    return render(request, 'checkout.html')

@csrf_exempt
def handlerequest(request):
    # PayTm Will Send you post request Here
    form = request.POST
    print(form)
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = paytm_checksum.verify_checksum(response_dict, merchant_key='xxxxxxxxxxxxxxxx',checksum=checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print("Order Succcessful")
        else:
            print("Order does not successfule beacause "+ response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response':response_dict  })

    


