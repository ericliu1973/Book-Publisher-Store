from django.core.urlresolvers import  reverse
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from  hello.models import Book,Author,Publisher,Store,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView,DetailView
from hello.forms import CommentForm,SearchForm,EmailForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.core.mail import send_mail
from django.views.generic.dates import YearArchiveView,MonthArchiveView,DayArchiveView
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
def book_list2(request):
    book_list=Book.objects.all()
    paginator = Paginator(book_list,4)
    page= request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books= paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        books = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return  render(request,'book_list_ajax.html',{'books':books})
    return render(request,'book_list2.html',{'books':books})





@login_required
def author_list(request):
    authors = Author.objects.all()
    if request.method=='POST':
         search_form=SearchForm(data=request.POST)
         if search_form.is_valid():
             cd= search_form.cleaned_data
             s_type = cd['search_type']
             keyword = cd['search_words']
             return HttpResponseRedirect(reverse("hello:search",kwargs={'s_type':s_type,'keyword':keyword}))

    form=SearchForm()
    return render(request, 'author_list.html', {'authors': authors,'form': form})

def search(request,s_type,keyword):
    if s_type=='0':
        alist = Author.objects.filter(name__contains=keyword)
        if len(alist)>0:
            return render(request,'search_result.html',{'authors':alist,'flag':0,'num':1})
    if s_type=='1':
        blist=Book.objects.filter(name__contains=keyword)
        if len(blist)>0:
            return render(request,'search_result.html',{'books':blist,'flag':1,'num':1})

    return render(request,'search_result.html',{'num':0})

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


def share_email(request,id):
    book = Book.objects.get(id=id)
    sent = False
    book_abs_url = request.build_absolute_uri(book.get_absolute_url())
    form =EmailForm()
    if request.method=='POST':
        form = EmailForm(data=request.POST)
        if form.is_valid():
            cd =form.cleaned_data
            subject = 'Dear {},your friend {} recomends the book :{} to you'.format(cd['person'],request.user.first_name,book.name)
            message = '{}\n\nThe URL of this book : {}'.format(cd['info'],book_abs_url)
            send_mail(subject,message,'admin@liuyu.ca',[cd['to']])
            sent= True
        else:
            form = EmailForm()
    return render(request,'share.html',{'form':form,'sent':sent,'book':book})

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

class BookYearArchiveView(YearArchiveView):
    queryset = Book.objects.all()
    date_field = "pubdate"
    make_object_list = True
    allow_future = True


class BookMonthArchiveView(MonthArchiveView):
    queryset = Book.objects.all()
    date_field = 'pubdate'
    make_object_list = True
    allow_future = True

