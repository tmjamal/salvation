"""Test template rendering"""
from app import app
from flask import render_template

def test_template():
    with app.app_context():
        try:
            # Test with empty slideshow items
            result = render_template('home.html', slideshow_items=[])
            print("Template rendered successfully with empty items")
            print(f"Length: {len(result)}")
            
            # Test with sample items
            sample_items = [
                {'type': 'Test', 'title': 'Test Title', 'content': 'Test Content', 'color': 'emerald'}
            ]
            result2 = render_template('home.html', slideshow_items=sample_items)
            print("Template rendered successfully with sample items")
            print(f"Length: {len(result2)}")
            
        except Exception as e:
            print(f"Template error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_template()
