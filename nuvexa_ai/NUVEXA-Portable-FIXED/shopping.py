import random

class ShoppingEngine:
    def __init__(self):
        self.products = {
            'coconut water': [
                {'name': 'Vita Coco Pure Coconut Water 12-Pack', 'price': 18.99, 'image': '🥥', 'description': 'Natural hydration with 5 essential electrolytes', 'rating': 4.5, 'source': 'Amazon'},
                {'name': 'Harmless Harvest Organic Coconut Water', 'price': 24.99, 'image': '🥥', 'description': 'USDA Organic, sustainably sourced', 'rating': 4.7, 'source': 'Walmart'},
                {'name': 'C2O Pure Coconut Water 6-Pack', 'price': 12.49, 'image': '🥥', 'description': 'Not from concentrate, no added sugar', 'rating': 4.3, 'source': 'Target'}
            ],
            'peptides': [
                {'name': 'Collagen Peptides Powder by Vital Proteins', 'price': 43.00, 'image': '💊', 'description': '20g collagen per serving, unflavored', 'rating': 4.6, 'source': 'Amazon'},
                {'name': 'Sports Research Collagen Peptides', 'price': 32.95, 'image': '💊', 'description': 'Grass-fed, non-GMO, gluten-free', 'rating': 4.5, 'source': 'Walmart'}
            ],
            'laptop': [
                {'name': 'MacBook Pro 14" M3 Pro', 'price': 1999.00, 'image': '💻', 'description': '18GB RAM, 512GB SSD, Space Black', 'rating': 4.8, 'source': 'Apple Store'},
                {'name': 'Dell XPS 15 Intel Core i7', 'price': 1649.99, 'image': '💻', 'description': '16GB RAM, 512GB SSD, 15.6" OLED', 'rating': 4.6, 'source': 'Dell'}
            ],
            'headphones': [
                {'name': 'Sony WH-1000XM5 Wireless', 'price': 399.99, 'image': '🎧', 'description': 'Industry-leading noise cancellation', 'rating': 4.8, 'source': 'Amazon'},
                {'name': 'Apple AirPods Max', 'price': 549.00, 'image': '🎧', 'description': 'Spatial audio, premium sound', 'rating': 4.7, 'source': 'Apple Store'}
            ]
        }
    
    def search_products(self, query):
        query_lower = query.lower()
        for category, products in self.products.items():
            if category in query_lower:
                return products
        results = []
        for category, products in self.products.items():
            for word in query_lower.split():
                if word in category:
                    results.extend(products)
                    break
        if not results:
            all_products = []
            for products in self.products.values():
                all_products.extend(products)
            return random.sample(all_products, min(3, len(all_products)))
        return results
    
    def get_product_recommendations(self, category):
        return self.products.get(category, [])
