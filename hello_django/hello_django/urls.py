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
from django.conf.urls import include,url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^paypal/', include("paypal.standard.ipn.urls")),
    url(r'^order/', include("order.urls", namespace='order',app_name='order')),
    url(r'^cart/', include("cart.urls", namespace='cart')),
    url(r'^payment/', include("payment.urls", namespace='payment')),
    url(r'^account/',include("account.urls",namespace='account',app_name='account')),
    url(r'^', include("hello.urls",namespace='hello',app_name='hello')),
    url(r'^ratings/',include("star_ratings.urls",namespace='ratings',app_name='ratings')),
    url(r'^oauth/', include("social_django.urls", namespace='social')),
    url(r'^search/', include('haystack.urls')),
]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
