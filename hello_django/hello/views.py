from django.core.urlresolvers import  reverse
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from  hello.models import Book,Author,Publisher,Store,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView,DetailView
from hello.forms import CommentForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def hello(request):
	return  HttpResponseRedirect(reverse("account:login",))
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

    comments = book.comment.all()

    if request.method=='POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment= comment_form.save(commit=False)
            new_comment.book=book
            new_comment.person=request.user
            new_comment.save()
    else:
        comment_form=CommentForm()
        new_comment=False




    return render(request,'book_detail.html',{'book':book,'comments':comments,'comment_form':comment_form,'new_comment':new_comment})

def add_comment(request,id):
    book = Book.objects.get(id=id)
    if request.method=='POST':
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.person = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse("hello:book_detail",kwargs={"pk":book.id}))
    else:
        comment_form = CommentForm()
        new_comment = False
    return render(request, 'add_comment.html',
                  {'book': book, 'comment_form': comment_form, 'new_comment': new_comment})

@login_required
def author_datail(request,id):
    author = get_object_or_404(Author, id=id)
    return render(request,'author_detail.html',{'author':author})


class BookListView(ListView):
    queryset = Book.objects.all()
    context_object_name = 'books'
    paginate_by = 3
    template_name = 'book_list.html'

@login_required
def BookListByYear(request,year):
    book_list=Book.objects.filter(pubdate__year=year)
    paginator=Paginator(book_list,3)
    page=request.GET.get('page')
    try:
            books = paginator.page(page)
    except PageNotAnInteger:
            books =paginator.page(1)
    except EmptyPage:
            books=paginator.page(paginator.num_pages)
    return render(request,'book_list.html',{'page':page,'books':books })





class AuthorListView(ListView):
    queryset = Author.objects.all()
    context_object_name = 'authors'
    paginate_by = 3
    template_name = 'author_list.html'

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    # def get_object(self, queryset=None):
    #     obj=self.model.objects.get(name__startswith='python')
    #     return obj

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(BookDetailView, self).get_context_data(**kwargs)
        # form = CommentForm()
        comment_list = self.object.comment.all()
        context.update({
            # 'form': form,
            'comment_list': comment_list,
        })
        return context
