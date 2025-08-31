import json
import sqlite3
from datetime import datetime
from pathlib import Path
from config import DATA_DIR

class LocalDatabase:
    """Simple local database for MVP using SQLite"""
    
    def __init__(self):
        self.db_path = DATA_DIR / "corpus.db"
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Contributions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contributions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                category TEXT NOT NULL,
                media_type TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                language TEXT NOT NULL,
                file_path TEXT,
                file_hash TEXT,
                file_size INTEGER,
                is_public BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, user_id, email, name, password_hash):
        """Create new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (id, email, name, password_hash) VALUES (?, ?, ?, ?)",
                (user_id, email, name, password_hash)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_user_by_email(self, email):
        """Get user by email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'email': user[1],
                'name': user[2],
                'password_hash': user[3],
                'created_at': user[4]
            }
        return None
    
    def create_contribution(self, contribution_data):
        """Create new contribution"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO contributions 
            (id, user_id, category, media_type, title, description, language, 
             file_path, file_hash, file_size, is_public)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            contribution_data['id'],
            contribution_data['user_id'],
            contribution_data['category'],
            contribution_data['media_type'],
            contribution_data['title'],
            contribution_data.get('description', ''),
            contribution_data['language'],
            contribution_data.get('file_path', ''),
            contribution_data.get('file_hash', ''),
            contribution_data.get('file_size', 0),
            contribution_data.get('is_public', False)
        ))
        
        conn.commit()
        conn.close()
    
    def get_user_contributions(self, user_id):
        """Get all contributions by user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM contributions WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        contributions = cursor.fetchall()
        conn.close()
        
        return [self._contribution_to_dict(c) for c in contributions]
    
    def get_public_contributions(self, category=None, media_type=None, language=None):
        """Get public contributions with optional filters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM contributions WHERE is_public = TRUE"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        if media_type:
            query += " AND media_type = ?"
            params.append(media_type)
        if language:
            query += " AND language = ?"
            params.append(language)
        
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        contributions = cursor.fetchall()
        conn.close()
        
        return [self._contribution_to_dict(c) for c in contributions]
    
    def _contribution_to_dict(self, contribution):
        """Convert contribution tuple to dictionary"""
        return {
            'id': contribution[0],
            'user_id': contribution[1],
            'category': contribution[2],
            'media_type': contribution[3],
            'title': contribution[4],
            'description': contribution[5],
            'language': contribution[6],
            'file_path': contribution[7],
            'file_hash': contribution[8],
            'file_size': contribution[9],
            'is_public': bool(contribution[10]),
            'created_at': contribution[11]
        }

# Global database instance
db = LocalDatabase()