"""Check database for hit counter models and data"""
from app import app, db

def check_hit_counter():
    with app.app_context():
        print("=== Database Models Check ===")
        
        # Get all table names
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")
        
        # Check for any hit/visit/count related tables
        hit_tables = [t for t in tables if any(keyword in t.lower() for keyword in ['hit', 'visit', 'count', 'stat', 'analytics'])]
        
        if hit_tables:
            print(f"\nFound hit counter related tables: {hit_tables}")
            for table in hit_tables:
                print(f"\n--- Table: {table} ---")
                try:
                    columns = inspector.get_columns(table)
                    for col in columns:
                        print(f"  {col['name']}: {col['type']}")
                    
                    # Check count
                    result = db.session.execute(f"SELECT COUNT(*) FROM {table}")
                    count = result.scalar()
                    print(f"  Total records: {count}")
                    
                except Exception as e:
                    print(f"  Error checking table: {e}")
        else:
            print("\nNo hit counter tables found!")
            print("Available tables:", tables)

if __name__ == '__main__':
    check_hit_counter()
