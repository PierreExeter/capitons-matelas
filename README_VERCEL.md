# Vercel Deployment Guide - Waitress Setup

This guide explains how to deploy the mattress button point calculator on Vercel using Waitress as the production server.

## 🚀 Quick Deploy

### Prerequisites
- Vercel account and CLI installed
- Git repository connected to Vercel

### One-Step Deployment
```bash
# Install Vercel CLI (if not already installed)
npm i -g vercel

# Deploy to Vercel
vercel --prod
```

## 📁 Project Structure

```
├── server.py              # Main Flask app with Waitress
├── templates/
│   └── index.html         # Frontend template
├── vercel.json             # Vercel configuration
└── requirements.txt          # Python dependencies
```

## 🔧 Configuration

### vercel.json
- Routes all requests to `server.py`
- Configures Python 3.9 runtime
- Simple catch-all routing

### server.py
- **Flask app** with production-ready routes
- **Waitress server** for production deployment
- **All endpoints**: /, /calculate, /health
- **Same calculation logic** as original app

## 🧪 Local Testing

### Test Locally with Vercel CLI
```bash
# Install dependencies
pip install -r requirements.txt

# Test with Vercel CLI
vercel dev

# Test endpoints
curl http://localhost:3000/health
curl -X POST http://localhost:3000/calculate \
  -H "Content-Type: application/json" \
  -d '{"x":220,"y":240,"min_dist_x":30,"min_dist_y":40,"edge_distance":15}'
```

### Test Production Server Locally
```bash
# Run with Waitress (production mode)
python server.py

# Test on port 8000
curl http://localhost:8000/health
```

## 🌐 Production Features

### Waitress Benefits
- ✅ **Production WSGI server** - Replaces Flask dev server
- ✅ **Multi-threaded** - Handles concurrent requests
- ✅ **Stable & mature** - Battle-tested WSGI server
- ✅ **Lightweight** - Minimal overhead
- ✅ **Vercel compatible** - Works with serverless

### Vercel Serverless Benefits
- ✅ **Auto-scaling** - Handles traffic spikes automatically
- ✅ **Global CDN** - Edge caching worldwide
- ✅ **Zero maintenance** - No server management needed
- ✅ **Pay-per-execution** - Cost-effective

## 📋 Deployment Process

### Step 1: Prepare Repository
```bash
# Ensure files are committed
git add .
git commit -m "Add Waitress setup for Vercel deployment"
git push
```

### Step 2: Deploy to Vercel
```bash
# Deploy production
vercel --prod

# Follow prompts to link repository
# Deployment completes in 1-2 minutes
```

### Step 3: Verify Deployment
```bash
# Test production URL
curl https://your-app.vercel.app/health
curl https://your-app.vercel.app/
```

## 🔍 Environment Variables (Optional)

For production configuration, set in Vercel dashboard:
- `FLASK_ENV=production`
- `LOG_LEVEL=INFO`
- Custom domain settings
- SSL certificates (automatic)

## 🎯 API Endpoints

All endpoints work identically to original Flask app:

### GET /
Returns the HTML calculator interface

### POST /calculate
```json
{
  "points": [[15.0, 15.0], [45.0, 15.0], ...],
  "rectangle": {"x": 220.0, "y": 240.0}
}
```

### GET /health
```json
{
  "status": "healthy",
  "service": "matelas-calc"
}
```

## 🚨 Troubleshooting

### Common Issues
- **404 errors** - Check `vercel.json` routing
- **Import errors** - Verify `requirements.txt`
- **Timeout** - Check Vercel function logs
- **CORS issues** - Not applicable with single server file

### Debug Commands
```bash
# View deployment logs
vercel logs

# Check build process
vercel build

# Redeploy latest
vercel --prod --force
```

## 🎉 Success!

Your mattress button point calculator is now running on Vercel with:
- Production-ready Waitress server
- Global CDN distribution
- Automatic scaling
- Zero maintenance overhead
- Same functionality as original app

The application maintains all original features while gaining enterprise-grade deployment capabilities.
