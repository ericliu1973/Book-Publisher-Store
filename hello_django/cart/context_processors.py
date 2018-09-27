from .cart import Cart
def cart(request):
    return {'cart':Cart(request)}    # 在所有的模板文件中使用cart变量，则调用Cart类的初始化实例