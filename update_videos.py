from app import app, db, Dialogue

def update_video_urls():
    videos = {
        'യേശു ക്രൂശിക്കപ്പെട്ടോ? - അഹമ്മദ് ദീദാത്ത്': 't60Hms_nUVo',
        'മുഹമ്മദ് നബി ബൈബിളിൽ - അഹമ്മദ് ദീദാത്ത്': 'Yyv4gCO_p2s',
        'ക്രിസ്തു ഇസ്ലാമിൽ - അഹമ്മദ് ദീദാത്ത്': '6fAmsyL_L6I',
        'യേശു ദൈവമാണോ? - ഡോ. സാക്കിർ നായിക്': '2n-S_60V7lA',
        'ഖുർആൻ അല്ലാഹുവിന്റെ വചനമാണോ? - ഡോ. സാക്കിർ നായിക്': '8mG5o6P93fE',
        'ഇസ്ലാം എല്ലാ മാനവരാശിക്കും - ഡോ. സാക്കിർ നായിക്': 'rXAnfA0867k'
    }

    with app.app_context():
        for title, vid in videos.items():
            db.session.query(Dialogue).filter(Dialogue.title_ml == title).update(
                {Dialogue.video_url: f'https://www.youtube.com/watch?v={vid}'}
            )
        db.session.commit()
        print("Updated video URLs successfully.")

if __name__ == "__main__":
    update_video_urls()
