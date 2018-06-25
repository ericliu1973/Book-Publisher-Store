from django import template
from django.db.models import Count
from star_ratings.models import Rating
register =template.Library()
from hello.models import Book

@register.simple_tag
def total_books():
    return Book.objects.count()

@register.assignment_tag
def get_new_books(count =5):
    return Book.objects.order_by('-pubdate')[0:5]

@register.assignment_tag
def get_most_comment(count =5):
    return Book.objects.annotate(total_comment=Count('comment')).order_by('-total_comment')[0:5]

@register.assignment_tag
def get_high_score(count = 5 ):
    return Rating.objects.order_by('-average')[0:5]