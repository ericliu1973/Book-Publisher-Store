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

urlpatterns = [
    url(r'^hello/$', views.hello),
    # url(r'^author_list/$',views.author_list,name='author_list'),
    url(r'^store_list/$',views.store_list,name='store_list'),
    # url(r'^book_list/$',views.book_list,name='book_list'),
    url(r'^publisher_list/$',views.publisher_list),
    url(r'^book/(?P<id>\d+)/$',views.book_datail,name='book_detail'),
    url(r'^author/(?P<id>\d+)/$',views.author_datail,name='author_detail'),
    url(r'^book_list/$',views.BookListView.as_view(),name='book_list'),
    url(r'^author_list/$',views.AuthorListView.as_view(),name='author_list'),
]
