from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST
from hello.models import Book
from .cart import Cart
from .form import CartAddForm

# Create your views here.
@require_POST
def cart_add(request,id):
    cart = Cart(request)
    book = get_object_or_404(Book,id=id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=book ,quantity=cd['quantity'],update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(requst,id):
    cart = Cart(requst)
    book = get_object_or_404(Book,id=id)
    cart.remove(book)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)

    for item in cart:
        item['update_quantity_form'] =CartAddForm(initial={'quantity':item['quantity'],'update':True})
    return render(request,'cart_detail.html',{'cart':cart})