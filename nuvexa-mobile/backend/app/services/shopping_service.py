"""
Shopping service for product search.
Currently uses mock data, can be extended with real APIs.
"""
from typing import List, Dict


class ShoppingService:
    """Service for product search operations."""

    def __init__(self):
        # Mock product database
        self.products = {
            'laptop': [
                {
                    'name': 'MacBook Air M2 13"',
                    'price': 1199.00,
                    'image': '💻',
                    'images': [
                        'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400',
                        'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=400'
                    ],
                    'description': 'Powerful M2 chip, 8GB RAM, 256GB SSD, stunning Retina display',
                    'rating': 4.8,
                    'source': 'Apple Store'
                },
                {
                    'name': 'Dell XPS 13 Plus',
                    'price': 1299.00,
                    'image': '💻',
                    'images': [
                        'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400',
                        'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400'
                    ],
                    'description': 'Intel i7, 16GB RAM, 512GB SSD, edge-to-edge display',
                    'rating': 4.6,
                    'source': 'Dell'
                }
            ],
            'headphones': [
                {
                    'name': 'Sony WH-1000XM5',
                    'price': 399.99,
                    'image': '🎧',
                    'images': [
                        'https://images.unsplash.com/photo-1545127398-14699f92334b?w=400',
                        'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400'
                    ],
                    'description': 'Industry-leading noise cancellation, 30-hour battery, exceptional sound',
                    'rating': 4.9,
                    'source': 'Amazon'
                },
                {
                    'name': 'Apple AirPods Max',
                    'price': 549.00,
                    'image': '🎧',
                    'images': [
                        'https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=400',
                        'https://images.unsplash.com/photo-1625075751551-ec7c8f5cd11e?w=400'
                    ],
                    'description': 'Premium over-ear design, spatial audio, active noise cancellation',
                    'rating': 4.7,
                    'source': 'Apple Store'
                }
            ],
            'phone': [
                {
                    'name': 'iPhone 15 Pro',
                    'price': 999.00,
                    'image': '📱',
                    'images': [
                        'https://images.unsplash.com/photo-1678911820864-e5c47f6f2e82?w=400',
                        'https://images.unsplash.com/photo-1592286927505-b7e2e2b77c89?w=400'
                    ],
                    'description': 'A17 Pro chip, titanium design, 48MP camera, USB-C',
                    'rating': 4.8,
                    'source': 'Apple Store'
                },
                {
                    'name': 'Samsung Galaxy S24 Ultra',
                    'price': 1199.00,
                    'image': '📱',
                    'images': [
                        'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400',
                        'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400'
                    ],
                    'description': 'Snapdragon 8 Gen 3, 200MP camera, S Pen included, 12GB RAM',
                    'rating': 4.7,
                    'source': 'Samsung'
                }
            ],
            'watch': [
                {
                    'name': 'Apple Watch Series 9',
                    'price': 399.00,
                    'image': '⌚',
                    'images': [
                        'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=400',
                        'https://images.unsplash.com/photo-1434494878577-86c23bcb06b9?w=400'
                    ],
                    'description': 'S9 chip, double tap gesture, health tracking, always-on display',
                    'rating': 4.8,
                    'source': 'Apple Store'
                }
            ],
            'tablet': [
                {
                    'name': 'iPad Pro 11"',
                    'price': 799.00,
                    'image': '📱',
                    'images': [
                        'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400',
                        'https://images.unsplash.com/photo-1585790050230-5dd28404f1b4?w=400'
                    ],
                    'description': 'M2 chip, Liquid Retina display, Apple Pencil support',
                    'rating': 4.9,
                    'source': 'Apple Store'
                }
            ],
            'camera': [
                {
                    'name': 'Sony Alpha 7 IV',
                    'price': 2499.00,
                    'image': '📷',
                    'images': [
                        'https://images.unsplash.com/photo-1606980707986-77f4c90aa2f0?w=400',
                        'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400'
                    ],
                    'description': '33MP full-frame sensor, 4K 60fps video, advanced autofocus',
                    'rating': 4.9,
                    'source': 'B&H Photo'
                }
            ]
        }

    def search_products(self, query: str) -> List[Dict]:
        """
        Search for products based on query.

        Args:
            query: Search query string

        Returns:
            List of matching products
        """
        query_lower = query.lower().strip()

        # Search through all categories
        results = []
        for category, products in self.products.items():
            if category in query_lower or query_lower in category:
                results.extend(products)

        # Also check product names and descriptions
        if not results:
            for category, products in self.products.items():
                for product in products:
                    if (query_lower in product['name'].lower() or
                        query_lower in product['description'].lower()):
                        results.append(product)

        return results

    def get_categories(self) -> List[str]:
        """Get all available product categories."""
        return list(self.products.keys())
