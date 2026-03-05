from app import app, db, StoryCategory
with app.app_context():
    for c in StoryCategory.query.all():
        print(f"{c.id}: {c.name_en}")
