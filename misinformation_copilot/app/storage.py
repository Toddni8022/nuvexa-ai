"""SQLite database storage and file management"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from .config import DB_PATH, SCREENSHOTS_DIR


class PostStorage:
    """Manages storage and retrieval of collected posts"""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database with required schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_name TEXT NOT NULL,
                url TEXT,
                author TEXT,
                post_timestamp TEXT,
                text_content TEXT,
                screenshot_path TEXT,
                collected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'queued',
                misinfo_score INTEGER,
                tags TEXT,
                rationale TEXT,
                fact_check_questions TEXT,
                drafts TEXT
            )
        """)

        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_status ON posts(status)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_score ON posts(misinfo_score)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_target ON posts(target_name)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_collected_at ON posts(collected_at)
        """)

        conn.commit()
        conn.close()

    def add_post(
        self,
        target_name: str,
        url: Optional[str] = None,
        author: Optional[str] = None,
        post_timestamp: Optional[str] = None,
        text_content: Optional[str] = None,
        screenshot_path: Optional[str] = None
    ) -> int:
        """Add a new post to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO posts (
                target_name, url, author, post_timestamp,
                text_content, screenshot_path, status
            )
            VALUES (?, ?, ?, ?, ?, ?, 'queued')
        """, (target_name, url, author, post_timestamp, text_content, screenshot_path))

        post_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return post_id

    def update_post(self, post_id: int, **kwargs):
        """Update post fields"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build dynamic update query
        allowed_fields = {
            'status', 'misinfo_score', 'tags', 'rationale',
            'fact_check_questions', 'drafts', 'url', 'author',
            'post_timestamp', 'text_content'
        }

        updates = []
        values = []

        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(f"{key} = ?")
                # Convert lists/dicts to JSON strings
                if isinstance(value, (list, dict)):
                    value = json.dumps(value)
                values.append(value)

        if updates:
            values.append(post_id)
            query = f"UPDATE posts SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()

        conn.close()

    def get_post(self, post_id: int) -> Optional[Dict[str, Any]]:
        """Get a single post by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return self._row_to_dict(row)
        return None

    def get_posts(
        self,
        status: Optional[str] = None,
        min_score: Optional[int] = None,
        max_score: Optional[int] = None,
        target_name: Optional[str] = None,
        search_term: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0,
        order_by: str = "collected_at",
        order_dir: str = "DESC"
    ) -> List[Dict[str, Any]]:
        """Get posts with optional filtering"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = "SELECT * FROM posts WHERE 1=1"
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)

        if min_score is not None:
            query += " AND misinfo_score >= ?"
            params.append(min_score)

        if max_score is not None:
            query += " AND misinfo_score <= ?"
            params.append(max_score)

        if target_name:
            query += " AND target_name = ?"
            params.append(target_name)

        if search_term:
            query += " AND (text_content LIKE ? OR author LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])

        # Add ordering
        allowed_order_fields = ['collected_at', 'misinfo_score', 'id', 'target_name']
        if order_by in allowed_order_fields:
            query += f" ORDER BY {order_by}"
            if order_dir.upper() in ['ASC', 'DESC']:
                query += f" {order_dir}"

        # Add limit and offset
        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_dict(row) for row in rows]

    def get_posts_count(
        self,
        status: Optional[str] = None,
        min_score: Optional[int] = None,
        max_score: Optional[int] = None
    ) -> int:
        """Get count of posts matching criteria"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM posts WHERE 1=1"
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)

        if min_score is not None:
            query += " AND misinfo_score >= ?"
            params.append(min_score)

        if max_score is not None:
            query += " AND misinfo_score <= ?"
            params.append(max_score)

        cursor.execute(query, params)
        count = cursor.fetchone()[0]
        conn.close()

        return count

    def delete_post(self, post_id: int):
        """Delete a post and its screenshot"""
        post = self.get_post(post_id)
        if post and post.get('screenshot_path'):
            screenshot_file = SCREENSHOTS_DIR / Path(post['screenshot_path']).name
            if screenshot_file.exists():
                screenshot_file.unlink()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        conn.close()

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        # Total posts
        cursor.execute("SELECT COUNT(*) FROM posts")
        stats['total'] = cursor.fetchone()[0]

        # By status
        cursor.execute("""
            SELECT status, COUNT(*) FROM posts GROUP BY status
        """)
        stats['by_status'] = dict(cursor.fetchall())

        # Score distribution
        cursor.execute("""
            SELECT
                COUNT(CASE WHEN misinfo_score >= 70 THEN 1 END) as high,
                COUNT(CASE WHEN misinfo_score >= 40 AND misinfo_score < 70 THEN 1 END) as medium,
                COUNT(CASE WHEN misinfo_score < 40 THEN 1 END) as low,
                COUNT(CASE WHEN misinfo_score IS NULL THEN 1 END) as unscored
            FROM posts
        """)
        row = cursor.fetchone()
        stats['score_distribution'] = {
            'high': row[0],
            'medium': row[1],
            'low': row[2],
            'unscored': row[3]
        }

        conn.close()
        return stats

    def export_to_csv(self, posts: List[Dict[str, Any]], output_path: Path):
        """Export posts to CSV"""
        import csv

        if not posts:
            return

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            # Get all keys from first post
            fieldnames = [
                'id', 'target_name', 'url', 'author', 'post_timestamp',
                'text_content', 'status', 'misinfo_score', 'tags',
                'rationale', 'collected_at'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()

            for post in posts:
                # Flatten JSON fields for CSV
                row = post.copy()
                if isinstance(row.get('tags'), str):
                    try:
                        row['tags'] = ', '.join(json.loads(row['tags']))
                    except:
                        pass
                writer.writerow(row)

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        """Convert SQLite row to dictionary with JSON parsing"""
        data = dict(row)

        # Parse JSON fields
        json_fields = ['tags', 'fact_check_questions', 'drafts']
        for field in json_fields:
            if data.get(field):
                try:
                    data[field] = json.loads(data[field])
                except:
                    pass

        return data


# Singleton instance
_storage = None


def get_storage() -> PostStorage:
    """Get singleton storage instance"""
    global _storage
    if _storage is None:
        _storage = PostStorage()
    return _storage
