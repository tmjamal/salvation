"""
Bulk import hadiths from the free hadith-api.
Downloads Arabic + English text for all major collections.
Collections: Bukhari, Muslim, Tirmidhi, Nasai, Ibn Majah, Abu Dawud
"""
import json
import urllib.request
import time
import sys

from app import app, db, HadithCollection, Hadith

API_BASE = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions"

COLLECTIONS = [
    {
        "name_en": "Sahih Al-Bukhari",
        "name_ml": "സഹീഹ് അൽ-ബുഖാരി",
        "slug": "bukhari",
        "icon": "📘",
        "desc": "ഇമാം ബുഖാരി (194-256 AH) സമാഹരിച്ച ഏറ്റവും ആധികാരികമായ ഹദീസ് ശേഖരം. 7563 ഹദീസുകൾ.",
        "api_ara": "ara-bukhari",
        "api_eng": "eng-bukhari",
    },
    {
        "name_en": "Sahih Muslim",
        "name_ml": "സഹീഹ് മുസ്‌ലിം",
        "slug": "muslim",
        "icon": "📗",
        "desc": "ഇമാം മുസ്‌ലിം (206-261 AH) സമാഹരിച്ച രണ്ടാമത്തെ ഏറ്റവും ആധികാരിക ഹദീസ് ശേഖരം.",
        "api_ara": "ara-muslim",
        "api_eng": "eng-muslim",
    },
    {
        "name_en": "Jami at-Tirmidhi",
        "name_ml": "ജാമിഅ് അത്-തിർമിദി",
        "slug": "tirmidhi",
        "icon": "📙",
        "desc": "ഇമാം തിർമിദി (209-279 AH) സമാഹരിച്ച ഹദീസ് ശേഖരം. കുതുബ് അസ്-സിത്ത ശേഖരത്തിൽ ഉൾപ്പെടുന്നു.",
        "api_ara": "ara-tirmidhi",
        "api_eng": "eng-tirmidhi",
    },
    {
        "name_en": "Sunan an-Nasai",
        "name_ml": "സുനൻ അന്-നസാഈ",
        "slug": "nasai",
        "icon": "📕",
        "desc": "ഇമാം നസാഈ (215-303 AH) സമാഹരിച്ച ഹദീസ് ശേഖരം. ഫിഖ്ഹ് വിഷയങ്ങളിൽ വിശദമായ ശേഖരം.",
        "api_ara": "ara-nasai",
        "api_eng": "eng-nasai",
    },
    {
        "name_en": "Sunan Ibn Majah",
        "name_ml": "സുനൻ ഇബ്‌ൻ മാജ",
        "slug": "ibnmajah",
        "icon": "📒",
        "desc": "ഇമാം ഇബ്‌ൻ മാജ (209-273 AH) സമാഹരിച്ച ഹദീസ് ശേഖരം. കുതുബ് അസ്-സിത്തയിൽ ഉൾപ്പെടുന്നു.",
        "api_ara": "ara-ibnmajah",
        "api_eng": "eng-ibnmajah",
    },
    {
        "name_en": "Sunan Abu Dawud",
        "name_ml": "സുനൻ അബൂ ദാവൂദ്",
        "slug": "abudawud",
        "icon": "📓",
        "desc": "ഇമാം അബൂ ദാവൂദ് (202-275 AH) സമാഹരിച്ച ഹദീസ് ശേഖരം. ഫിഖ്ഹ് ഹദീസുകളുടെ പ്രധാന ശേഖരം.",
        "api_ara": "ara-abudawud",
        "api_eng": "eng-abudawud",
    },
]


def fetch_json(url):
    """Download JSON from URL with retry."""
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"  Retry {attempt+1}/3: {e}")
            time.sleep(2)
    return None


def import_collection(coll_info):
    """Import a single hadith collection."""
    slug = coll_info["slug"]
    
    # Get or create collection
    collection = HadithCollection.query.filter_by(slug=slug).first()
    if not collection:
        collection = HadithCollection(
            name_en=coll_info["name_en"],
            name_ml=coll_info["name_ml"],
            slug=slug,
            icon=coll_info["icon"],
            description_ml=coll_info["desc"],
        )
        db.session.add(collection)
        db.session.flush()
    else:
        collection.name_ml = coll_info["name_ml"]
        collection.description_ml = coll_info["desc"]
        collection.icon = coll_info["icon"]
    
    # Check existing count
    existing = Hadith.query.filter_by(collection_id=collection.id).count()
    if existing > 100:
        print(f"  {slug}: Already has {existing} hadiths, skipping.")
        return existing
    
    # Delete old sample hadiths
    if existing > 0 and existing < 100:
        Hadith.query.filter_by(collection_id=collection.id).delete()
        db.session.flush()
    
    # Fetch Arabic
    print(f"  Fetching Arabic for {slug}...")
    ara_url = f"{API_BASE}/{coll_info['api_ara']}.min.json"
    ara_data = fetch_json(ara_url)
    if not ara_data:
        print(f"  ERROR: Could not fetch Arabic data for {slug}")
        return 0
    
    # Fetch English
    print(f"  Fetching English for {slug}...")
    eng_url = f"{API_BASE}/{coll_info['api_eng']}.min.json"
    eng_data = fetch_json(eng_url)
    
    # Parse hadiths
    ara_hadiths = ara_data.get("hadiths", [])
    eng_hadiths = eng_data.get("hadiths", []) if eng_data else []
    
    # Build English lookup by hadith number
    eng_lookup = {}
    for eh in eng_hadiths:
        hnum = eh.get("hadithnumber", 0)
        eng_lookup[hnum] = eh.get("text", "")
    
    count = 0
    batch = []
    for h in ara_hadiths:
        hnum = h.get("hadithnumber", 0)
        ara_text = h.get("text", "")
        eng_text = eng_lookup.get(hnum, "")
        
        # Use section info if available
        grades_list = h.get("grades", [])
        grade = ""
        if grades_list:
            grade = grades_list[0].get("grade", "") if isinstance(grades_list[0], dict) else ""
        
        ref = h.get("reference", {})
        chapter = ""
        if isinstance(ref, dict):
            chapter = f"Book {ref.get('book', '')}, Hadith {ref.get('hadith', '')}"
        
        hadith = Hadith(
            collection_id=collection.id,
            hadith_number=hnum,
            text_arabic=ara_text,
            text_ml=eng_text,  # English for now, admin can translate
            grade=grade,
            chapter_ml=chapter,
        )
        batch.append(hadith)
        count += 1
        
        # Commit in batches of 500
        if len(batch) >= 500:
            db.session.bulk_save_objects(batch)
            db.session.flush()
            batch = []
            print(f"    Imported {count} hadiths...")
    
    # Final batch
    if batch:
        db.session.bulk_save_objects(batch)
        db.session.flush()
    
    db.session.commit()
    print(f"  {slug}: Imported {count} hadiths total.")
    return count


def main():
    with app.app_context():
        total = 0
        for coll in COLLECTIONS:
            print(f"\n{'='*50}")
            print(f"Importing: {coll['name_en']} ({coll['name_ml']})")
            print(f"{'='*50}")
            n = import_collection(coll)
            total += n
        
        print(f"\n{'='*50}")
        print(f"GRAND TOTAL: {total} hadiths imported")
        print(f"Collections: {HadithCollection.query.count()}")
        print(f"{'='*50}")


if __name__ == "__main__":
    main()
