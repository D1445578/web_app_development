CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_type TEXT NOT NULL CHECK(item_type IN ('lost', 'found')),
    title TEXT NOT NULL,
    description TEXT,
    location TEXT NOT NULL,
    item_date DATE,
    image_path TEXT,
    contact_info TEXT,
    status TEXT DEFAULT 'open' CHECK(status IN ('open', 'resolved')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
