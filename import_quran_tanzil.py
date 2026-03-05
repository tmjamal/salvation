"""Import Quran verses from Tanzil.net Malayalam translation"""
import requests
import json
from app import app, db, Surah, Verse

def import_quran_from_tanzil():
    """Import complete Quran with Malayalam translation from Tanzil.net API"""
    
    with app.app_context():
        print("Starting Quran import from Tanzil.net...")
        
        # Tanzil.net API endpoint for Malayalam translation
        # Using the official Malayalam translation (ID: 131)
        api_url = "https://api.quran.com/api/v4/quran/verses/uthmani?translations=131"
        
        try:
            # Get all verses
            response = requests.get(api_url)
            if response.status_code != 200:
                print(f"API request failed: {response.status_code}")
                return False
                
            data = response.json()
            verses = data.get('verses', [])
            
            imported_count = 0
            for verse_data in verses:
                verse_id = verse_data.get('id')
                verse_number = verse_data.get('verse_number')
                chapter_id = verse_data.get('chapter_id')
                
                # Get Arabic text
                text_arabic = verse_data.get('text_uthmani', '')
                
                # Get Malayalam translation
                translations = verse_data.get('translations', [])
                translation_ml = ''
                if translations and len(translations) > 0:
                    translation_ml = translations[0].get('text', '')
                
                # Find the surah in our database
                surah = Surah.query.filter_by(number=chapter_id).first()
                if not surah:
                    print(f"Surah {chapter_id} not found in database")
                    continue
                
                # Check if verse already exists
                existing_verse = Verse.query.filter_by(
                    surah_id=surah.id, 
                    verse_number=verse_number
                ).first()
                
                if existing_verse:
                    # Update existing verse
                    existing_verse.text_arabic = text_arabic
                    existing_verse.translation_ml = translation_ml
                    print(f"Updated verse {chapter_id}:{verse_number}")
                else:
                    # Add new verse
                    new_verse = Verse(
                        surah_id=surah.id,
                        verse_number=verse_number,
                        text_arabic=text_arabic,
                        translation_ml=translation_ml
                    )
                    db.session.add(new_verse)
                    print(f"Added verse {chapter_id}:{verse_number}")
                
                imported_count += 1
                
                # Commit every 50 verses to avoid memory issues
                if imported_count % 50 == 0:
                    db.session.commit()
                    print(f"Progress: {imported_count} verses imported")
            
            # Final commit
            db.session.commit()
            
            print(f"✅ Successfully imported {imported_count} verses!")
            return True
            
        except Exception as e:
            print(f"❌ Error importing Quran: {str(e)}")
            db.session.rollback()
            return False

def import_sample_surahs():
    """Import a few sample Surahs to demonstrate functionality"""
    
    with app.app_context():
        print("Importing sample Surahs (2, 3, 36, 67, 112)...")
        
        # Sample data for key Surahs
        sample_surahs = {
            2: {  # Al-Baqarah - First 5 verses
                "verses": [
                    (1, "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ", "അല്ലാഹുവിന്റെ പേരിൽ, പരമകരുണാധരനായ, അത്യന്തം കരുണാലുവായ"),
                    (2, "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "സ്തുതി ലോകരുടെ നാഥനായ അല്ലാഹുവിനാകുന്നു"),
                    (3, "الرَّحْمَنِ الرَّحِيمِ", "പരമകരുണാധരനും അത്യന്തം കരുണാലുമായ അല്ലാഹുവിന്"),
                    (4, "مَالِكِ يَوْمِ الدِّينِ", "വിധിദിനത്തിന്റെ ഉടമസ്ഥനായ"),
                    (5, "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ", "നിന്നെ മാത്രം ഞങ്ങൾ വണങ്ങുന്നു; നിന്നിൽ നിന്ന് മാത്രം ഞങ്ങൾ സഹായം തേടുന്നു")
                ]
            },
            3: {  # Aal-Imran - First 3 verses
                "verses": [
                    (1, "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ الم", "അല്ലാഹുവിന്റെ പേരിൽ, പരമകരുണാധരനായ, അത്യന്തം കരുണാലുവായ"),
                    (2, "اللَّهُ لَا إِلَهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ", "അല്ലാഹു അല്ലാഹു അല്ലാഹു, അവനൊഴികെ ദൈവമില്ല, അവനാണ് ജീവനും നിലനിൽപ്പും"),
                    (3, "نَزَّلَ عَلَيْكَ الْكِتَابَ بِالْحَقِّ مُصَدِّقًا لِمَا بَيْنَ يَدَيْهِ وَأَنْزَلَ التَّوْرَاةَ وَالْإِنْجِيلَ", "അവൻ നിനക്ക് സത്യത്തോടെ ഗ്രന്ഥം അവതരിപ്പിച്ചു. നിനക്ക് മുമ്പുണ്ടായിരുന്നതിനെ സത്യപ്പെടുത്തുന്നതായിരുന്നു അത്. തൗറാത്ും ഇൻജീലും അവതരിപ്പിച്ചതും അവനാണ്")
                ]
            },
            36: {  # Ya-Sin - First 5 verses
                "verses": [
                    (1, "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ يس", "യാസീൻ"),
                    (2, "وَالْقُرْآنِ الْحَكِيمِ", "തീർച്ചയുള്ള ഖുർആനെ സത്യം"),
                    (3, "إِنَّكَ لَمِنَ الْمُرْسَلِينَ", "തീർച്ചയായും നീ ദൂതന്മാരിൽ പെട്ടവനാകുന്നു"),
                    (4, "عَلَى صِرَاطٍ مُسْتَقِيمٍ", "നേരുള്ള പാതയിൽ"),
                    (5, "تَنْزِيلَ الْعَزِيزِ الرَّحِيمِ", "അതി ശക്തനും കരുണാനിധനുമായ അല്ലാഹുവിന്റെ അവതരണമാകുന്നു")
                ]
            },
            67: {  # Al-Mulk - First 5 verses
                "verses": [
                    (1, "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ تَبَارَكَ الَّذِي بِيَدِهِ الْمُلْكُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ", "ആധിപത്യം അവന്റെ കൈവശമുള്ളവനായ അല്ലാഹുവിനെ അനുഗ്രഹിക്കട്ടെ. എല്ലാത്തിനുമുപരി അവൻ സർവശക്തനാകുന്നു"),
                    (2, "الَّذِي خَلَقَ الْمَوْتَ وَالْحَيَاةَ لِيَبْلُوَكُمْ أَيُّكُمْ أَحْسَنُ عَمَلًا", "മരണത്തെയും ജീവിതത്തെയും അവൻ സൃഷ്ടിച്ചു. നിങ്ങളിൽ ആരാണ് നല്ല പ്രവൃത്തി ചെയ്യുന്നതെന്ന് പരീക്ഷിക്കുന്നതിന് വേണ്ടിയാണത്"),
                    (3, "الَّذِي خَلَقَ سَبْعَ سَمَاوَاتٍ طِبَاقًا وَمَا مَدَرْيَتَ الطَّيْرُ وَهُوَ بِكُلِّ شَيْءٍ عَلِيمٌ", "ഏഴ് അന്തരീക്ഷങ്ങൾ അടുക്കങ്ങളായി അവൻ സൃഷ്ടിച്ചു. പക്ഷികൾക്ക് പറക്കാൻ കഴിയാത്ത ഒന്നുമില്ല. എല്ലാത്തിനെയും അറിയുന്നവനാണ് അവൻ"),
                    (4, "الَّذِي أَدْخَلَ الْجَنَّةَ عَلَى مَنْ شَاءَ مِنْ عِبَادِهِ وَلَقَدْ آتَيْنَا مُوسَى تِسْعَ آيَاتٍ بَيِّنَاتٍ فَاسْأَلْ بَنِي إِسْرَائِيلَ إِذْ جَاءَهُمْ فَقَالَ لَهُ فِرْعَوْنُ إِنِّي لَأَظُنُّكَ يَا مُوسَى مَسْحُورًا", "തന്റെ ദാസന്മാളിൽ ആരെയെങ്കിലും അവൻ സ്വർഗത്തിൽ പ്രവേശിപ്പിച്ചു. മൂസായ്ക്ക് നാം ഒൻപത് വ്യക്തമായ തെളിവുകൾ നൽകിയിട്ടുണ്ട്. അതിനാൽ മൂസാ ഇസ്രായേൽ സന്തതികളോട് ചോദിച്ചു നോക്കൂ. അദ്ദേഹം അവരുടെ അടുത്ത് ചെന്നപ്പോൾ ഫിറവോൺ പറഞ്ഞു: മൂസാ, ഞാൻ കരുതുന്നു നീ മന്ത്രവാസിയാണെന്ന്"),
                    (5, "قَالَ لَقَدْ عَلِمْتَ مَا أَنْزَلَ هَؤُلَاءِ إِلَّا رَبُّ السَّمَاوَاتِ وَالْأَرْضِ بَصَائِرَ وَإِنِّي لَأَظُنُّكَ يَا مُوسَى مَسْحُورًا", "അദ്ദേഹം (മൂസാ) പറഞ്ഞു: നീ നിസ്സാരമായി അറിഞ്ഞിരിക്കുന്നു; ആകാശങ്ങളുടെയും ഭൂമിയുടെയും നാഥൻ മാത്രമേ ഇവയെ അവതരിപ്പിച്ചിട്ടുള്ളൂ. തീർച്ചയായും, ഞാൻ കരുതുന്നു, നീ മന്ത്രവാസിയാണെന്ന്")
                ]
            },
            112: {  # Al-Ikhlas - Complete Surah
                "verses": [
                    (1, "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ قُلْ هُوَ اللَّهُ أَحَدٌ", "പറയുക: അവൻ അല്ലാഹുവാണ്, ഏകൻ"),
                    (2, "اللَّهُ الصَّمَدُ", "അല്ലാഹു എല്ലാം ചെയ്യുന്നവനാകുന്നു"),
                    (3, "لَمْ يَلِدْ وَلَمْ يُولَدْ", "അവൻ ജനിച്ചിട്ടില്ല, ജനിപ്പിച്ചിട്ടുമില്ല"),
                    (4, "وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ", "അവന്ന് തുല്യനായി ആരുമില്ല")
                ]
            }
        }
        
        imported_count = 0
        
        for surah_num, data in sample_surahs.items():
            surah = Surah.query.filter_by(number=surah_num).first()
            if not surah:
                print(f"Surah {surah_num} not found in database")
                continue
                
            print(f"Importing Surah {surah_num}: {surah.name_malayalam}")
            
            for verse_num, arabic, malayalam in data["verses"]:
                # Check if verse already exists
                existing_verse = Verse.query.filter_by(
                    surah_id=surah.id, 
                    verse_number=verse_num
                ).first()
                
                if existing_verse:
                    # Update existing verse
                    existing_verse.text_arabic = arabic
                    existing_verse.translation_ml = malayalam
                    print(f"  Updated verse {verse_num}")
                else:
                    # Add new verse
                    new_verse = Verse(
                        surah_id=surah.id,
                        verse_number=verse_num,
                        text_arabic=arabic,
                        translation_ml=malayalam
                    )
                    db.session.add(new_verse)
                    print(f"  Added verse {verse_num}")
                
                imported_count += 1
            
            # Commit after each Surah
            db.session.commit()
        
        print(f"✅ Successfully imported {imported_count} verses from sample Surahs!")
        return True

if __name__ == '__main__':
    print("Quran Import Options:")
    print("1. Import sample Surahs (quick test)")
    print("2. Import complete Quran from Tanzil.net (may take time)")
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        import_sample_surahs()
    elif choice == "2":
        import_quran_from_tanzil()
    else:
        print("Invalid choice. Running sample import...")
        import_sample_surahs()
