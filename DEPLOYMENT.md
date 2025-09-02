# 🚀 Deployment Guide

## Deploy to Streamlit Cloud

### 1. **Prepare Your Repository**
- Push your code to GitHub/GitLab
- Ensure `.streamlit/secrets.toml` is in `.gitignore` (already done)
- Make sure all dependencies are in `requirements.txt`

### 2. **Deploy to Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub/GitLab
3. Click "New app"
4. Select your repository and branch
5. Set the main file path to `app.py`
6. Click "Deploy"

### 3. **Set Up Secrets in Streamlit Cloud**
1. In your deployed app, go to "Settings" → "Secrets"
2. Add your TMDB API key:
```toml
[tmdb]
api_key = "your_actual_api_key_here"
```

### 4. **Get Your Own TMDB API Key**
1. Go to [themoviedb.org](https://www.themoviedb.org)
2. Create an account
3. Go to Settings → API
4. Request an API key
5. Replace the demo key in Streamlit Cloud secrets

### 5. **Environment Variables (Alternative)**
If you prefer environment variables:
```bash
export TMDB_API_KEY="your_api_key_here"
```

## 🔒 Security Notes
- **Never commit API keys to Git**
- Use Streamlit Cloud secrets for production
- The demo key in `secrets.toml` is for development only
- Each deployment environment should have its own API key

## 🌐 Custom Domain (Optional)
- Streamlit Cloud provides free hosting
- You can add custom domains in the settings
- SSL certificates are automatically managed

## 📊 Monitoring
- Check app performance in Streamlit Cloud dashboard
- Monitor API usage for TMDB
- Set up alerts for any errors


