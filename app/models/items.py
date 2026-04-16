import sqlite3
import os

from flask import current_app

def get_db_connection():
    """
    Establish and return a connection to the SQLite database.
    Assumes the database file is defined in the app configuration via matching instance folder.
    """
    # Fallback to default instance path if current_app is not available (e.g. outside request context)
    db_path = current_app.config.get('DATABASE', os.path.join(current_app.instance_path, 'database.db'))
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # To return dict-like objects
    return conn

def create_item(data):
    """
    Create a new item (lost or found) in the database.
    data requires: item_type, title, location
    optional: description, item_date, image_path, contact_info
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO items (
                item_type, title, description, location, 
                item_date, image_path, contact_info, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('item_type'),
            data.get('title'),
            data.get('description', None),
            data.get('location'),
            data.get('item_date', None),
            data.get('image_path', None),
            data.get('contact_info', None),
            data.get('status', 'open')
        ))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def get_all_items(item_type=None, search_query=None):
    """
    Retrieve all items, with optional filtering by type and search query (matching title or description).
    """
    conn = get_db_connection()
    try:
        query = "SELECT * FROM items WHERE 1=1"
        params = []
        
        if item_type:
            query += " AND item_type = ?"
            params.append(item_type)
            
        if search_query:
            query += " AND (title LIKE ? OR description LIKE ? OR location LIKE ?)"
            like_term = f"%{search_query}%"
            params.extend([like_term, like_term, like_term])
            
        query += " ORDER BY created_at DESC"
        
        items = conn.execute(query, params).fetchall()
        return [dict(ix) for ix in items]
    finally:
        conn.close()

def get_item_by_id(item_id):
    """
    Retrieve a single item by its ID.
    """
    conn = get_db_connection()
    try:
        item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        return dict(item) if item else None
    finally:
        conn.close()

def update_item_status(item_id, status):
    """
    Update the status of an item (e.g., 'open' -> 'resolved')
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE items SET status = ? WHERE id = ?", (status, item_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def delete_item(item_id):
    """
    Delete an item by its ID.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
