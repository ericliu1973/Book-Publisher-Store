from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from  hello.models import Book,Author,Publisher,Store
# Create your views here.
def hello(request):
	user_list = User.objects.all()
	return render(request, 'table.html', {'user_list':user_list})

def book_list(request):
	books=Book.objects.all()
	return render(request,'book_list.html',{'books':books})

def author_list(request):
	authors=Author.objects.all()
	return render(request,'author_list.html',{'authors':authors})

def publisher_list(request):
	publishers=Publisher.objects.all()
	return render(request,'publisher_list.html',{'publishers':publishers})

def store_list(request):
	stores=Store.objects.all()
	return render(request,'store_list.html',{'stores':stores})

def book_datail(request,id):
    book = get_object_or_404(Book, id=id)
    return render(request,'book_detail.html',{'book':book})
