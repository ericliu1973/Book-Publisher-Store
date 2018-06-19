from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^login/$', views.user_login, name='login'),
    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),

    # login / logout urls   login/logout/logout-then-login used view function from django
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),

    # change password urls   password-change/done used view function from django
    url(r'^password-change/$', 'django.contrib.auth.views.password_change', {'template_name':'registration/password_change_form.html','post_change_redirect':'account:password_change_done'}, name='password_change'),
    url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),

    # restore password urls   password-reset/done/confirm/complet also used the function provided by django
    url(r'^password-reset/$', 'django.contrib.auth.views.password_reset',{'template_name':'registration/password_reset_form.html','post_reset_redirect':'account:password_reset_done'}, name='password_reset'),
    url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', 'django.contrib.auth.views.password_reset_confirm',{'template_name':'registration/password_reset_confirm.html','post_reset_redirect':'account:password_reset_complete'}, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
]