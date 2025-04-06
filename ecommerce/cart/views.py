from django.shortcuts import render
from django.http import JsonResponse

from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404

def cart_summary(request):
    return render(request, "cart/cart-summary.html")

def cart_add(request):
    try:
        cart = Cart(request)
        print(type(cart))
        
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_quantity = int(request.POST.get('product_quantity'))

            product = get_object_or_404(Product, id=product_id)
            
            cart.add(product=product, product_quantity=product_quantity)


            cart_quantity = cart.__len__()
            
            
            response = JsonResponse({'quantity': cart_quantity})
            return response
    except Exception as e:
        return JsonResponse({'error': str(e)})

def cart_delete(request):
    try:
        cart = Cart(request)
        # implement logic to delete product from cart
        pass
    except Exception as e:
        return JsonResponse({'error': str(e)})

def cart_update(request):
    try:
        cart = Cart(request)
        # implement logic to update product quantity in cart
        pass
    except Exception as e:
        return JsonResponse({'error': str(e)})