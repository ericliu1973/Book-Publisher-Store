from decimal import Decimal
from django.conf import settings
from hello.models import Book


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)    #cart =self.session['cart']=request.session['cart']
        if not cart:   #
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart  # Actually cart is a dic

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())      #返回cart 中商品的总数

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.遍历购物车中的商品
        cart.keys 是一个个的字符化后的product.id
        """
        product_ids = self.cart.keys()  #为一个购物车中所有的product_id列表
        # get the product objects and add them to the cart
        products = Book.objects.filter(id__in=product_ids)  #queryset of Products
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():   #cart is a dic , the key of cart dic is 'product.id', the value of cart dic is another dic ['prodcut']=product, ['price']=xxxx,['total_price']=xxxx,['quantity']=xxxx
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)  #session 采用JSON结构，因此其key只能支持字符串形式 dict_keys(['quantity', 'price', 'product', 'total_price', 'update_quantity_form'])
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}


        print ('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        print(update_quantity)
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')

        if update_quantity:

            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # update the session cart  settings.CART_SESSION_ID='cart'
        self.session[settings.CART_SESSION_ID] = self.cart  #self.session['cart']=self.cart  和初始化的__init__函数操作正好相反
        # mark the session as "modified" to make sure it is saved ， session.modified = True 相当于对后台DB进行commit
        self.session.modified = True

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        # get the total price of the cart
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
