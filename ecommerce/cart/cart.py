# cart.py

class Cart():
    
    def __init__(self, request):
        
        self.session = request.session
        
        cart = self.session.get("session_key")
        
        if 'session_key' not in request.session:
            
            cart = self.session["session_key"] = {}
            
        self.cart = cart
        


    def add(self, product, product_quantity):
        
        product_id = str(product.id)
        
        if product_id in self.cart:
            
            self.cart[product_id]['qty'] = int(product_quantity)
            
        else:
            
            # ADAUGAREA IMAGINII PRODUSULUI (calea/url-ul)
            self.cart[product_id] = {'price': str(product.price), 
                                    'qty': int(product_quantity),
                                    'image': str(product.image)} # Salveaza ImageField-ul ca string
            
        self.session.modified = True
        
        
    def __len__(self):
        
        return sum(item['qty'] for item in self.cart.values())

    
    def get_total_price(self):
        """
        Calculeaza pretul total al tuturor produselor din cos.
        """
        # Converteste pretul din string in float inainte de calcul
        return sum(float(item['price']) * item['qty'] for item in self.cart.values())
        
    
    def __iter__(self):
        """
        Itereaza prin produsele din cos, adauga obiectele Product si subtotalul.
        Adaugă logica de gestionare a produselor șterse din baza de date.
        """
        # Import local din aplicatia 'store' (unde se afla modelul Product)
        from store.models import Product 
        
        product_ids = self.cart.keys()
        
        # Cauta obiectele 'Product' in baza de date
        products = Product.objects.filter(id__in=product_ids)
        
        # Creează un dicționar de lookup pentru produsele GĂSITE
        product_lookup = {str(p.id): p for p in products}

        cart = self.cart
        
        keys_to_delete = []

        # Itereaza prin itemii din sesiune
        for item_key, item_data in cart.items():
            
            if item_key in product_lookup:
                
                # Asociaza obiectul produs intreg
                item_data['product'] = product_lookup[item_key]
                
                # Calculeaza subtotalul si converteste pretul
                item_data['price'] = float(item_data['price'])
                item_data['subtotal'] = item_data['price'] * item_data['qty']
                
                yield item_data
            else:
                # Produsul este in sesiune dar nu in DB (se va sterge din sesiune)
                keys_to_delete.append(item_key)
        
        # Sterge cheile orfane din sesiune
        if keys_to_delete:
            for key in keys_to_delete:
                del self.cart[key]
            self.session.modified = True
            
    # Adaugam functiile de delete si update pentru a fi complete
    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        
    def update(self, product_id, product_quantity):
        product_id = str(product_id)
        product_quantity = int(product_quantity)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_quantity
        self.session.modified = True