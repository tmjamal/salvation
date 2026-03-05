"""Create PageHit table for hit counter"""
from app import app, db

def create_hit_counter_table():
    with app.app_context():
        print("Creating PageHit table...")
        try:
            # Create the table
            db.create_all()
            print("PageHit table created successfully!")
            
            # Check if table exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'page_hits' in tables:
                print("PageHit table exists in database")
                
                # Get table info
                columns = inspector.get_columns('page_hits')
                print("Table structure:")
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")
            else:
                print("PageHit table not found")
                
        except Exception as e:
            print(f"Error creating table: {e}")

if __name__ == '__main__':
    create_hit_counter_table()
