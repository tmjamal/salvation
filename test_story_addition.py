"""Test story addition"""
from app import app, db, Story, StoryCategory

def test_story_addition():
    with app.app_context():
        print("=== Story Addition Test ===")
        
        # Check existing categories
        categories = StoryCategory.query.all()
        print(f"Found {len(categories)} story categories:")
        for cat in categories:
            print(f"  - Category ID: {cat.id}")
        
        # Check existing stories
        stories = Story.query.all()
        print(f"\nFound {len(stories)} stories total")
        
        # Check stories by category
        for cat in categories:
            cat_stories = Story.query.filter_by(category_id=cat.id).all()
            print(f"  Category {cat.id}: {len(cat_stories)} stories")
            for story in cat_stories:
                print(f"    - Story ID: {story.id}, Order: {story.order}")

if __name__ == '__main__':
    test_story_addition()
