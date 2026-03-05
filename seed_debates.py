"""Add more debates of Ahmed Deedat and Dr. Zakir Naik."""
from app import app, db, Dialogue

def add_debates():
    with app.app_context():
        debates = [
            # Dr. Zakir Naik
            {
                "title_ml": "യേശു ദൈവമാണോ? - ഡോ. സാക്കിർ നായിക്",
                "slug": "is-jesus-god-zakir-naik",
                "speaker": "ഡോ. സാക്കിർ നായിക്",
                "description_ml": "യേശുക്രിസ്തുവിന്റെ ദൈവത്വത്തെക്കുറിച്ചുള്ള ഡോ. സാക്കിർ നായിക്കിന്റെ സംവാദം.",
                "content_ml": "<h2>യേശു ദൈവമാണോ?</h2><p>ബൈബിളിന്റെ അടിസ്ഥാനത്തിൽ യേശുക്രിസ്തു താൻ ദൈവമാണെന്ന് ഒരിടത്തും പറഞ്ഞിട്ടില്ലെന്ന് ഡോ. സാക്കിർ നായിക് വിശദീകരിക്കുന്നു.</p>",
                "video_url": "https://www.youtube.com/watch?v=2n-S_60V7lA"
            },
            {
                "title_ml": "ഖുർആൻ അല്ലാഹുവിന്റെ വചനമാണോ? - ഡോ. സാക്കിർ നായിക്",
                "slug": "is-the-quran-gods-word-zakir-naik",
                "speaker": "ഡോ. സാക്കിർ നായിക്",
                "description_ml": "ഖുർആന്റെ ദൈവികതയെക്കുറിച്ചുള്ള പ്രഭാഷണം.",
                "content_ml": "<h2>ഖുർആൻ അല്ലാഹുവിന്റെ വചനമാണോ?</h2><p>ശാസ്ത്രീയ ലക്ഷണങ്ങളുടെയും വെല്ലുവിളികളുടെയും അടിസ്ഥാനത്തിൽ ഖുർആൻ മനുഷ്യനിർമ്മിതമല്ലെന്ന് തെളിയിക്കുന്നു.</p>",
                "video_url": "https://www.youtube.com/watch?v=8mG5o6P93fE"
            },
            {
                "title_ml": "ഇസ്ലാം എല്ലാ മാനവരാശിക്കും - ഡോ. സാക്കിർ നായിക്",
                "slug": "islam-for-all-mankind-zakir-naik",
                "speaker": "ഡോ. സാക്കിർ നായിക്",
                "description_ml": "ഇസ്ലാം ഒരു മതമല്ല, മറിച്ച് ഒരു ജീവിതരീതിയാണെന്ന് വിശദീകരിക്കുന്നു.",
                "content_ml": "<h2>ഇസ്ലാം എല്ലാ മാനവരാശിക്കും</h2><p>ജാതിക്കും മതത്തിനും അതീതമായി ഏകദൈവ വിശ്വാസത്തിന്റെ സന്ദേശം പങ്കുവെക്കുന്നു.</p>",
                "video_url": "https://www.youtube.com/watch?v=rXAnfA0867k"
            },
            # Ahmed Deedat
            {
                "title_ml": "യേശു ക്രൂശിക്കപ്പെട്ടോ? - അഹമ്മദ് ദീദാത്ത്",
                "slug": "was-christ-crucified-ahmed-deedat",
                "speaker": "അഹമ്മദ് ദീദാത്ത്",
                "description_ml": "ക്രൂശീകരണത്തെക്കുറിച്ചുള്ള ക്രിസ്തീയ സഭകളുമായുള്ള സംവാദം.",
                "content_ml": "<h2>യേശു ക്രൂശിക്കപ്പെട്ടോ?</h2><p>ബൈബിൾ വാക്യങ്ങൾ ഉപയോഗിച്ച് ക്രൂശീകരണം നടന്നില്ലെന്ന് അഹമ്മദ് ദീദാത്ത് വാദിക്കുന്നു.</p>",
                "video_url": "https://www.youtube.com/watch?v=nO3S8L96Cyk"
            },
            {
                "title_ml": "മുഹമ്മദ് നബി ബൈബിളിൽ - അഹമ്മദ് ദീദാത്ത്",
                "slug": "muhammad-in-the-bible-ahmed-deedat",
                "speaker": "അഹമ്മദ് ദീദാത്ത്",
                "description_ml": "ബൈബിളിലെ പ്രവചനങ്ങളിൽ മുഹമ്മദ് നബിയെക്കുറിച്ചുള്ള പരാമർശങ്ങൾ.",
                "content_ml": "<h2>മുഹമ്മദ് നബി ബൈബിളിൽ</h2><p>ആവർത്തനപുസ്തകത്തിലെയും മറ്റ് ഭാഗങ്ങളിലെയും പ്രവചനങ്ങൾ ഇസ്ലാമിക പ്രവാചകനിലേക്കാണ് ചൂണ്ടിക്കാണിക്കുന്നതെന്ന് അദ്ദേഹം സമർത്ഥിക്കുന്നു.</p>",
                "video_url": "https://www.youtube.com/watch?v=u1fK-FmY384"
            },
            {
                "title_ml": "ക്രിസ്തു ഇസ്ലാമിൽ - അഹമ്മദ് ദീദാത്ത്",
                "slug": "christ-in-islam-ahmed-deedat",
                "speaker": "അഹമ്മദ് ദീദാത്ത്",
                "description_ml": "ഇസ്ലാം യേശുവിനെ എങ്ങനെ കാണുന്നു എന്നതിനെക്കുറിച്ചുള്ള പ്രഭാഷണം.",
                "content_ml": "<h2>ക്രിസ്തു ഇസ്ലാമിൽ</h2><p>യേശുവിനെ ഒരു പ്രവാചകനായി ഇസ്ലാം ബഹുമാനിക്കുന്നതിനെക്കുറിച്ച് അദ്ദേഹം സംസാരിക്കുന്നു.</p>",
                "video_url": "https://www.youtube.com/watch?v=xV3_tN7K5p8"
            }
        ]
        
        for d in debates:
            if not Dialogue.query.filter_by(slug=d["slug"]).first():
                db.session.add(Dialogue(**d))
        
        db.session.commit()
        print(f"Added {len(debates)} new debates successfully.")

if __name__ == '__main__':
    add_debates()
