"""Add image_url column to articles table"""
from app import app, db
from sqlalchemy import text

def add_image_url_column():
    with app.app_context():
        # Add image_url column to articles table
        try:
            db.session.execute(text("""
                ALTER TABLE articles 
                ADD COLUMN image_url VARCHAR(500)
            """))
            db.session.commit()
            print("Successfully added image_url column!")
        except Exception as e:
            if "duplicate column name" in str(e):
                print("image_url column already exists!")
            else:
                print(f"Error adding column: {e}")
                db.session.rollback()

if __name__ == '__main__':
    add_image_url_column()
