import random

class ShoppingEngine:
    def __init__(self):
        self.products = {
            'chocolate': [
                {
                    'name': 'Lindt Excellence Dark Chocolate Box',
                    'price': 9.99,
                    'image': '🍫',
                    'images': [
                        'https://images.unsplash.com/photo-1511381939415-e44015466834?w=400',
                        'https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=400'
                    ],
                    'description': 'Premium 70% dark chocolate, 12 piece assortment',
                    'rating': 4.9,
                    'source': 'Amazon'
                },
                {
                    'name': 'Ghirardelli Intense Dark Collection',
                    'price': 10.99,
                    'image': '🍫',
                    'images': [
                        'https://images.unsplash.com/photo-1606312619070-d48b4cda81f5?w=400',
                        'https://images.unsplash.com/photo-1548907040-4baa42d10919?w=400'
                    ],
                    'description': '86% dark chocolate squares, bold flavor',
                    'rating': 4.7,
                    'source': 'Target'
                }
            ],
            'candlestick': [
                {
                    'name': 'Modern Gold Candlestick Holder - 24" Tall',
                    'price': 19.99,
                    'image': '🕯️',
                    'images': [
                        'https://images.unsplash.com/photo-1602874801006-e877d04d5a1e?w=400',
                        'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=400'
                    ],
                    'description': 'Sleek modern design, 24 inches tall',
                    'rating': 4.8,
                    'source': 'Amazon'
                }
            ],
            'coconut water': [
                {
                    'name': 'Vita Coco Pure Coconut Water 12-Pack',
                    'price': 18.99,
                    'image': '🥥',
                    'images': [
                        'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400',
                        'https://images.unsplash.com/photo-1585217844553-46e8d891c741?w=400'
                    ],
                    'description': 'Natural hydration with electrolytes',
                    'rating': 4.5,
                    'source': 'Amazon'
                }
            ]
        }
    
    def search_products(self, query):
        query_lower = query.lower().strip()
        
        # Exact keyword matching
        for category in self.products.keys():
            if category in query_lower or query_lower in category:
                return self.products[category]
        
        # Return empty if no match
        return []
