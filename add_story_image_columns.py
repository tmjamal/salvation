"""Add image_url columns to story tables"""
from app import app, db
from sqlalchemy import text

def add_story_image_columns():
    with app.app_context():
        # Add image_url column to story_categories table
        try:
            db.session.execute(text("""
                ALTER TABLE story_categories 
                ADD COLUMN image_url VARCHAR(500)
            """))
            db.session.commit()
            print("Successfully added image_url column to story_categories!")
        except Exception as e:
            if "duplicate column name" in str(e):
                print("image_url column already exists in story_categories!")
            else:
                print(f"Error adding column to story_categories: {e}")
                db.session.rollback()
        
        # Add image_url column to stories table
        try:
            db.session.execute(text("""
                ALTER TABLE stories 
                ADD COLUMN image_url VARCHAR(500)
            """))
            db.session.commit()
            print("Successfully added image_url column to stories!")
        except Exception as e:
            if "duplicate column name" in str(e):
                print("image_url column already exists in stories!")
            else:
                print(f"Error adding column to stories: {e}")
                db.session.rollback()

if __name__ == '__main__':
    add_story_image_columns()
