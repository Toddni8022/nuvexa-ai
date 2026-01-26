import sqlite3
import json
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any
from contextlib import contextmanager
from config import DB_NAME
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NuvexaDB:
    """Database handler for NUVEXA application."""
    
    def __init__(self):
        """Initialize database connection and create tables."""
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        self.create_tables()
    
    def __del__(self):
        """Close database connection on deletion."""
        if hasattr(self, 'conn'):
            self.conn.close()
    
    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor."""
        cursor = self.conn.cursor()
        try:
            yield cursor
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            cursor.close()
    
    def create_tables(self):
        """Create database tables if they don't exist."""
        with self.get_cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    avatar_style TEXT DEFAULT 'Stylized Futuristic Human',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    mode TEXT NOT NULL,
                    message TEXT NOT NULL,
                    role TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    product_name TEXT NOT NULL,
                    product_price REAL NOT NULL,
                    product_image TEXT,
                    product_description TEXT,
                    quantity INTEGER DEFAULT 1,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    items TEXT NOT NULL,
                    total_amount REAL NOT NULL,
                    status TEXT DEFAULT 'completed',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_conversations_user_mode 
                ON conversations(user_id, mode, timestamp)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_cart_user 
                ON cart(user_id)
            ''')
    
    def get_or_create_user(self, name: str = "User") -> int:
        """Get existing user or create a new one."""
        if not name or not name.strip():
            name = "User"
        
        with self.get_cursor() as cursor:
            cursor.execute('SELECT id FROM users WHERE name = ?', (name.strip(),))
            result = cursor.fetchone()
            
            if result:
                return result[0]
            else:
                cursor.execute('INSERT INTO users (name) VALUES (?)', (name.strip(),))
                return cursor.lastrowid
    
    def save_message(self, user_id: int, mode: str, message: str, role: str) -> bool:
        """Save a conversation message."""
        if not message or not message.strip() or role not in ["user", "assistant"]:
            return False
        
        try:
            with self.get_cursor() as cursor:
                cursor.execute('''
                    INSERT INTO conversations (user_id, mode, message, role)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, mode, message.strip(), role))
            return True
        except Exception as e:
            logger.error(f"Failed to save message: {str(e)}")
            return False
    
    def get_conversation_history(self, user_id: int, mode: str, limit: int = 20) -> List[Tuple[str, str]]:
        """Get conversation history for a user in a specific mode."""
        with self.get_cursor() as cursor:
            cursor.execute('''
                SELECT role, message FROM conversations
                WHERE user_id = ? AND mode = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, mode, limit))
            results = cursor.fetchall()
            return [(row[0], row[1]) for row in reversed(results)]
    
    def add_to_cart(self, user_id: int, product_name: str, product_price: float, 
                    product_image: str = "", product_description: str = "", quantity: int = 1) -> Optional[int]:
        """Add item to cart or update quantity if already exists."""
        if not product_name or product_price < 0 or quantity < 1:
            return None
        
        try:
            with self.get_cursor() as cursor:
                # Check if item already exists in cart
                cursor.execute('''
                    SELECT id, quantity FROM cart 
                    WHERE user_id = ? AND product_name = ?
                ''', (user_id, product_name))
                existing = cursor.fetchone()
                
                if existing:
                    # Update quantity
                    new_quantity = existing[1] + quantity
                    cursor.execute('''
                        UPDATE cart SET quantity = ? WHERE id = ?
                    ''', (new_quantity, existing[0]))
                    return existing[0]
                else:
                    # Insert new item
                    cursor.execute('''
                        INSERT INTO cart (user_id, product_name, product_price, product_image, product_description, quantity)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (user_id, product_name, product_price, product_image, product_description, quantity))
                    return cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to add to cart: {str(e)}")
            return None
    
    def get_cart_items(self, user_id: int) -> List[Tuple]:
        """Get all items in user's cart."""
        with self.get_cursor() as cursor:
            cursor.execute('''
                SELECT id, product_name, product_price, product_image, product_description, quantity
                FROM cart WHERE user_id = ?
                ORDER BY added_at DESC
            ''', (user_id,))
            return cursor.fetchall()
    
    def update_cart_quantity(self, cart_id: int, quantity: int) -> bool:
        """Update quantity of a cart item."""
        if quantity < 1:
            return self.remove_from_cart(cart_id)
        
        try:
            with self.get_cursor() as cursor:
                cursor.execute('UPDATE cart SET quantity = ? WHERE id = ?', (quantity, cart_id))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to update cart quantity: {str(e)}")
            return False
    
    def remove_from_cart(self, cart_id: int) -> bool:
        """Remove item from cart."""
        try:
            with self.get_cursor() as cursor:
                cursor.execute('DELETE FROM cart WHERE id = ?', (cart_id,))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to remove from cart: {str(e)}")
            return False
    
    def clear_cart(self, user_id: int) -> bool:
        """Clear all items from user's cart."""
        try:
            with self.get_cursor() as cursor:
                cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
                return True
        except Exception as e:
            logger.error(f"Failed to clear cart: {str(e)}")
            return False
    
    def create_order(self, user_id: int, items: List[Dict[str, Any]], total_amount: float) -> Optional[int]:
        """Create a new order from cart items."""
        if not items or total_amount < 0:
            return None
        
        try:
            with self.get_cursor() as cursor:
                cursor.execute('''
                    INSERT INTO orders (user_id, items, total_amount)
                    VALUES (?, ?, ?)
                ''', (user_id, json.dumps(items), total_amount))
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to create order: {str(e)}")
            return None
    
    def get_user_orders(self, user_id: int, limit: int = 10) -> List[Tuple]:
        """Get user's order history."""
        with self.get_cursor() as cursor:
            cursor.execute('''
                SELECT id, items, total_amount, status, created_at
                FROM orders WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))
            return cursor.fetchall()
    
    def update_avatar_style(self, user_id: int, avatar_style: str) -> bool:
        """Update user's avatar style preference."""
        if avatar_style not in ['Stylized Futuristic Human', 'Realistic Human', 
                                'Anime Style', 'Cartoon Style', 'Minimalist Icon']:
            return False
        
        try:
            with self.get_cursor() as cursor:
                cursor.execute('UPDATE users SET avatar_style = ? WHERE id = ?', (avatar_style, user_id))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to update avatar style: {str(e)}")
            return False
    
    def get_avatar_style(self, user_id: int) -> str:
        """Get user's avatar style preference."""
        with self.get_cursor() as cursor:
            cursor.execute('SELECT avatar_style FROM users WHERE id = ?', (user_id,))
            result = cursor.fetchone()
            return result[0] if result else 'Stylized Futuristic Human'
