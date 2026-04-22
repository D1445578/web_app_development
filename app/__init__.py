import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_default_secret')
    
    # Ensure instance folder exists for DB
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Set DB path
    app.config['DATABASE'] = os.path.join(app.instance_path, 'database.db')
    
    # Ensure static/uploads exists
    uploads_path = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(uploads_path, exist_ok=True)
    
    # Register blueprints
    from .routes import main, lost, found
    app.register_blueprint(main.bp)
    app.register_blueprint(lost.bp)
    app.register_blueprint(found.bp)
    
    return app

def init_db():
    app = create_app()
    with app.app_context():
        import sqlite3
        db_path = app.config['DATABASE']
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
        if os.path.exists(schema_path):
            conn = sqlite3.connect(db_path)
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()
            conn.close()
            print(f"Database initialized at {db_path}")
        else:
            print("schema.sql not found!")
