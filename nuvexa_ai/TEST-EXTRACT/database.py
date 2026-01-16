import sqlite3
import json
from datetime import datetime
from config import DB_NAME

class NuvexaDB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
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
        
        self.conn.commit()
    
    def get_or_create_user(self, name="User"):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM users WHERE name = ?', (name,))
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
            self.conn.commit()
            return cursor.lastrowid
    
    def save_message(self, user_id, mode, message, role):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (user_id, mode, message, role)
            VALUES (?, ?, ?, ?)
        ''', (user_id, mode, message, role))
        self.conn.commit()
    
    def get_conversation_history(self, user_id, mode, limit=10):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT role, message FROM conversations
            WHERE user_id = ? AND mode = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, mode, limit))
        results = cursor.fetchall()
        return [(role, msg) for role, msg in reversed(results)]
    
    def add_to_cart(self, user_id, product_name, product_price, product_image="", product_description=""):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO cart (user_id, product_name, product_price, product_image, product_description)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, product_name, product_price, product_image, product_description))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_cart_items(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, product_name, product_price, product_image, product_description, quantity
            FROM cart WHERE user_id = ?
        ''', (user_id,))
        return cursor.fetchall()
    
    def remove_from_cart(self, cart_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM cart WHERE id = ?', (cart_id,))
        self.conn.commit()
    
    def clear_cart(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
        self.conn.commit()
    
    def create_order(self, user_id, items, total_amount):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO orders (user_id, items, total_amount)
            VALUES (?, ?, ?)
        ''', (user_id, json.dumps(items), total_amount))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_user_orders(self, user_id, limit=5):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, items, total_amount, status, created_at
            FROM orders WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        return cursor.fetchall()
    
    def update_avatar_style(self, user_id, avatar_style):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET avatar_style = ? WHERE id = ?', (avatar_style, user_id))
        self.conn.commit()
    
    def get_avatar_style(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT avatar_style FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 'Stylized Futuristic Human'
