"""hello_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from hello import views
from django.views.generic.dates import ArchiveIndexView
from .models import Book

urlpatterns = [
    url(r'^$', views.hello),

    url(r'^author_list/$',views.author_list,name='author_list'),
    url(r'^store_list/$',views.store_list,name='store_list'),
    url(r'^book_list/$',views.book_list,name='book_list'),
    # url(r'^book_list/$',views.book_list2,name='book_list'),
    url(r'^publisher_list/$',views.publisher_list),
    url(r'^book_list/(?P<year>\d+)/$',views.BookListByYear,name='book_year_list'),
    # url(r'^book/(?P<id>\d+)/$',views.book_datail,name='book_detail'),
    url(r'^addcomment/(?P<id>\d+)/$',views.add_comment,name='add_comment'),
    url(r'^author/(?P<id>\d+)/$',views.author_datail,name='author_detail'),
    # url(r'^post/(?P<pk>[0-9]+)/$',views.PostDetailView.as_view(), name='detail'),
    url(r'^book/(?P<pk>[0-9]+)/$',views.BookDetailView.as_view(),name='book_detail'),
    url(r'^testrating/$',views.BookDetailView.as_view(),name='rating_test'),
    url(r'^search/(?P<s_type>\d+)/(?P<keyword>\w+)/$',views.search,name='search'),
    url(r'^share/(?P<id>\d+)/$',views.share_email,name='share'),
    url(r'^archive/$',ArchiveIndexView.as_view(model=Book,date_field="pubdate"),name='book_archive'),
    url(r'^archive/(?P<year>[0-9]{4})/$',views.BookYearArchiveView.as_view(),name='book_year_archive'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',views.BookMonthArchiveView.as_view(month_format='%m'),name='book_month_numeric'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$',views.BookMonthArchiveView.as_view(),name='book_month_archive'),

    # url(r'^book_list/$',views.BookListView.as_view(),name='book_list'),
    # url(r'^author_list/$',views.AuthorListView.as_view(),name='author_list'),
]
