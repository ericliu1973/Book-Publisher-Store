from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(default='xxx@xxx.com')
    nation= models.CharField(max_length=50,default='ca' )
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='PIC/%Y/%m/%d', blank=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author_detail',args=[self.id])

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
        return reverse('book_detail',args=[self.id,])

class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book,related_name='store')


    def __str__(self):
        return self.name


class Comment(models.Model):
    book =models.ForeignKey(Book,related_name='comment')
    body = models.TextField()
    pubdate= models.DateTimeField(auto_now_add=True)
    # pubdate_f=models.DateTimeField(auto_now_add=True)
    person =models.ForeignKey(User,related_name='comment')

    class Meta:
        ordering =('pubdate',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.person,self.book)