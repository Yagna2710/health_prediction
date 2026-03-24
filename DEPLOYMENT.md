# Complete Deployment Guide

This guide walks you through deploying the Health Prediction application using GitHub, Render (backend), and Vercel (frontend).

## Prerequisites

- GitHub account
- Render account (https://render.com - sign up with GitHub)
- Vercel account (https://vercel.com - sign up with GitHub)
- Git installed on your local machine

---

## Part 1: Push Code to GitHub

### Step 1: Create GitHub Repository

1. Go to https://github.com and log in
2. Click the "+" icon in the top right → "New repository"
3. Fill in repository details:
   - **Repository name**: `health-prediction-app` (or your choice)
   - **Description**: "AI-powered health prediction and recommendation system"
   - **Visibility**: Public or Private (both work with Render and Vercel)
4. **Do NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

### Step 2: Initialize Git and Push Code

Open your terminal in the project root directory and run:

```bash
# Initialize git repository (if not already initialized)
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit: Health prediction application"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/health-prediction-app.git

# Push to GitHub
git push -u origin main
```

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username.

If you get an error about branch name, try:
```bash
git branch -M main
git push -u origin main
```

### Step 3: Verify Upload

1. Go to your GitHub repository URL
2. Verify that both `backend/` and `frontend/` folders are visible
3. Check that all files are present

---

## Part 2: Deploy Backend to Render

### Step 1: Sign Up and Connect GitHub

1. Go to https://dashboard.render.com/
2. Click "Get Started" or "Sign Up"
3. Choose "Sign up with GitHub"
4. Authorize Render to access your GitHub account

### Step 2: Create New Web Service

1. In Render dashboard, click "New +" button (top right)
2. Select "Web Service"
3. Click "Connect" next to your GitHub repository
   - If you don't see it, click "Configure account" to grant access
4. Select your `health-prediction-app` repository

### Step 3: Configure Web Service

Fill in the following settings:

**Basic Settings:**
- **Name**: `health-prediction-backend` (or your choice)
- **Region**: Choose closest to your users (e.g., Oregon, Frankfurt)
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

**Instance Type:**
- Select "Free" (for testing) or "Starter" (for production)
- Note: Free tier may sleep after inactivity

### Step 4: Add Environment Variables

Scroll down to "Environment Variables" section and add:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `PORT` | `10000` |
| `CORS_ORIGINS` | `*` (temporary - we'll update this later) |

### Step 5: Deploy Backend

1. Click "Create Web Service" button at the bottom
2. Wait for deployment to complete (5-10 minutes)
3. Watch the logs for any errors
4. Once deployed, you'll see "Your service is live 🎉"

### Step 6: Copy Backend URL

1. At the top of the page, you'll see your service URL
2. It will look like: `https://health-prediction-backend.onrender.com`
3. **Copy this URL** - you'll need it for frontend deployment
4. Test it by visiting: `https://your-backend-url.onrender.com/health` (should return "Health Prediction API is running")

---

## Part 3: Deploy Frontend to Vercel

### Step 1: Sign Up and Connect GitHub

1. Go to https://vercel.com/
2. Click "Sign Up" or "Log In"
3. Choose "Continue with GitHub"
4. Authorize Vercel to access your GitHub account

### Step 2: Import Project

1. In Vercel dashboard, click "Add New..." → "Project"
2. You'll see a list of your GitHub repositories
3. Find `health-prediction-app` and click "Import"

### Step 3: Configure Project Settings

Vercel will auto-detect the Vite configuration. Configure:

**Project Settings:**
- **Framework Preset**: Vite (auto-detected)
- **Root Directory**: Click "Edit" and select `frontend`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `dist` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

### Step 4: Add Environment Variables

Before deploying, click "Environment Variables" and add:

| Name | Value |
|------|-------|
| `VITE_API_BASE_URL` | `https://your-backend-url.onrender.com` |

**Important**: Replace `your-backend-url.onrender.com` with the actual Render URL you copied earlier.

### Step 5: Deploy Frontend

1. Click "Deploy" button
2. Wait for deployment to complete (2-5 minutes)
3. Watch the build logs for any errors
4. Once deployed, you'll see "Congratulations!" with your live URL

### Step 6: Copy Frontend URL

1. Your frontend URL will look like: `https://health-prediction-app.vercel.app`
2. **Copy this URL** - you need to update backend CORS settings

---

## Part 4: Update Backend CORS Settings

Now that frontend is deployed, update the backend to allow requests from your Vercel domain.

### Step 1: Update Render Environment Variables

1. Go back to Render dashboard: https://dashboard.render.com/
2. Click on your `health-prediction-backend` service
3. Click "Environment" in the left sidebar
4. Find the `CORS_ORIGINS` variable
5. Click "Edit" and update the value to your Vercel URL:
   ```
   https://your-app.vercel.app
   ```
6. Click "Save Changes"

### Step 2: Redeploy Backend

1. The service will automatically redeploy with new environment variables
2. Wait for redeployment to complete (2-3 minutes)
3. Check logs to ensure no errors

---

## Part 5: Test Your Deployment

### Step 1: Test Backend API

1. Open your browser and visit: `https://your-backend-url.onrender.com/health`
2. You should see: `{"message": "Health Prediction API is running", "status": "ok"}`

### Step 2: Test Frontend Application

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Fill out the health profile form with test data:
   - Age: 45
   - Gender: Male
   - BMI: 28.5
   - Blood Pressure: 130/85
   - Cholesterol: 220
   - Glucose: 110
   - Smoking: No
   - Physical Activity: Moderate
3. Click "Generate Prediction"
4. Verify that predictions and recommendations load correctly

### Step 3: Check Browser Console

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for any errors (especially CORS or network errors)
4. If you see errors, review the troubleshooting section below

---

## Part 6: Troubleshooting Common Issues

### Issue 1: CORS Errors

**Symptoms:**
- Browser console shows: "Access to fetch has been blocked by CORS policy"
- Frontend can't connect to backend

**Solutions:**
1. Verify `CORS_ORIGINS` in Render matches your Vercel URL exactly
2. Ensure no trailing slashes in URLs
3. Check that Render service redeployed after changing environment variables
4. Try setting `CORS_ORIGINS` to `*` temporarily to test (not recommended for production)

### Issue 2: Backend Not Responding (503 Error)

**Symptoms:**
- API requests timeout or return 503 errors
- Backend URL shows "Service Unavailable"

**Solutions:**
1. **Free tier sleeping**: Render free tier sleeps after 15 minutes of inactivity
   - First request may take 30-60 seconds to wake up
   - Consider upgrading to paid tier for production
2. Check Render logs for errors:
   - Go to Render dashboard → Your service → Logs
3. Verify `gunicorn` is starting correctly
4. Check that `runtime.txt` specifies compatible Python version

### Issue 3: Frontend Build Fails on Vercel

**Symptoms:**
- Vercel deployment fails during build
- Error messages about missing dependencies

**Solutions:**
1. Check Node.js version compatibility:
   - Add `engines` field to `package.json` if needed
2. Verify all dependencies are in `package.json`
3. Clear Vercel cache:
   - Go to Project Settings → General → Clear Cache
   - Redeploy
4. Check build logs for specific error messages

### Issue 4: Environment Variables Not Working

**Symptoms:**
- Frontend shows "undefined" for API URL
- Backend can't read environment variables

**Solutions:**

**Frontend (Vercel):**
1. Ensure variable name starts with `VITE_`
2. Redeploy after adding environment variables
3. Check that variables are set for "Production" environment
4. Verify in browser console: `import.meta.env.VITE_API_BASE_URL`

**Backend (Render):**
1. Verify variables are saved in Render dashboard
2. Wait for automatic redeployment after changes
3. Check logs to see if variables are loaded

### Issue 5: Model Files Not Loading

**Symptoms:**
- Backend returns 500 errors
- Logs show "FileNotFoundError" for `.pkl` files

**Solutions:**
1. Verify model files are committed to GitHub:
   ```bash
   git add backend/*.pkl
   git commit -m "Add model files"
   git push
   ```
2. Check that files aren't in `.gitignore`
3. Ensure files are in the `backend/` directory
4. Redeploy on Render after pushing files

### Issue 6: API Returns 404 for All Routes

**Symptoms:**
- All API endpoints return 404
- Only root URL works

**Solutions:**
1. Check `app.py` has all route definitions
2. Verify Flask app is running correctly in logs
3. Test routes locally first
4. Check that `gunicorn app:app` points to correct Flask app

---

## Part 7: Continuous Deployment (Auto-Deploy on Git Push)

Both Render and Vercel support automatic deployments when you push to GitHub.

### Enable Auto-Deploy on Render

1. Go to Render dashboard → Your service
2. Click "Settings" in left sidebar
3. Under "Build & Deploy", ensure "Auto-Deploy" is set to "Yes"
4. Select branch to deploy (usually `main`)
5. Now every push to `main` will trigger a new deployment

### Enable Auto-Deploy on Vercel

1. Vercel enables this by default
2. Every push to `main` triggers a production deployment
3. Pushes to other branches create preview deployments
4. You can configure this in Project Settings → Git

### Making Updates

To update your deployed application:

```bash
# Make your changes to code
git add .
git commit -m "Description of changes"
git push origin main
```

Both services will automatically detect the push and redeploy.

---

## Part 8: Monitoring and Logs

### Viewing Render Logs

1. Go to Render dashboard
2. Click on your service
3. Click "Logs" in left sidebar
4. View real-time logs of your application
5. Use search to filter specific errors

### Viewing Vercel Logs

1. Go to Vercel dashboard
2. Click on your project
3. Click on a deployment
4. Click "Functions" or "Build Logs" tab
5. View deployment and runtime logs

### Setting Up Alerts

**Render:**
- Go to Service Settings → Notifications
- Add email or Slack notifications for deployment failures

**Vercel:**
- Go to Project Settings → Notifications
- Configure deployment notifications

---

## Part 9: Custom Domains (Optional)

### Adding Custom Domain to Vercel

1. Go to Project Settings → Domains
2. Click "Add Domain"
3. Enter your domain (e.g., `healthpredict.com`)
4. Follow DNS configuration instructions
5. Vercel provides automatic HTTPS

### Adding Custom Domain to Render

1. Go to Service Settings → Custom Domain
2. Click "Add Custom Domain"
3. Enter your domain (e.g., `api.healthpredict.com`)
4. Update DNS records as instructed
5. Render provides automatic HTTPS

**Note**: Update `CORS_ORIGINS` and `VITE_API_BASE_URL` after adding custom domains.

---

## Part 10: Local Development Setup

### Backend Local Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "FLASK_ENV=development" > .env.local
echo "CORS_ORIGINS=http://localhost:5173" >> .env.local

# Run development server
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Local Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_BASE_URL=http://localhost:5000" > .env.local

# Run development server
npm run dev
```

Frontend will run on `http://localhost:5173`

---

## Quick Reference

### Your Deployment URLs

After completing deployment, document your URLs here:

- **Frontend (Vercel)**: `https://_____.vercel.app`
- **Backend (Render)**: `https://_____.onrender.com`
- **GitHub Repository**: `https://github.com/_____/_____`

### Important Commands

```bash
# Push updates to GitHub
git add .
git commit -m "Your message"
git push origin main

# View Render logs
# Visit: https://dashboard.render.com → Your Service → Logs

# View Vercel logs
# Visit: https://vercel.com → Your Project → Deployments

# Redeploy manually on Render
# Dashboard → Your Service → Manual Deploy → Deploy latest commit

# Redeploy manually on Vercel
# Dashboard → Your Project → Deployments → Redeploy
```

### Environment Variables Summary

**Render (Backend):**
- `FLASK_ENV=production`
- `PORT=10000`
- `CORS_ORIGINS=https://your-app.vercel.app`

**Vercel (Frontend):**
- `VITE_API_BASE_URL=https://your-backend.onrender.com`

---

## Support and Resources

- **Render Documentation**: https://render.com/docs
- **Vercel Documentation**: https://vercel.com/docs
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Vite Documentation**: https://vitejs.dev/

---

## Security Best Practices

1. **Never commit sensitive data** to GitHub (API keys, passwords)
2. **Use environment variables** for all configuration
3. **Keep dependencies updated** regularly
4. **Enable HTTPS** (automatic on Render and Vercel)
5. **Restrict CORS** to specific domains in production
6. **Monitor logs** regularly for suspicious activity
7. **Use strong passwords** for all accounts

---

**Deployment Complete!** 🎉

Your Health Prediction application is now live and accessible worldwide.
