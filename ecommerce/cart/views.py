from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .cart import Cart
from store.models import Product # Importam modelul Product din aplicatia 'store'


def cart_summary(request):
    
    cart = Cart(request)
    # Cand iteram peste 'cart' in template, se obtin obiectele Product si se calculeaza subtotalul
    return render(request, "cart/cart-summary.html", {"cart": cart})


def cart_add(request):
    try:
        cart = Cart(request)
        
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
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            
            cart.delete(product_id=product_id)
            
            cart_quantity = cart.__len__()
            cart_total = cart.get_total_price()
            
            response = JsonResponse({'quantity': cart_quantity, 'total': cart_total})
            return response
    except Exception as e:
        return JsonResponse({'error': str(e)})


def cart_update(request):
    try:
        cart = Cart(request)
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product_quantity = int(request.POST.get('product_quantity'))
            
            cart.update(product_id=product_id, product_quantity=product_quantity)
            
            cart_quantity = cart.__len__()
            cart_total = cart.get_total_price()
            
            # Subtotalul specific produsului actualizat 
            new_subtotal = float(cart.cart[str(product_id)]['price']) * product_quantity

            response = JsonResponse({'quantity': cart_quantity, 
                                     'total': cart_total, 
                                     'subtotal': new_subtotal})
            return response
    except Exception as e:
        return JsonResponse({'error': str(e)})