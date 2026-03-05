"""
സ്രഷ്ടാവിന്റെ മാർഗദർശനം - Islamic Malayalam Website
Complete Flask application with admin panel
"""

import os
import json
from datetime import datetime
from functools import wraps

from flask import (Flask, render_template, request, redirect, url_for,
                   flash, jsonify, abort, session)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, UserMixin, login_user, logout_user,
                         login_required, current_user)
from werkzeug.security import generate_password_hash, check_password_hash

# Import configuration
from config import config

# ─── App Configuration ───────────────────────────────────────────────
app = Flask(__name__)

# Get configuration from environment
config_name = os.environ.get('FLASK_ENV', 'production')
app.config.from_object(config[config_name])

# Ensure database path is absolute for production
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'islamic_site.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'


# ═══════════════════════════════════════════════════════════════════════
# DATABASE MODELS
# ═══════════════════════════════════════════════════════════════════════

class AdminUser(UserMixin, db.Model):
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Surah(db.Model):
    __tablename__ = 'surahs'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    name_arabic = db.Column(db.String(100), nullable=False)
    name_malayalam = db.Column(db.String(200), nullable=False)
    name_english = db.Column(db.String(100))
    total_verses = db.Column(db.Integer)
    revelation_type = db.Column(db.String(20))  # Makki/Madani
    summary_ml = db.Column(db.Text)
    verses = db.relationship('Verse', backref='surah', lazy=True,
                             order_by='Verse.verse_number')


class Verse(db.Model):
    __tablename__ = 'verses'
    id = db.Column(db.Integer, primary_key=True)
    surah_id = db.Column(db.Integer, db.ForeignKey('surahs.id'), nullable=False)
    verse_number = db.Column(db.Integer, nullable=False)
    text_arabic = db.Column(db.Text, nullable=False)
    translation_ml = db.Column(db.Text, nullable=False)
    tafsir_ml = db.Column(db.Text)


class HadithCollection(db.Model):
    __tablename__ = 'hadith_collections'
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_ml = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description_ml = db.Column(db.Text)
    icon = db.Column(db.String(10), default='📘')
    hadiths = db.relationship('Hadith', backref='collection', lazy=True)


class Hadith(db.Model):
    __tablename__ = 'hadiths'
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('hadith_collections.id'))
    hadith_number = db.Column(db.Integer)
    narrator_ml = db.Column(db.String(300))
    text_arabic = db.Column(db.Text)
    text_ml = db.Column(db.Text, nullable=False)
    chapter_ml = db.Column(db.String(300))
    grade = db.Column(db.String(50))
    is_featured = db.Column(db.Boolean, default=False)


class Pillar(db.Model):
    __tablename__ = 'pillars'
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(50), nullable=False)
    name_ml = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(10))
    short_desc_ml = db.Column(db.Text)
    full_content_ml = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)


class StoryCategory(db.Model):
    __tablename__ = 'story_categories'
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(50), nullable=False)
    name_ml = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description_ml = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    icon = db.Column(db.String(10))
    stories = db.relationship('Story', backref='category', lazy=True)


class Story(db.Model):
    __tablename__ = 'stories'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('story_categories.id'))
    title_en = db.Column(db.String(200))
    title_ml = db.Column(db.String(400), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    short_desc_ml = db.Column(db.Text)
    full_content_ml = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.Text)  # For YouTube, Instagram, TikTok video links
    image_url = db.Column(db.String(500))  # For story images
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ArticleCategory(db.Model):
    __tablename__ = 'article_categories'
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_ml = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    icon = db.Column(db.String(10))
    articles = db.relationship('Article', backref='category', lazy=True)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('article_categories.id'))
    title_ml = db.Column(db.String(500), nullable=False)
    slug = db.Column(db.String(300), unique=True, nullable=False)
    summary_ml = db.Column(db.Text)
    content_ml = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(200))
    image_url = db.Column(db.String(500))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Fatwa(db.Model):
    __tablename__ = 'fatwas'
    id = db.Column(db.Integer, primary_key=True)
    question_ml = db.Column(db.Text, nullable=False)
    answer_ml = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    scholar = db.Column(db.String(200))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Dialogue(db.Model):
    __tablename__ = 'dialogues'
    id = db.Column(db.Integer, primary_key=True)
    title_ml = db.Column(db.String(500), nullable=False)
    slug = db.Column(db.String(300), unique=True, nullable=False)
    speaker = db.Column(db.String(200))
    description_ml = db.Column(db.Text)
    content_ml = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def video_id(self):
        if not self.video_url:
            return ""
        if "v=" in self.video_url:
            return self.video_url.split("v=")[1].split("&")[0]
        if "youtu.be/" in self.video_url:
            return self.video_url.split("youtu.be/")[1].split("?")[0]
        return ""


class DailyVerse(db.Model):
    __tablename__ = 'daily_verses'
    id = db.Column(db.Integer, primary_key=True)
    verse_arabic = db.Column(db.Text, nullable=False)
    verse_ml = db.Column(db.Text, nullable=False)
    reference = db.Column(db.String(100))
    date = db.Column(db.Date, default=datetime.utcnow)


class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)


class PageHit(db.Model):
    __tablename__ = 'page_hits'
    id = db.Column(db.Integer, primary_key=True)
    page_url = db.Column(db.String(500), nullable=False)
    page_title = db.Column(db.String(200))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    referrer = db.Column(db.String(500))
    visit_date = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(100))
    
    # Indexes for better performance
    __table_args__ = (
        db.Index('idx_page_url', 'page_url'),
        db.Index('idx_visit_date', 'visit_date'),
        db.Index('idx_session_id', 'session_id'),
    )


# ═══════════════════════════════════════════════════════════════════════
# AUTH
# ═══════════════════════════════════════════════════════════════════════

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(AdminUser, int(user_id))


# ═══════════════════════════════════════════════════════════════════════
# PAGE HIT TRACKING
# ═══════════════════════════════════════════════════════════════════════

def track_page_hit(page_url, page_title=None):
    """Track a page visit"""
    try:
        # Don't track admin pages
        if '/admin' in page_url:
            return
            
        # Don't track static files
        if any(ext in page_url for ext in ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico']):
            return
            
        # Get client info
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', ''))
        user_agent = request.environ.get('HTTP_USER_AGENT', '')[:500]  # Limit length
        referrer = request.environ.get('HTTP_REFERER', '')[:500]  # Limit length
        session_id = session.get('_id', 'anonymous')
        
        # Debug logging
        print(f"DEBUG: Tracking hit for {page_url} - {page_title}")
        
        # Create hit record
        hit = PageHit(
            page_url=page_url,
            page_title=page_title,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer,
            session_id=session_id
        )
        
        db.session.add(hit)
        db.session.commit()
        
        print(f"DEBUG: Hit recorded successfully. Total hits: {PageHit.query.count()}")
        
    except Exception as e:
        # Don't let tracking errors break the app
        print(f"Hit tracking error: {e}")
        db.session.rollback()


# ═══════════════════════════════════════════════════════════════════════
# PUBLIC ROUTES
# ═══════════════════════════════════════════════════════════════════════

@app.route('/')
def home():
    import random
    
    # Track page hit
    track_page_hit(request.url, 'ഹോം - സ്രഷ്ടാവിന്റെ മാർഗദർശനം')
    
    # 1. Random Verse from Quran
    random_verse = None
    all_verses_count = Verse.query.count()
    if all_verses_count > 0:
        random_verse = Verse.query.offset(random.randint(0, all_verses_count - 1)).first()
    
    # 2. Random Hadith
    random_hadith = None
    all_hadiths_count = Hadith.query.count()
    if all_hadiths_count > 0:
        random_hadith = Hadith.query.offset(random.randint(0, all_hadiths_count - 1)).first()
    
    # 3. Random Story
    random_story = None
    all_stories_count = Story.query.count()
    if all_stories_count > 0:
        random_story = Story.query.offset(random.randint(0, all_stories_count - 1)).first()
        
    # 4. Random Article
    random_article = None
    all_articles_count = Article.query.count()
    if all_articles_count > 0:
        random_article = Article.query.offset(random.randint(0, all_articles_count - 1)).first()
        
    # 5. Random Dialogue
    random_dialogue = None
    all_dialogues_count = Dialogue.query.count()
    if all_dialogues_count > 0:
        random_dialogue = Dialogue.query.offset(random.randint(0, all_dialogues_count - 1)).first()

    slideshow_items = []
    if random_verse:
        slideshow_items.append({
            'type': 'ഖുർആൻ വചനം',
            'title': f'{random_verse.surah.name_malayalam} ({random_verse.surah.number}:{random_verse.verse_number})',
            'content': random_verse.translation_ml,
            'arabic': random_verse.text_arabic,
            'link': url_for('surah_detail', surah_number=random_verse.surah.number),
            'color': 'emerald'
        })
    if random_hadith:
        slideshow_items.append({
            'type': 'ഹദീസ്',
            'title': random_hadith.collection.name_ml if random_hadith.collection else 'ഹദീസ്',
            'content': random_hadith.text_ml,
            'arabic': random_hadith.text_arabic,
            'link': url_for('hadith_collection', slug=random_hadith.collection.slug) if random_hadith.collection else url_for('hadith'),
            'color': 'sky'
        })
    if random_story:
        slideshow_items.append({
            'type': 'കഥ',
            'title': random_story.title_ml,
            'content': random_story.short_desc_ml or (random_story.full_content_ml[:150] + '...'),
            'link': url_for('story_detail', cat_slug=random_story.category.slug, story_slug=random_story.slug),
            'color': 'amber'
        })
    if random_article:
        slideshow_items.append({
            'type': 'ലേഖനം',
            'title': random_article.title_ml,
            'content': random_article.summary_ml or (random_article.content_ml[:150] + '...'),
            'link': url_for('article_detail', slug=random_article.slug),
            'color': 'slate'
        })
    if random_dialogue:
        slideshow_items.append({
            'type': 'സംവാദം',
            'title': random_dialogue.title_ml,
            'content': random_dialogue.description_ml or 'പ്രമുഖ പണ്ഡിതരുടെ സംവാദങ്ങൾ.',
            'link': url_for('dialogue_detail', slug=random_dialogue.slug),
            'video_id': random_dialogue.video_id,
            'color': 'red'
        })

    random.shuffle(slideshow_items)
    
    # Get total hits for display
    total_hits = PageHit.query.count()
    
    return render_template('home.html',
                           daily_verse=random_verse,
                           slideshow_items=slideshow_items,
                           total_hits=total_hits)


@app.route('/quran')
def quran():
    track_page_hit(request.url, 'ഖുർആൻ - സൂറകളുടെ പട്ടിക')
    surahs = Surah.query.order_by(Surah.number).all()
    return render_template('quran.html', surahs=surahs)


@app.route('/quran/<int:surah_number>')
def surah_detail(surah_number):
    surah = Surah.query.filter_by(number=surah_number).first_or_404()
    track_page_hit(request.url, f'ഖുർആൻ - {surah.name_malayalam}')
    return render_template('surah_detail.html', surah=surah)


@app.route('/hadith')
def hadith():
    track_page_hit(request.url, 'ഹദീസ് - ശേഖരങ്ങൾ')
    collections = HadithCollection.query.all()
    return render_template('hadith.html', collections=collections)


@app.route('/hadith/<slug>')
def hadith_collection(slug):
    collection = HadithCollection.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    hadiths = Hadith.query.filter_by(collection_id=collection.id) \
        .order_by(Hadith.hadith_number).paginate(page=page, per_page=20)
    track_page_hit(request.url, f'ഹദീസ് - {collection.name_ml}')
    return render_template('hadith_collection.html',
                           collection=collection, hadiths=hadiths)


@app.route('/pillars')
def pillars():
    track_page_hit(request.url, 'ഇസ്‌ലാമിക് തൂണുകൾ')
    all_pillars = Pillar.query.order_by(Pillar.order).all()
    return render_template('pillars.html', pillars=all_pillars)


@app.route('/pillars/<slug>')
def pillar_detail(slug):
    pillar = Pillar.query.filter_by(slug=slug).first_or_404()
    track_page_hit(request.url, f'ഇസ്‌ലാമിക് തൂണുകൾ - {pillar.name_ml}')
    return render_template('pillar_detail.html', pillar=pillar)


@app.route('/stories')
def stories():
    track_page_hit(request.url, 'ഇസ്‌ലാമിക് കഥകൾ')
    categories = StoryCategory.query.all()
    return render_template('stories.html', categories=categories)


@app.route('/stories/<slug>')
def story_category(slug):
    category = StoryCategory.query.filter_by(slug=slug).first_or_404()
    all_stories = Story.query.filter_by(category_id=category.id) \
        .order_by(Story.order).all()
    track_page_hit(request.url, f'കഥകൾ - {category.name_ml}')
    return render_template('story_list.html',
                           category=category, stories=all_stories)


@app.route('/stories/<cat_slug>/<story_slug>')
def story_detail(cat_slug, story_slug):
    story = Story.query.filter_by(slug=story_slug).first_or_404()
    track_page_hit(request.url, f'കഥ - {story.title_ml}')
    return render_template('story_detail.html', story=story)


@app.route('/articles')
def articles():
    track_page_hit(request.url, 'ഇസ്‌ലാമിക് ലേഖനങ്ങൾ')
    categories = ArticleCategory.query.all()
    page = request.args.get('page', 1, type=int)
    all_articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('articles.html',
                           categories=categories, articles=all_articles)


@app.route('/articles/category/<slug>')
def articles_by_category(slug):
    category = ArticleCategory.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    cat_articles = Article.query.filter_by(category_id=category.id) \
        .order_by(Article.created_at.desc()).paginate(page=page, per_page=12)
    return render_template('articles_category.html',
                           category=category, articles=cat_articles)


@app.route('/articles/<slug>')
def article_detail(slug):
    article = Article.query.filter_by(slug=slug).first_or_404()
    related = Article.query.filter_by(category_id=article.category_id) \
        .filter(Article.id != article.id).limit(3).all()
    track_page_hit(request.url, f'ലേഖനം - {article.title_ml}')
    return render_template('article_detail.html',
                           article=article, related=related)


@app.route('/fatwa')
def fatwa():
    track_page_hit(request.url, 'ഇസ്‌ലാമിക് ഫത്‌വകൾ')
    page = request.args.get('page', 1, type=int)
    all_fatwas = Fatwa.query.order_by(Fatwa.created_at.desc()) \
        .paginate(page=page, per_page=10)
    return render_template('fatwa.html', fatwas=all_fatwas)


@app.route('/dialogues')
def dialogues():
    track_page_hit(request.url, 'ഇസ്‌ലാമിക് സംവാദങ്ങൾ')
    all_dialogues = Dialogue.query.order_by(Dialogue.created_at.desc()).all()
    return render_template('dialogues.html', dialogues=all_dialogues)


@app.route('/dialogues/<slug>')
def dialogue_detail(slug):
    dialogue = Dialogue.query.filter_by(slug=slug).first_or_404()
    track_page_hit(request.url, f'സംവാദം - {dialogue.title_ml}')
    return render_template('dialogue_detail.html', dialogue=dialogue)


@app.route('/search')
def search():
    track_page_hit(request.url, 'തിരച്ചൽ')
    q = request.args.get('q', '')
    results = {
        'articles': [],
        'stories': [],
        'fatwas': [],
        'hadiths': []
    }
    if q:
        results['articles'] = Article.query.filter(
            Article.title_ml.contains(q) | Article.content_ml.contains(q)
        ).limit(10).all()
        results['stories'] = Story.query.filter(
            Story.title_ml.contains(q) | Story.full_content_ml.contains(q)
        ).limit(10).all()
        results['fatwas'] = Fatwa.query.filter(
            Fatwa.question_ml.contains(q) | Fatwa.answer_ml.contains(q)
        ).limit(10).all()
        results['hadiths'] = Hadith.query.filter(
            Hadith.text_ml.contains(q)
        ).limit(10).all()
    return render_template('search.html', query=q, results=results)


# ═══════════════════════════════════════════════════════════════════════
# ADMIN ROUTES
# ═══════════════════════════════════════════════════════════════════════

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('അസാധുവായ ഉപയോക്തൃനാമമോ പാസ്‌വേഡോ', 'error')
    return render_template('admin/login.html')


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/admin')
@login_required
def admin_dashboard():
    stats = {
        'surahs': Surah.query.count(),
        'verses': Verse.query.count(),
        'hadiths': Hadith.query.count(),
        'stories': Story.query.count(),
        'pillars': Pillar.query.count(),
        'articles': Article.query.count(),
        'fatwas': Fatwa.query.count(),
        'dialogues': Dialogue.query.count(),
        'total_hits': PageHit.query.count(),
        'today_hits': PageHit.query.filter(PageHit.visit_date >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)).count(),
        'unique_visitors': PageHit.query.distinct(PageHit.session_id).count()
    }
    return render_template('admin/dashboard.html', stats=stats)


# ── Admin: Quran Management ──────────────────────────────────────────

@app.route('/admin/surahs')
@login_required
def admin_surahs():
    surahs = Surah.query.order_by(Surah.number).all()
    return render_template('admin/surahs.html', surahs=surahs)


@app.route('/admin/surah/add', methods=['GET', 'POST'])
@login_required
def admin_surah_add():
    if request.method == 'POST':
        surah = Surah(
            number=request.form['number'],
            name_arabic=request.form['name_arabic'],
            name_malayalam=request.form['name_malayalam'],
            name_english=request.form.get('name_english', ''),
            total_verses=request.form.get('total_verses', 0),
            revelation_type=request.form.get('revelation_type', ''),
            summary_ml=request.form.get('summary_ml', '')
        )
        db.session.add(surah)
        db.session.commit()
        flash('സൂറ വിജയകരമായി ചേർത്തു!', 'success')
        return redirect(url_for('admin_surahs'))
    return render_template('admin/surah_form.html', surah=None)


@app.route('/admin/surah/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_surah_edit(id):
    surah = Surah.query.get_or_404(id)
    if request.method == 'POST':
        surah.number = request.form['number']
        surah.name_arabic = request.form['name_arabic']
        surah.name_malayalam = request.form['name_malayalam']
        surah.name_english = request.form.get('name_english', '')
        surah.total_verses = request.form.get('total_verses', 0)
        surah.revelation_type = request.form.get('revelation_type', '')
        surah.summary_ml = request.form.get('summary_ml', '')
        db.session.commit()
        flash('സൂറ അപ്ഡേറ്റ് ചെയ്തു!', 'success')
        return redirect(url_for('admin_surahs'))
    return render_template('admin/surah_form.html', surah=surah)


@app.route('/admin/surah/delete/<int:id>', methods=['POST'])
@login_required
def admin_surah_delete(id):
    surah = Surah.query.get_or_404(id)
    Verse.query.filter_by(surah_id=surah.id).delete()
    db.session.delete(surah)
    db.session.commit()
    flash('സൂറ ഡിലീറ്റ് ചെയ്തു!', 'success')
    return redirect(url_for('admin_surahs'))


@app.route('/admin/surah/<int:surah_id>/verses')
@login_required
def admin_verses(surah_id):
    surah = Surah.query.get_or_404(surah_id)
    verses = Verse.query.filter_by(surah_id=surah_id).order_by(Verse.verse_number).all()
    return render_template('admin/verses.html', surah=surah, verses=verses)


@app.route('/admin/surah/<int:surah_id>/verse/add', methods=['GET', 'POST'])
@login_required
def admin_verse_add(surah_id):
    surah = Surah.query.get_or_404(surah_id)
    if request.method == 'POST':
        verse = Verse(
            surah_id=surah_id,
            verse_number=request.form['verse_number'],
            text_arabic=request.form['text_arabic'],
            translation_ml=request.form['translation_ml'],
            tafsir_ml=request.form.get('tafsir_ml', '')
        )
        db.session.add(verse)
        db.session.commit()
        flash('ആയത്ത് ചേർത്തു!', 'success')
        return redirect(url_for('admin_verses', surah_id=surah_id))
    return render_template('admin/verse_form.html', surah=surah, verse=None)


@app.route('/admin/verse/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_verse_edit(id):
    verse = Verse.query.get_or_404(id)
    if request.method == 'POST':
        verse.verse_number = request.form['verse_number']
        verse.text_arabic = request.form['text_arabic']
        verse.translation_ml = request.form['translation_ml']
        verse.tafsir_ml = request.form.get('tafsir_ml', '')
        db.session.commit()
        flash('ആയത്ത് അപ്ഡേറ്റ് ചെയ്തു!', 'success')
        return redirect(url_for('admin_verses', surah_id=verse.surah_id))
    return render_template('admin/verse_form.html', surah=verse.surah, verse=verse)


@app.route('/admin/verse/delete/<int:id>', methods=['POST'])
@login_required
def admin_verse_delete(id):
    verse = Verse.query.get_or_404(id)
    sid = verse.surah_id
    db.session.delete(verse)
    db.session.commit()
    flash('ആയത്ത് ഡിലീറ്റ് ചെയ്തു!', 'success')
    return redirect(url_for('admin_verses', surah_id=sid))


# ── Admin: Hadith Management ─────────────────────────────────────────

@app.route('/admin/hadith-collections')
@login_required
def admin_hadith_collections():
    collections = HadithCollection.query.all()
    return render_template('admin/hadith_collections.html', collections=collections)


@app.route('/admin/hadith-collection/add', methods=['GET', 'POST'])
@login_required
def admin_hadith_collection_add():
    if request.method == 'POST':
        coll = HadithCollection(
            name_en=request.form['name_en'],
            name_ml=request.form['name_ml'],
            slug=request.form['slug'],
            description_ml=request.form.get('description_ml', ''),
            icon=request.form.get('icon', '📘')
        )
        db.session.add(coll)
        db.session.commit()
        flash('ഹദീസ് ശേഖരം ചേർത്തു!', 'success')
        return redirect(url_for('admin_hadith_collections'))
    return render_template('admin/hadith_collection_form.html', collection=None)


@app.route('/admin/hadith-collection/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_hadith_collection_edit(id):
    coll = HadithCollection.query.get_or_404(id)
    if request.method == 'POST':
        coll.name_en = request.form['name_en']
        coll.name_ml = request.form['name_ml']
        coll.slug = request.form['slug']
        coll.description_ml = request.form.get('description_ml', '')
        coll.icon = request.form.get('icon', '📘')
        db.session.commit()
        flash('ശേഖരം അപ്ഡേറ്റ് ചെയ്തു!', 'success')
        return redirect(url_for('admin_hadith_collections'))
    return render_template('admin/hadith_collection_form.html', collection=coll)


@app.route('/admin/hadith-collection/delete/<int:id>', methods=['POST'])
@login_required
def admin_hadith_collection_delete(id):
    coll = HadithCollection.query.get_or_404(id)
    Hadith.query.filter_by(collection_id=id).delete()
    db.session.delete(coll)
    db.session.commit()
    flash('ശേഖരം ഡിലീറ്റ് ചെയ്തു!', 'success')
    return redirect(url_for('admin_hadith_collections'))


@app.route('/admin/hadith-collection/<int:coll_id>/hadiths')
@login_required
def admin_hadiths(coll_id):
    coll = HadithCollection.query.get_or_404(coll_id)
    page = request.args.get('page', 1, type=int)
    hadiths = Hadith.query.filter_by(collection_id=coll_id) \
        .order_by(Hadith.hadith_number).paginate(page=page, per_page=20)
    return render_template('admin/hadiths.html', collection=coll, hadiths=hadiths)


@app.route('/admin/hadith/add/<int:coll_id>', methods=['GET', 'POST'])
@login_required
def admin_hadith_add(coll_id):
    coll = HadithCollection.query.get_or_404(coll_id)
    if request.method == 'POST':
        h = Hadith(
            collection_id=coll_id,
            hadith_number=request.form.get('hadith_number', 0),
            narrator_ml=request.form.get('narrator_ml', ''),
            text_arabic=request.form.get('text_arabic', ''),
            text_ml=request.form['text_ml'],
            chapter_ml=request.form.get('chapter_ml', ''),
            grade=request.form.get('grade', ''),
            is_featured='is_featured' in request.form
        )
        db.session.add(h)
        db.session.commit()
        flash('ഹദീസ് ചേർത്തു!', 'success')
        return redirect(url_for('admin_hadiths', coll_id=coll_id))
    return render_template('admin/hadith_form.html', collection=coll, hadith=None)


@app.route('/admin/hadith/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_hadith_edit(id):
    h = Hadith.query.get_or_404(id)
    if request.method == 'POST':
        h.hadith_number = request.form.get('hadith_number', 0)
        h.narrator_ml = request.form.get('narrator_ml', '')
        h.text_arabic = request.form.get('text_arabic', '')
        h.text_ml = request.form['text_ml']
        h.chapter_ml = request.form.get('chapter_ml', '')
        h.grade = request.form.get('grade', '')
        h.is_featured = 'is_featured' in request.form
        db.session.commit()
        flash('ഹദീസ് അപ്ഡേറ്റ് ചെയ്തു!', 'success')
        return redirect(url_for('admin_hadiths', coll_id=h.collection_id))
    return render_template('admin/hadith_form.html', collection=h.collection, hadith=h)


@app.route('/admin/hadith/delete/<int:id>', methods=['POST'])
@login_required
def admin_hadith_delete(id):
    h = Hadith.query.get_or_404(id)
    cid = h.collection_id
    db.session.delete(h)
    db.session.commit()
    flash('ഹദീസ് ഡിലീറ്റ് ചെയ്തു!', 'success')
    return redirect(url_for('admin_hadiths', coll_id=cid))


# ── Admin: Pillars Management ────────────────────────────────────────

@app.route('/admin/pillars')
@login_required
def admin_pillars():
    all_pillars = Pillar.query.order_by(Pillar.order).all()
    return render_template('admin/pillars.html', pillars=all_pillars)


@app.route('/admin/pillar/add', methods=['GET', 'POST'])
@login_required
def admin_pillar_add():
    if request.method == 'POST':
        p = Pillar(
            name_en=request.form['name_en'],
            name_ml=request.form['name_ml'],
            slug=request.form['slug'],
            icon=request.form.get('icon', '☪'),
            short_desc_ml=request.form.get('short_desc_ml', ''),
            full_content_ml=request.form.get('full_content_ml', ''),
            order=request.form.get('order', 0)
        )
        db.session.add(p)
        db.session.commit()
        flash('തൂണ്‍ ചേർത്തു!', 'success')
        return redirect(url_for('admin_pillars'))
    return render_template('admin/pillar_form.html', pillar=None)


@app.route('/admin/pillar/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_pillar_edit(id):
    p = Pillar.query.get_or_404(id)
    if request.method == 'POST':
        p.name_en = request.form['name_en']
        p.name_ml = request.form['name_ml']
        p.slug = request.form['slug']
        p.icon = request.form.get('icon', '☪')
        p.short_desc_ml = request.form.get('short_desc_ml', '')
        p.full_content_ml = request.form.get('full_content_ml', '')
        p.order = request.form.get('order', 0)
        db.session.commit()
        flash('തൂണ്‍ അപ്ഡേറ്റ് ചെയ്തു!', 'success')
        return redirect(url_for('admin_pillars'))
    return render_template('admin/pillar_form.html', pillar=p)


@app.route('/admin/pillar/delete/<int:id>', methods=['POST'])
@login_required
def admin_pillar_delete(id):
    p = Pillar.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('തൂണ്‍ ഡിലീറ്റ് ചെയ്തു!', 'success')
    return redirect(url_for('admin_pillars'))


# ── Admin: Story Management ──────────────────────────────────────────

@app.route('/admin/story-categories')
@login_required
def admin_story_categories():
    cats = StoryCategory.query.all()
    return render_template('admin/story_categories.html', categories=cats)


@app.route('/admin/story-category/add', methods=['GET', 'POST'])
@login_required
def admin_story_category_add():
    if request.method == 'POST':
        cat = StoryCategory(
            name_en=request.form['name_en'],
            name_ml=request.form['name_ml'],
            slug=request.form['slug'],
            icon=request.form.get('icon', '📖'),
            description_ml=request.form.get('description_ml', ''),
            image_url=request.form.get('image_url', '')
        )
        db.session.add(cat)
        db.session.commit()
        flash('വിഭാഗം ചേർത്തു!', 'success')
        return redirect(url_for('admin_story_categories'))
    return render_template('admin/story_category_form.html', category=None, categories=StoryCategory.query.all())


@app.route('/admin/story-category/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_story_category_edit(id):
    cat = StoryCategory.query.get_or_404(id)
    if request.method == 'POST':
        cat.name_en = request.form['name_en']
        cat.name_ml = request.form['name_ml']
        cat.slug = request.form['slug']
        cat.icon = request.form.get('icon', '📖')
        cat.description_ml = request.form.get('description_ml', '')
        cat.image_url = request.form.get('image_url', '')
        db.session.commit()
        flash('വിഭാഗം അപ്ഡേറ്റ് ചെയ്തു!', 'success')
        return redirect(url_for('admin_story_categories'))
    return render_template('admin/story_category_form.html', category=cat, categories=StoryCategory.query.all())


@app.route('/admin/story-category/delete/<int:id>', methods=['POST'])
@login_required
def admin_story_category_delete(id):
    cat = StoryCategory.query.get_or_404(id)
    Story.query.filter_by(category_id=id).delete()
    db.session.delete(cat)
    db.session.commit()
    flash('വിഭാഗം ഡിലീറ്റ് ചെയ്തു!', 'success')
    return redirect(url_for('admin_story_categories'))


@app.route('/admin/stories/<int:cat_id>')
@login_required
def admin_stories(cat_id):
    cat = StoryCategory.query.get_or_404(cat_id)
    # Order by order field, but put order=0 items at the end
    all_stories = Story.query.filter_by(category_id=cat_id).order_by(Story.order.asc(), Story.id.asc()).all()
    print(f"DEBUG: Category {cat_id} has {len(all_stories)} stories")
    return render_template('admin/stories.html', category=cat, stories=all_stories)


@app.route('/admin/story/add/<int:cat_id>', methods=['GET', 'POST'])
@login_required
def admin_story_add(cat_id):
    cat = StoryCategory.query.get_or_404(cat_id)
    if request.method == 'POST':
        s = Story(
            category_id=cat_id,
            title_en=request.form.get('title_en', ''),
            title_ml=request.form['title_ml'],
            slug=request.form['slug'],
            short_desc_ml=request.form.get('short_desc_ml', ''),
            full_content_ml=request.form['full_content_ml'],
            video_url=request.form.get('video_url', ''),
            image_url=request.form.get('image_url', ''),
            order=request.form.get('order', 0)
        )
        db.session.add(s)
        db.session.commit()
        flash('കഥ ചേർത്തു!', 'success')
        return redirect(url_for('admin_stories', cat_id=cat_id))
    return render_template('admin/story_form.html', category=cat, story=None, categories=StoryCategory.query.all())


@app.route('/admin/story/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_story_edit(id):
    s = Story.query.get_or_404(id)
    if request.method == 'POST':
        s.title_en = request.form.get('title_en', '')
        s.title_ml = request.form['title_ml']
        s.slug = request.form['slug']
        s.short_desc_ml = request.form.get('short_desc_ml', '')
        s.full_content_ml = request.form['full_content_ml']
        s.video_url = request.form.get('video_url', '')
        s.image_url = request.form.get('image_url', '')
        s.order = request.form.get('order', 0)
        db.session.commit()
        flash('കഥ അപ്ഡേറ്റ് ചെയ്തു!', 'success')
        return redirect(url_for('admin_stories', cat_id=s.category_id))
    return render_template('admin/story_form.html', category=s.category, story=s, categories=StoryCategory.query.all())


@app.route('/admin/story/delete/<int:id>', methods=['POST'])
@login_required
def admin_story_delete(id):
    s = Story.query.get_or_404(id)
    cid = s.category_id
    db.session.delete(s)
    db.session.commit()
    flash('കഥ ഡിലീറ്റ് ചെയ്തു!', 'success')
    return redirect(url_for('admin_stories', cat_id=cid))


# ── Admin: Article Management ────────────────────────────────────────

@app.route('/admin/article-categories')
@login_required
def admin_article_categories():
    cats = ArticleCategory.query.all()
    return render_template('admin/article_categories.html', categories=cats)


@app.route('/admin/article-category/add', methods=['GET', 'POST'])
@login_required
def admin_article_category_add():
    if request.method == 'POST':
        cat = ArticleCategory(
            name_en=request.form['name_en'],
            name_ml=request.form['name_ml'],
            slug=request.form['slug'],
            icon=request.form.get('icon', '📄')
        )
        db.session.add(cat)
        db.session.commit()
        flash('ലേഖന വിഭാഗം ചേർത്തു!', 'success')
        return redirect(url_for('admin_article_categories'))
    return render_template('admin/article_category_form.html', category=None)


@app.route('/admin/article-category/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_article_category_edit(id):
    cat = ArticleCategory.query.get_or_404(id)
    if request.method == 'POST':
        cat.name_en = request.form['name_en']
        cat.name_ml = request.form['name_ml']
        cat.slug = request.form['slug']
        cat.icon = request.form.get('icon', '📄')
        db.session.commit()
        flash('ലേഖന വിഭാഗം അപ്ഡേറ്റ് ചെയ്തു!', 'success')
        return redirect(url_for('admin_article_categories'))
    return render_template('admin/article_category_form.html', category=cat)


@app.route('/admin/article-category/delete/<int:id>', methods=['POST'])
@login_required
def admin_article_category_delete(id):
    cat = ArticleCategory.query.get_or_404(id)
    Article.query.filter_by(category_id=id).delete()
    db.session.delete(cat)
    db.session.commit()
    flash('ലേഖന വിഭാഗം ഡിലീറ്റ് ചെയ്തു!', 'success')
    return redirect(url_for('admin_article_categories'))


@app.route('/admin/articles')
@login_required
def admin_articles():
    page = request.args.get('page', 1, type=int)
    all_articles = Article.query.order_by(Article.created_at.desc()) \
        .paginate(page=page, per_page=20)
    cats = ArticleCategory.query.all()
    return render_template('admin/articles.html',
                           articles=all_articles, categories=cats)


@app.route('/admin/article/add', methods=['GET', 'POST'])
@login_required
def admin_article_add():
    cats = ArticleCategory.query.all()
    if request.method == 'POST':
        a = Article(
            category_id=request.form.get('category_id'),
            title_ml=request.form['title_ml'],
            slug=request.form['slug'],
            summary_ml=request.form.get('summary_ml', ''),
            content_ml=request.form['content_ml'],
            author=request.form.get('author', ''),
            image_url=request.form.get('image_url', ''),
            is_featured='is_featured' in request.form
        )
        db.session.add(a)
        db.session.commit()
        flash('ലേഖനം ചേർത്തു!', 'success')
        return redirect(url_for('admin_articles'))
    return render_template('admin/article_form.html',
                           categories=cats, article=None)


@app.route('/admin/article/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_article_edit(id):
    a = Article.query.get_or_404(id)
    cats = ArticleCategory.query.all()
    if request.method == 'POST':
        a.category_id = request.form.get('category_id')
        a.title_ml = request.form['title_ml']
        a.slug = request.form['slug']
        a.summary_ml = request.form.get('summary_ml', '')
        a.content_ml = request.form['content_ml']
        a.author = request.form.get('author', '')
        a.image_url = request.form.get('image_url', '')
        a.is_featured = 'is_featured' in request.form
        db.session.commit()
        flash('ലേഖനം അപ്ഡേറ്റ് ചെയ്തു!', 'success')
        return redirect(url_for('admin_articles'))
    return render_template('admin/article_form.html',
                           categories=cats, article=a)


@app.route('/admin/article/delete/<int:id>', methods=['POST'])
@login_required
def admin_article_delete(id):
    a = Article.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    flash('ലേഖനം ഡിലീറ്റ് ചെയ്തു!', 'success')
    return redirect(url_for('admin_articles'))


# ── Admin: Fatwa Management ──────────────────────────────────────────

@app.route('/admin/fatwas')
@login_required
def admin_fatwas():
    page = request.args.get('page', 1, type=int)
    all_fatwas = Fatwa.query.order_by(Fatwa.created_at.desc()) \
        .paginate(page=page, per_page=20)
    return render_template('admin/fatwas.html', fatwas=all_fatwas)


@app.route('/admin/fatwa/add', methods=['GET', 'POST'])
@login_required
def admin_fatwa_add():
    if request.method == 'POST':
        f = Fatwa(
            question_ml=request.form['question_ml'],
            answer_ml=request.form['answer_ml'],
            category=request.form.get('category', ''),
            scholar=request.form.get('scholar', ''),
            is_featured='is_featured' in request.form
        )
        db.session.add(f)
        db.session.commit()
        flash('ഫത്‍വ ചേർത്തു!', 'success')
        return redirect(url_for('admin_fatwas'))
    return render_template('admin/fatwa_form.html', fatwa=None)


@app.route('/admin/fatwa/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_fatwa_edit(id):
    f = Fatwa.query.get_or_404(id)
    if request.method == 'POST':
        f.question_ml = request.form['question_ml']
        f.answer_ml = request.form['answer_ml']
        f.category = request.form.get('category', '')
        f.scholar = request.form.get('scholar', '')
        f.is_featured = 'is_featured' in request.form
        db.session.commit()
        flash('ഫത്‍വ അപ്ഡേറ്റ് ചെയ്തു!', 'success')
        return redirect(url_for('admin_fatwas'))
    return render_template('admin/fatwa_form.html', fatwa=f)


@app.route('/admin/fatwa/delete/<int:id>', methods=['POST'])
@login_required
def admin_fatwa_delete(id):
    f = Fatwa.query.get_or_404(id)
    db.session.delete(f)
    db.session.commit()
    flash('ഫത്‍വ ഡിലീറ്റ് ചെയ്തു!', 'success')
    return redirect(url_for('admin_fatwas'))


# ── Admin: Dialogue Management ───────────────────────────────────────

@app.route('/admin/dialogues')
@login_required
def admin_dialogues():
    all_dialogues = Dialogue.query.order_by(Dialogue.created_at.desc()).all()
    return render_template('admin/dialogues.html', dialogues=all_dialogues)


@app.route('/admin/dialogue/add', methods=['GET', 'POST'])
@login_required
def admin_dialogue_add():
    if request.method == 'POST':
        d = Dialogue(
            title_ml=request.form['title_ml'],
            slug=request.form['slug'],
            speaker=request.form.get('speaker', ''),
            description_ml=request.form.get('description_ml', ''),
            content_ml=request.form['content_ml'],
            video_url=request.form.get('video_url', '')
        )
        db.session.add(d)
        db.session.commit()
        flash('സംവാദം ചേർത്തു!', 'success')
        return redirect(url_for('admin_dialogues'))
    return render_template('admin/dialogue_form.html', dialogue=None)


@app.route('/admin/dialogue/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_dialogue_edit(id):
    d = Dialogue.query.get_or_404(id)
    if request.method == 'POST':
        d.title_ml = request.form['title_ml']
        d.slug = request.form['slug']
        d.speaker = request.form.get('speaker', '')
        d.description_ml = request.form.get('description_ml', '')
        d.content_ml = request.form['content_ml']
        d.video_url = request.form.get('video_url', '')
        db.session.commit()
        flash('സംവാദം അപ്ഡേറ്റ് ചെയ്തു!', 'success')
        return redirect(url_for('admin_dialogues'))
    return render_template('admin/dialogue_form.html', dialogue=d)


@app.route('/admin/dialogue/delete/<int:id>', methods=['POST'])
@login_required
def admin_dialogue_delete(id):
    d = Dialogue.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    flash('സംവാദം ഡിലീറ്റ് ചെയ്തു!', 'success')
    return redirect(url_for('admin_dialogues'))


# ── Admin: Daily Verse ────────────────────────────────────────────────

@app.route('/admin/daily-verses')
@login_required
def admin_daily_verses():
    verses = DailyVerse.query.order_by(DailyVerse.id.desc()).all()
    return render_template('admin/daily_verses.html', verses=verses)


@app.route('/admin/daily-verse/add', methods=['GET', 'POST'])
@login_required
def admin_daily_verse_add():
    if request.method == 'POST':
        dv = DailyVerse(
            verse_arabic=request.form['verse_arabic'],
            verse_ml=request.form['verse_ml'],
            reference=request.form.get('reference', '')
        )
        db.session.add(dv)
        db.session.commit()
        flash('ദിവസ വചനം ചേർത്തു!', 'success')
        return redirect(url_for('admin_daily_verses'))
    return render_template('admin/daily_verse_form.html', verse=None)


@app.route('/admin/daily-verse/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_daily_verse_edit(id):
    dv = DailyVerse.query.get_or_404(id)
    if request.method == 'POST':
        dv.verse_arabic = request.form['verse_arabic']
        dv.verse_ml = request.form['verse_ml']
        dv.reference = request.form.get('reference', '')
        db.session.commit()
        flash('ദിവസ വചനം അപ്ഡേറ്റ് ചെയ്തു!', 'success')
        return redirect(url_for('admin_daily_verses'))
    return render_template('admin/daily_verse_form.html', verse=dv)


@app.route('/admin/daily-verse/delete/<int:id>', methods=['POST'])
@login_required
def admin_daily_verse_delete(id):
    dv = DailyVerse.query.get_or_404(id)
    db.session.delete(dv)
    db.session.commit()
    flash('ദിവസ വചനം ഡിലീറ്റ് ചെയ്തു!', 'success')
    return redirect(url_for('admin_daily_verses'))


@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    themes = [
        {'id': 'green-peacock', 'name': 'Green & Peacock Blue'},
        {'id': 'gray-black', 'name': 'Gray & Black'},
        {'id': 'blue-light', 'name': 'Dark Blue & Light Blue'},
        {'id': 'orange-red', 'name': 'Orange & Red'}
    ]
    
    current_theme_setting = SiteSettings.query.filter_by(key='active_theme').first()
    if request.method == 'POST':
        theme_id = request.form.get('theme')
        if not current_theme_setting:
            current_theme_setting = SiteSettings(key='active_theme', value=theme_id)
            db.session.add(current_theme_setting)
        else:
            current_theme_setting.value = theme_id
        db.session.commit()
        flash('സൈറ്റ് ക്രമീകരണങ്ങൾ അപ്ഡേറ്റ് ചെയ്തു!', 'success')
        return redirect(url_for('admin_settings'))
    
    return render_template('admin/settings.html', themes=themes, current_theme=current_theme_setting.value if current_theme_setting else 'green-peacock')


# ═══════════════════════════════════════════════════════════════════════
# TEMPLATE FILTERS
# ═══════════════════════════════════════════════════════════════════════

@app.template_filter('yt_embed')
def yt_embed_filter(url):
    if not url:
        return ""
    if "youtube.com/watch?v=" in url:
        return url.replace("youtube.com/watch?v=", "youtube.com/embed/")
    if "youtu.be/" in url:
        return url.replace("youtu.be/", "youtube.com/embed/")
    return url


# ═══════════════════════════════════════════════════════════════════════
# TEMPLATE CONTEXT
# ═══════════════════════════════════════════════════════════════════════

@app.context_processor
def inject_site_data():
    theme_setting = SiteSettings.query.filter_by(key='active_theme').first()
    active_theme = theme_setting.value if theme_setting else 'green-peacock'
    return {
        'site_name': 'സ്രഷ്ടാവിന്റെ മാർഗദർശനം',
        'site_tagline': 'ഇസ്ലാമിനെക്കുറിച്ച് പഠിക്കാനുള്ള ഒരു വേദിയാണ് ഇത്.',
        'current_year': datetime.now().year,
        'active_theme': active_theme
    }


# ═══════════════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
