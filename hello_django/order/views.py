from django.shortcuts import render
from .models import OrderItem,Order
from .forms import OrderCreateForm
from cart.cart import Cart
# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method =='POST':
        data =OrderCreateForm(data=request.POST)
        if data.is_valid():
            order=data.save()
            for item in cart:
                book=item['product']
                price=item['price']
                quantity=item['quantity']
                OrderItem.objects.create(order=order,product=book,price=price,quantity=quantity)
            cart.clear()
        return render(request,'created.html',{'order':order})
    else:
        form =OrderCreateForm()
        return render(request,'creating.html',{'form':form,'cart':cart,})
