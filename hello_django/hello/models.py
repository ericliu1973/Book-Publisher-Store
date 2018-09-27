from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation
from  taggit.managers import TaggableManager

class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(default='xxx@xxx.com')
    nation= models.CharField(max_length=50,default='ca' )
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='PIC/%Y/%m/%d', blank=True)


    def __str__(self):
        return self.name

	
	#通过定于get_absolute_url的方法实现反向URL 	
    def get_absolute_url(self):
        return reverse('hello:author_detail',args=[self.id])

class Publisher(models.Model):
    name = models.CharField(max_length=300)
    num_awards = models.IntegerField()

    # 定义queryset显示方式
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
    stock_number = models.IntegerField(default=0)
    tags = TaggableManager()
    def __str__(self):
        return self.name
		
	#通过定于get_absolute_url的方法实现反向URL 
    def get_absolute_url(self):
        return reverse('hello:book_detail',args=[self.id,])

class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book,related_name='store')


    def __str__(self):
        return self.name


class Comment(models.Model):
    book =models.ForeignKey(Book,related_name='comment')      #通过Book的manager可以采用annotate聚合方式对每本书的comment进行汇总
    content = models.TextField()
    pubdate= models.DateTimeField(auto_now_add=True)
    # pubdate_f=models.DateTimeField(auto_now_add=True)
    person =models.ForeignKey(User,related_name='comment')

    class Meta:
        ordering =('pubdate',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.person,self.book)   #注意format函数的使用方式