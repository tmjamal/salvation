"""Test surah template for errors"""
from app import app, db, Surah

def test_surah_template():
    with app.test_request_context():
        try:
            # Get Surah Al-Baqarah
            surah = Surah.query.filter_by(number=2).first()
            
            if surah:
                # Test template rendering
                from flask import render_template
                result = render_template('surah_detail.html', surah=surah)
                print("Template rendered successfully!")
                print("Length of rendered content:", len(result))
                
                # Check for common issues
                if 'surah.verses' in result:
                    print("✓ surah.verses is accessible")
                if 'ആയത്തുകൾ ഇതുവരെ ചേർത്തിട്ടില്ല' in result:
                    print("Still showing 'no verses' message")
                else:
                    print("No 'no verses' message found")
                    
            else:
                print("Surah not found")
                
        except Exception as e:
            print(f"Error rendering template: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_surah_template()
