from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from  hello.models import Book,Author,Publisher,Store
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
# Create your views here.
def hello(request):
	user_list = User.objects.all()
	return render(request, 'table.html', {'user_list':user_list})

@login_required
def book_list(request):
        # books=Book.objects.all()
        # return render(request,'book_list.html',{'books':books})
        book_list = Book.objects.all()
        paginator=Paginator(book_list,3)
        page=request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books =paginator.page(1)
        except EmptyPage:
            books=paginator.page(paginator.num_pages)
        return render(request,'book_list.html',{'page':page,
                                                    'books':books })
@login_required
def author_list(request):
	authors=Author.objects.all()
	return render(request,'author_list.html',{'authors':authors})
@login_required
def publisher_list(request):
	publishers=Publisher.objects.all()
	return render(request,'publisher_list.html',{'publishers':publishers})
@login_required
def store_list(request):
	# stores=Store.objects.all()
	# return render(request,'store_list.html',{'stores':stores})
    store_list = Store.objects.all()
    paginator = Paginator(store_list, 1)
    page = request.GET.get('page')
    try:
        stores = paginator.page(page)
    except PageNotAnInteger:
        stores = paginator.page(1)
    except EmptyPage:
        stores = paginator.page(paginator.num_pages)
    return render(request, 'store_list.html', {'page': page,
                                              'stores': stores})
@login_required
def book_datail(request,id):
    book = get_object_or_404(Book, id=id)
    return render(request,'book_detail.html',{'book':book})

@login_required
def author_datail(request,id):
    author = get_object_or_404(Author, id=id)
    return render(request,'author_detail.html',{'author':author})


class BookListView(ListView):
    queryset = Book.objects.all()
    context_object_name = 'books'
    paginate_by = 3
    template_name = 'book_list.html'

class AuthorListView(ListView):
    queryset = Author.objects.all()
    context_object_name = 'authors'
    paginate_by = 3
    template_name = 'author_list.html'

