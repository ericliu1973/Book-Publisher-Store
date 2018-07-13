from django.db import models
from hello.models import Book
from django.contrib.auth.models import User

class Order (models.Model):
    first_name = models.CharField(max_length=40)
    last_name=models.CharField(max_length=40)
    email=models.EmailField()
    address =models.CharField(max_length=200)
    post_code=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    paid=models.BooleanField(default=False)
    owner = models.ForeignKey(User,related_name='order',default='')

    def __str__(self):
        return 'order{}'.format(self.id)

    def get_total_price(self):
        return sum(item.get_cost() for item in self.item.all())



class OrderItem(models.Model):
        order = models.ForeignKey(Order,related_name='item')
        product = models.ForeignKey(Book,related_name='order')
        price = models.DecimalField(max_digits=10,decimal_places=2)
        quantity = models.PositiveIntegerField(default=1)

        def __str__(self):
            return '{}'.format(self.id)

        def get_cost(self):
            return self.price*self.quantity
# Create your models here.
