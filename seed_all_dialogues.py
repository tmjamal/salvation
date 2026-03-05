from app import app, db, Dialogue

def seed_all():
    data = [
        {
            "title": "Is the Bible God's Word? (Jimmy Swaggart)",
            "title_ml": "ബൈബിൾ ദൈവവചനമാണോ? (ജിമ്മി സ്വാഗാർട്ട്)",
            "speaker": "Ahmed Deedat",
            "video_id": "IlA22NNFlDw",
            "description": "The legendary Baton Rouge debate on the authenticity of the Bible.",
            "description_ml": "ബൈബിളിന്റെ ആധികാരികതയെക്കുറിച്ചുള്ള ഇതിഹാസമായ ബാട്ടൺ റൂഷ് സംവാദം."
        },
        {
            "title": "Is Jesus God? (vs Pastor Stanley)",
            "title_ml": "യേശു ദൈവമാണോ? (പാസ്റ്റർ സ്റ്റാൻലി)",
            "speaker": "Ahmed Deedat",
            "video_id": "QUUOO6mMCaM",
            "description": "A classic debate exploring the divinity of Jesus from different scriptural perspectives.",
            "description_ml": "യേശുവിന്റെ ദൈവത്വത്തെക്കുറിച്ച് വിവിധ തിരുവെഴുത്തുകളുടെ അടിസ്ഥാനത്തിലുള്ള ക്ലാസിക് സംവാദം."
        },
        {
            "title": "Crucifixion or Cruci-fiction? (Full)",
            "title_ml": "ക്രൂശീകരണമോ ക്രൂശീകരണ നാടകമോ? (പൂർണ്ണരൂപം)",
            "speaker": "Ahmed Deedat",
            "video_id": "QCsKW8AAy1U",
            "description": "Deedat's analysis of biblical passages regarding the crucifixion.",
            "description_ml": "ക്രൂശീകരണത്തെക്കുറിച്ചുള്ള ബൈബിൾ ഭാഗങ്ങളെക്കുറിച്ചുള്ള ദീദാത്തിന്റെ വിശകലനം."
        },
        {
            "title": "Bible vs Quran Debate",
            "title_ml": "ബൈബിളും ഖുർആനും - സംവാദം",
            "speaker": "Ahmed Deedat",
            "video_id": "73sYepBrWSs",
            "description": "A deep dive into the historical and contextual differences between the two scriptures.",
            "description_ml": "രണ്ട് വേദഗ്രന്ഥങ്ങൾ തമ്മിലുള്ള ചരിത്രപരവും സന്ദർഭോചിതവുമായ വ്യത്യാസങ്ങളെക്കുറിച്ചുള്ള ആഴത്തിലുള്ള പഠനം."
        },
        {
            "title": "The Greatest Man in History",
            "title_ml": "ചരിത്രത്തിലെ ഏറ്റവും മഹാനായ മനുഷ്യൻ",
            "speaker": "Ahmed Deedat",
            "video_id": "lFOmzPEV6OE",
            "description": "Explaining the impact and character of Prophet Muhammad (PBUH).",
            "description_ml": "മുഹമ്മദ് നബിയുടെ (സ) സ്വാധീനത്തെയും സ്വഭാവത്തെയും കുറിച്ചുള്ള വിശദീകരണം."
        },
        {
            "title": "Dialogue with Christianity",
            "title_ml": "ക്രിസ്തുമതവുമായുള്ള സംവാദം",
            "speaker": "Ahmed Deedat",
            "video_id": "OVJjmj6FPXM",
            "description": "Sheikh Ahmed Deedat engages in an open dialogue about faith and scripture.",
            "description_ml": "വിശ്വാസത്തെയും തിരുവെഴുത്തുകളെയും കുറിച്ച് ശൈഖ് അഹമ്മദ് ദീദാത്ത് നടത്തുന്ന തുറന്ന സംവാദം."
        },
        {
            "title": "Is the Bible the True Word of God?",
            "title_ml": "ബൈബിൾ യഥാർത്ഥ ദൈവവചനമാണോ?",
            "speaker": "Ahmed Deedat",
            "video_id": "JSlXgQxKQ-I",
            "description": "A critical examination of the Bible's textual history.",
            "description_ml": "ബൈബിളിന്റെ പാഠപരമായ ചരിത്രത്തെക്കുറിച്ചുള്ള വിമർശനാത്മകമായ പരിശോധന."
        },
        {
            "title": "What is His Name?",
            "title_ml": "അവന്റെ പേരെന്താണ്?",
            "speaker": "Ahmed Deedat",
            "video_id": "NqG-k5AUwWg",
            "description": "Focusing on the names and attributes of God in various traditions.",
            "description_ml": "വിവിധ പാരമ്പര്യങ്ങളിലെ ദൈവത്തിന്റെ നാമങ്ങളിലും ഗുണവിശേഷങ്ങളിലും ശ്രദ്ധ കേന്ദ്രീകരിക്കുന്നു."
        },
        {
            "title": "Resurrection or Resuscitation?",
            "title_ml": "പുനരുത്ഥാനമോ ബോധക്ഷയമോ?",
            "speaker": "Ahmed Deedat",
            "video_id": "NTRDNxK_Hgw",
            "description": "Debating the historical events surrounding Jesus' departure.",
            "description_ml": "യേശുവിന്റെ വേർപാടുമായി ബന്ധപ്പെട്ട ചരിത്ര സംഭവങ്ങളെക്കുറിച്ചുള്ള സംവാദം."
        },
        {
            "title": "Who Moved the Stone?",
            "title_ml": "ആരാണ് കല്ല് നീക്കിയത്?",
            "speaker": "Ahmed Deedat",
            "video_id": "-FqHtohLdFQ",
            "description": "Analyzing the scriptural accounts of the tomb of Christ.",
            "description_ml": "ക്രിസ്തുവിന്റെ കല്ലറയെക്കുറിച്ചുള്ള തിരുവെഴുത്തുകളിലെ വിവരണങ്ങളുടെ വിശകലനം."
        },
        {
            "title": "Christ in Islam (Sydney)",
            "title_ml": "ക്രിസ്തു ഇസ്ലാമിൽ (സിഡ്‌നി)",
            "speaker": "Ahmed Deedat",
            "video_id": "IE_62654ats",
            "description": "A lecture on the high status of Jesus within Islamic theology.",
            "description_ml": "ഇസ്ലാമിക ദൈവശാസ്ത്രത്തിൽ യേശുവിനുള്ള ഉയർന്ന സ്ഥാനത്തെക്കുറിച്ചുള്ള പ്രഭാഷണം."
        },
        {
            "title": "Does God Exist? (Zakir Naik)",
            "title_ml": "ദൈവം ഉണ്ടോ? (സാക്കിർ നായിക്)",
            "speaker": "Dr. Zakir Naik",
            "video_id": "wc3UkeyXdc0",
            "description": "Proving the existence of the Creator using logic and modern science.",
            "description_ml": "യുക്തിയും ആധുനിക ശാസ്ത്രവും ഉപയോഗിച്ച് സ്രഷ്ടാവിന്റെ നിലനിൽപ്പ് തെളിയിക്കുന്നു."
        },
        {
            "title": "Terrorism and Jihad",
            "title_ml": "ഭീകരവാദവും ജിഹാദും",
            "speaker": "Dr. Zakir Naik",
            "video_id": "nKXX-85kxiE",
            "description": "Clarifying the true concept of Jihad and Islam's stance on violence.",
            "description_ml": "ജിഹാദിന്റെ യഥാർത്ഥ സങ്കല്പവും അക്രമത്തോടുള്ള ഇസ്ലാമിന്റെ നിലപാടും വ്യക്തമാക്കുന്നു."
        },
        {
            "title": "Similarities Between Islam and Christianity",
            "title_ml": "ഇസ്ലാമും ക്രിസ്തുമതവും തമ്മിലുള്ള സാമ്യങ്ങൾ",
            "speaker": "Dr. Zakir Naik",
            "video_id": "_M1PcTlYalk",
            "description": "Building bridges through common values in both religions.",
            "description_ml": "ഇരു മതങ്ങളിലെയും പൊതുവായ മൂല്യങ്ങളിലൂടെ പാലങ്ങൾ നിർമ്മിക്കുന്നു."
        },
        {
            "title": "Quran and Modern Science",
            "title_ml": "ഖുർആനും ആധുനിക ശാസ്ത്രവും",
            "speaker": "Dr. Zakir Naik",
            "video_id": "cPkDQvmDviQ",
            "description": "Demonstrating how the Quran's revelations align with scientific facts.",
            "description_ml": "ഖുർആനിലെ വെളിപ്പെടുത്തലുകൾ ശാസ്ത്രീയ വസ്തുതകളുമായി എങ്ങനെ പൊരുത്തപ്പെടുന്നു എന്ന് തെളിയിക്കുന്നു."
        },
        {
            "title": "Women's Rights in Islam",
            "title_ml": "ഇസ്ലാമിലെ സ്ത്രീകളുടെ അവകാശങ്ങൾ",
            "speaker": "Dr. Zakir Naik",
            "video_id": "TN_7YiNatJc",
            "description": "Addressing misconceptions about the role of women in Islam.",
            "description_ml": "ഇസ്ലാമിലെ സ്ത്രീകളുടെ പങ്കിനെക്കുറിച്ചുള്ള തെറ്റിദ്ധാരണകളെ അഭിസംബോധന ചെയ്യുന്നു."
        },
        {
            "title": "Concept of God in Major Religions",
            "title_ml": "പ്രധാന മതങ്ങളിലെ ദൈവ സങ്കല്പം",
            "speaker": "Dr. Zakir Naik",
            "video_id": "mak96hfgRgo",
            "description": "Comparing the monotheistic concept across different faith systems.",
            "description_ml": "വിവിധ വിശ്വാസ രീതികളിലെ ഏകദൈവ സങ്കല്പത്തെ താരതമ്യം ചെയ്യുന്നു."
        },
        {
            "title": "Universal Brotherhood in Islam",
            "title_ml": "ഇസ്ലാമിലെ സാർവത്രിക സാഹോദര്യം",
            "speaker": "Dr. Zakir Naik",
            "video_id": "H6aK2fe_QXw",
            "description": "Explaining the Islamic vision of equality for all of humanity.",
            "description_ml": "മുഴുവൻ മനുഷ്യവർഗത്തിനും വേണ്ടിയുള്ള ഇസ്ലാമിന്റെ സമത്വ ദർശനം വിവരിക്കുന്നു."
        },
        {
            "title": "Quran - Word of God?",
            "title_ml": "ഖുർആൻ - ദൈവവചനമാണോ?",
            "speaker": "Dr. Zakir Naik",
            "video_id": "eUNjLclhq84",
            "description": "Presenting evidences that the Quran is a divine revelation.",
            "description_ml": "ഖുർആൻ ഒരു ദൈവിക വെളിപാടാണെന്നതിന് തെളിവുകൾ നിരത്തുന്നു."
        },
        {
            "title": "Why I Am a Muslim",
            "title_ml": "ഞാൻ എന്തുകൊണ്ട് മുസ്ലിമായി",
            "speaker": "Dr. Zakir Naik",
            "video_id": "iOTxCtUv6o0",
            "description": "The logic and rationality behind choosing Islam as a path.",
            "description_ml": "ഇസ്ലാം ഒരു പാതയായി തിരഞ്ഞെടുക്കുന്നതിന് പിന്നിലെ യുക്തിയും ബുദ്ധിപരതയും."
        },
        {
            "title": "Islam and the West",
            "title_ml": "ഇസ്ലാമും പാശ്ചാത്യ ലോകവും",
            "speaker": "Dr. Zakir Naik",
            "video_id": "ptFAozgMj60",
            "description": "Dialogue regarding current relations and misunderstandings.",
            "description_ml": "നിലവിലെ ബന്ധങ്ങളെക്കുറിച്ചും തെറ്റിദ്ധാരണകളെക്കുറിച്ചുമുള്ള സംവാദം."
        }
    ]

    with app.app_context():
        # Clear existing dialogues to avoid duplicates and ensure clean list
        db.session.query(Dialogue).delete()
        
        for item in data:
            slug = item["title"].lower().replace('?', '').replace('(', '').replace(')', '').replace(' ', '-').replace('--', '-')
            # Ensure unique slug if needed (though here clean delete handles it)
            
            d = Dialogue(
                title_ml=item["title_ml"],
                slug=slug[:100],
                speaker=item["speaker"],
                description_ml=item["description_ml"],
                content_ml=f"<h2>{item['title_ml']}</h2><p>{item['description_ml']}</p>",
                video_url=f"https://www.youtube.com/watch?v={item['video_id']}"
            )
            db.session.add(d)
        
        db.session.commit()
        print(f"Seeded {len(data)} dialogues successfully.")

if __name__ == "__main__":
    seed_all()
