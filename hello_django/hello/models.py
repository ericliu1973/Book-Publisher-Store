from django.db import models
from django.core.urlresolvers import reverse
class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=300)
    num_awards = models.IntegerField()

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author,related_name='book')
    publisher = models.ForeignKey(Publisher,related_name='book')
    pubdate = models.DateField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book_detail',args=[self.id])

class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book,related_name='store')


    def __str__(self):
        return self.name