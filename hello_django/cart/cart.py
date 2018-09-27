from decimal import Decimal
from django.conf import settings
from hello.models import Book


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session    #注意字典的赋值相当于文件的硬链接，共享同一段内存地址，因此改变对源字典和目标字典就生效
        cart = self.session.get(settings.CART_SESSION_ID)    #cart =self.session['cart']=request.session['cart']，作为request.session['cart']的value， 而其自身实质是个字典
        if not cart:   #
            # save an empty cart in the session ，其实质就是cart作为request.session['cart']的value，其自身就是一个空字典
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart  # Actually cart is a dic

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())      #返回cart 中商品的总数，对于类Cart 可用使用len()函数返回购物车中的商品数量

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.遍历购物车中的商品
        cart.keys 是一个个的字符化后的product.id  （cart字典中的key 就是商品的ID)
        """
        product_ids = self.cart.keys()  #为一个购物车中所有的product_id列表(准确讲不是列表，其数据类型是class dict_keys,但是其是可以迭代访问的， 在cart的字典里其key是product_id,value是针对此product的数量/价格等键值对
        # get the product objects and add them to the cart
        products = Book.objects.filter(id__in=product_ids)  #queryset of Products 返回一个BOOK的queryset(本身可以迭代查询）
        for product in products:
            self.cart[str(product.id)]['product'] = product    #在cart字典中额外定义的一个键值对其key是'product',value是product实例

        for item in self.cart.values():   #cart is a dic , the keys of cart dic is 'product.id', the values of cart dic  are 键值对['prodcut']=product实例, ['price']=xxxx,['total_price']=xxxx,['quantity']=xxxx
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
            self.cart[product_id]['quantity'] += quantity    #update_quantity为false 则是累加商品数量
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
