# Vercel Deployment Instructions

## Files Created for Vercel Deployment

1. **vercel.json** - Vercel configuration file
2. **api/index.py** - Vercel entry point
3. **Updated requirements.txt** - Added psycopg2-binary for PostgreSQL
4. **Updated config.py** - Added VercelConfig class
5. **Updated app.py** - Vercel environment detection

## Environment Variables Needed in Vercel

Set these in your Vercel dashboard:

1. **SECRET_KEY** - Your Flask secret key
2. **DATABASE_URL** - PostgreSQL connection string
3. **FLASK_ENV** - Set to 'production'

## Database Setup

### Option 1: PostgreSQL (Recommended for Vercel)
```
DATABASE_URL=postgresql://username:password@host:port/database
```

### Option 2: SQLite (Not recommended for production)
```
DATABASE_URL=sqlite:///islamic_site.db
```

## Deployment Steps

1. Push all files to your Git repository
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy - Vercel will automatically detect and deploy

## File Structure for Vercel

```
/
├── api/
│   └── index.py          # Vercel entry point
├── templates/
├── static/
├── app.py                  # Main Flask app
├── config.py               # Configuration
├── requirements.txt         # Dependencies
└── vercel.json            # Vercel config
```

## Troubleshooting

If you get "internal error":

1. Check Vercel logs for specific error
2. Verify all environment variables are set
3. Ensure DATABASE_URL is correct format
4. Check that all imports are in requirements.txt

## Notes

- The app.py file now detects Vercel environment automatically
- api/index.py handles Vercel-specific setup
- Database initialization happens through Vercel environment variables
