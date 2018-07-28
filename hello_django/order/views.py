from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from .models import OrderItem,Order
from .forms import OrderCreateForm
from cart.cart import Cart
# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method =='POST':
        data =OrderCreateForm(data=request.POST)
        print('***************************************************')
        print(data)
        print(dir(data))
        print('***************************************************')
        if data.is_valid():
            cd =data.cleaned_data
            fn=cd['first_name']
            ln=cd['last_name']
            em=cd['email']
            ad=cd['address']
            city=cd['city']
            pc=cd['post_code']
            order =Order.objects.create(first_name=fn,last_name=ln,email=em,city=city,post_code=pc,address=ad,owner=request.user)


            # order=data.save()
            for item in cart:
                book=item['product']
                price=item['price']
                quantity=item['quantity']
                OrderItem.objects.create(order=order,product=book,price=price,quantity=quantity)
            cart.clear()
        # return render(request,'created.html',{'order':order})
        request.session['order_id']=order.id
        return redirect(reverse('payment:process'))
    else:
        form =OrderCreateForm()
        return render(request,'creating.html',{'form':form,'cart':cart,})


def order_list(request):
    order_list = Order.objects.filter(owner=request.user)
    name = request.user.first_name
    return render(request,'order_list.html',{'order_list':order_list,'name':name})