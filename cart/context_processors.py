from .cart import Cart


def cart_history(request):
	return {'cart':Cart(request)}