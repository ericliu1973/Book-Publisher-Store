from django.contrib import admin
from .models import Author,Publisher,Book,Store,Comment

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Store)
admin.site.register(Publisher)
admin.site.register(Comment)
# Register your models here.
