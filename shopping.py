import random
from typing import List, Dict, Any
import re

class ShoppingEngine:
    """Product search and recommendation engine."""
    
    def __init__(self):
        """Initialize with product catalog."""
        self.products = {
            'coconut water': [
                {'name': 'Vita Coco Pure Coconut Water 12-Pack', 'price': 18.99, 'image': '🥥', 
                 'description': 'Natural hydration with 5 essential electrolytes', 'rating': 4.5, 'source': 'Amazon'},
                {'name': 'Harmless Harvest Organic Coconut Water', 'price': 24.99, 'image': '🥥', 
                 'description': 'USDA Organic, sustainably sourced', 'rating': 4.7, 'source': 'Walmart'},
                {'name': 'C2O Pure Coconut Water 6-Pack', 'price': 12.49, 'image': '🥥', 
                 'description': 'Not from concentrate, no added sugar', 'rating': 4.3, 'source': 'Target'},
                {'name': 'Zico Natural Coconut Water', 'price': 16.99, 'image': '🥥', 
                 'description': '100% pure coconut water, no added sugar', 'rating': 4.4, 'source': 'Amazon'}
            ],
            'peptides': [
                {'name': 'Collagen Peptides Powder by Vital Proteins', 'price': 43.00, 'image': '💊', 
                 'description': '20g collagen per serving, unflavored', 'rating': 4.6, 'source': 'Amazon'},
                {'name': 'Sports Research Collagen Peptides', 'price': 32.95, 'image': '💊', 
                 'description': 'Grass-fed, non-GMO, gluten-free', 'rating': 4.5, 'source': 'Walmart'},
                {'name': 'Orgain Collagen Peptides', 'price': 28.99, 'image': '💊', 
                 'description': 'Unflavored, 20g protein per serving', 'rating': 4.4, 'source': 'Target'}
            ],
            'laptop': [
                {'name': 'MacBook Pro 14" M3 Pro', 'price': 1999.00, 'image': '💻', 
                 'description': '18GB RAM, 512GB SSD, Space Black', 'rating': 4.8, 'source': 'Apple Store'},
                {'name': 'Dell XPS 15 Intel Core i7', 'price': 1649.99, 'image': '💻', 
                 'description': '16GB RAM, 512GB SSD, 15.6" OLED', 'rating': 4.6, 'source': 'Dell'},
                {'name': 'HP Spectre x360 14"', 'price': 1299.99, 'image': '💻', 
                 'description': '2-in-1 convertible, Intel Core i7, 16GB RAM', 'rating': 4.5, 'source': 'HP'},
                {'name': 'Lenovo ThinkPad X1 Carbon', 'price': 1499.00, 'image': '💻', 
                 'description': '14" Ultrabook, 16GB RAM, 512GB SSD', 'rating': 4.7, 'source': 'Lenovo'}
            ],
            'headphones': [
                {'name': 'Sony WH-1000XM5 Wireless', 'price': 399.99, 'image': '🎧', 
                 'description': 'Industry-leading noise cancellation', 'rating': 4.8, 'source': 'Amazon'},
                {'name': 'Apple AirPods Max', 'price': 549.00, 'image': '🎧', 
                 'description': 'Spatial audio, premium sound', 'rating': 4.7, 'source': 'Apple Store'},
                {'name': 'Bose QuietComfort 45', 'price': 329.00, 'image': '🎧', 
                 'description': 'Comfortable over-ear with noise cancellation', 'rating': 4.6, 'source': 'Bose'},
                {'name': 'Sennheiser Momentum 4', 'price': 379.99, 'image': '🎧', 
                 'description': 'Premium sound quality, 60-hour battery', 'rating': 4.7, 'source': 'Amazon'}
            ],
            'phone': [
                {'name': 'iPhone 15 Pro', 'price': 999.00, 'image': '📱', 
                 'description': '6.1" Super Retina XDR, A17 Pro chip', 'rating': 4.8, 'source': 'Apple Store'},
                {'name': 'Samsung Galaxy S24', 'price': 799.99, 'image': '📱', 
                 'description': '6.2" Dynamic AMOLED, 128GB storage', 'rating': 4.7, 'source': 'Samsung'},
                {'name': 'Google Pixel 8 Pro', 'price': 899.00, 'image': '📱', 
                 'description': '6.7" LTPO OLED, 128GB, AI-powered camera', 'rating': 4.6, 'source': 'Google Store'}
            ],
            'tablet': [
                {'name': 'iPad Pro 12.9" M2', 'price': 1099.00, 'image': '📱', 
                 'description': '12.9" Liquid Retina XDR, 256GB', 'rating': 4.8, 'source': 'Apple Store'},
                {'name': 'Samsung Galaxy Tab S9', 'price': 799.99, 'image': '📱', 
                 'description': '11" AMOLED, 128GB, S Pen included', 'rating': 4.6, 'source': 'Samsung'}
            ]
        }
        
        # Create keyword mapping for better search
        self.keyword_map = {
            'coconut': 'coconut water',
            'water': 'coconut water',
            'coco': 'coconut water',
            'collagen': 'peptides',
            'peptide': 'peptides',
            'supplement': 'peptides',
            'computer': 'laptop',
            'notebook': 'laptop',
            'macbook': 'laptop',
            'headphone': 'headphones',
            'earphone': 'headphones',
            'earbud': 'headphones',
            'smartphone': 'phone',
            'mobile': 'phone',
            'ipad': 'tablet',
            'tablet': 'tablet'
        }
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """Search for products based on query."""
        if not query or not query.strip():
            return []
        
        query_lower = query.lower().strip()
        results = []
        
        # Direct category match
        for category, products in self.products.items():
            if category in query_lower:
                results.extend(products)
                break
        
        # Keyword-based search
        if not results:
            matched_categories = set()
            query_words = re.findall(r'\w+', query_lower)
            
            for word in query_words:
                if word in self.keyword_map:
                    category = self.keyword_map[word]
                    if category not in matched_categories:
                        matched_categories.add(category)
                        results.extend(self.products.get(category, []))
            
            # Partial word matching in category names
            if not results:
                for category, products in self.products.items():
                    for word in query_words:
                        if word in category or category in word:
                            results.extend(products)
                            break
        
        # If still no results, search product names and descriptions
        if not results:
            query_words = set(re.findall(r'\w+', query_lower))
            for category, products in self.products.items():
                for product in products:
                    product_text = f"{product['name']} {product['description']}".lower()
                    if any(word in product_text for word in query_words if len(word) > 2):
                        results.append(product)
        
        # If no matches, return random recommendations
        if not results:
            all_products = []
            for products in self.products.values():
                all_products.extend(products)
            results = random.sample(all_products, min(5, len(all_products)))
        
        # Remove duplicates and limit results
        seen = set()
        unique_results = []
        for product in results:
            product_key = product['name']
            if product_key not in seen:
                seen.add(product_key)
                unique_results.append(product)
        
        return unique_results[:10]  # Limit to 10 results
    
    def get_product_recommendations(self, category: str) -> List[Dict[str, Any]]:
        """Get product recommendations for a category."""
        return self.products.get(category.lower(), [])
