class Cart():
    
    def __init__(self, request):
        
        self.session = request.session
        
        # Returning user - obtain his/her existing session_key
        
        cart = self.session.get("session_key")
        
        
        # New user - generate a new session_key
        
        if 'session_key' not in request.session:
            
            cart = self.session["session_key"] = {}
            
        self.cart = cart
        


    def add(self, product, product_quantity):
        
        product_id = str(product.id)
        
        if product_id in self.cart:
            
            self.cart[product_id]['qty'] = int(product_quantity)
            
        else:
            
            self.cart[product_id] = {'price': str(product.price), 
                                    'qty': int(product_quantity)}
            
        self.session.modified = True
        
        
    def __len__(self):
        
        return sum(item['qty'] for item in self.cart.values())