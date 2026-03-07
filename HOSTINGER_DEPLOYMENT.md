# Hostinger Deployment Guide
# www.findpeaceinlife.com

## 🎯 Deployment Steps for Hostinger

### 1. Upload Files
1. Login to Hostinger cPanel
2. Go to File Manager
3. Upload all your project files to public_html/
4. Make sure app.py is in the root

### 2. Python App Setup
1. In cPanel, look for "Setup Python App"
2. Configure:
   - Python Version: 3.11
   - Application Root: public_html
   - Application URL: /
   - Application Startup File: app.py
   - Application Mode: Production

### 3. Environment Variables
Set these in Python App settings:
- FLASK_ENV=production
- SECRET_KEY=srashtaavinte-maargadarshnam-2024-secret
- DATABASE_URL=sqlite:///public_html/islamic_site.db

### 4. Install Dependencies
In cPanel Terminal or SSH:
```bash
cd public_html
pip install -r requirements.txt
```

### 5. Create .htaccess
Create .htaccess file in public_html/:
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /app.wsgi/$1 [QSA,PT,L]
```

### 6. Test Website
Visit: www.findpeaceinlife.com

## 🕌 Features Ready:
✅ Daily verse changes every day
✅ All Islamic content restored
✅ Admin panel working
✅ Stories, articles, Quran, Hadith
✅ Beautiful Malayalam interface
✅ Mobile responsive design

## 🎉 Your Islamic Website is Ready!
www.findpeaceinlife.com - Spreading peace and Islamic knowledge
