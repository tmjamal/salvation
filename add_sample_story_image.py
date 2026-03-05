"""Add sample story with image"""
from app import app, db, Story, StoryCategory

def add_sample_story_with_image():
    with app.app_context():
        # Get or create a story category
        category = StoryCategory.query.filter_by(slug='islamic-stories').first()
        if not category:
            category = StoryCategory(
                name_en='Islamic Stories',
                name_ml='ഇസ്ലാമിക കഥകൾ',
                slug='islamic-stories',
                description_ml='ഇസ്ലാമിക കഥകളും ശേഷങ്ങൾ',
                image_url='https://images.unsplash.com/photo-1542816871-8f6f4b6c6c0b5d.jpg',
                icon='🕌'
            )
            db.session.add(category)
            db.session.commit()
            print("Created Islamic Stories category")
        
        # Add a sample story with image
        story = Story(
            category_id=category.id,
            title_en='The Power of Prayer',
            title_ml='പ്രാർത്തിന്റെ ശക്ഷം',
            slug='power-of-prayer',
            short_desc_ml='പ്രാർത്തിന്റെ ശക്ഷത്തിന്റെ ഉറപ്പം',
            full_content_ml='<h2>പ്രാർത്തിന്റെ ശക്ഷം</h2><p>പ്രാർത്തിന്റെ എന്ന്ന്തിന്റെ മഹാനായും ഏറ്റാതിയുന്റെ. അല്ലാതിന്റെ പ്രാർത്തിന്റെ ചെയ്യുകയാൻ നിന്ന്ന്ന്നും നിന്ന്ന്നും പ്രാർത്തിന്റെ ഉറപ്പം.</p>',
            video_url='https://www.youtube.com/watch?v=example',
            image_url='https://images.unsplash.com/photo-1542816871-8f6f4b6c6c0b5d.jpg',
            order=1
        )
        db.session.add(story)
        db.session.commit()
        print("Added sample story with image!")

if __name__ == '__main__':
    add_sample_story_with_image()
