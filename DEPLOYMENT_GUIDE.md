# Phase II Deployment Guide - Full Stack

**Stack**: Next.js 16+ (Vercel) + FastAPI (Railway) + PostgreSQL (Neon)

This guide walks you through deploying the complete application with all features working.

---

## 📋 Deployment Checklist

### Part 1: Database Setup (Neon PostgreSQL) - 5 minutes

### Part 2: Backend Deployment (Railway) - 10 minutes

### Part 3: Frontend Deployment (Vercel) - 5 minutes

**Total Time**: ~20 minutes

---

## 🗄️ Part 1: Setup Neon PostgreSQL Database

### Step 1: Create Neon Account

1. Go to https://neon.tech
2. Click "Sign Up" (use GitHub or email)
3. Verify your email if required

### Step 2: Create a New Project

1. Click "Create Project"
2. **Project Name**: `todo-app-phase2`
3. **Region**: Choose closest to you (e.g., US East, EU West)
4. **PostgreSQL Version**: 16 (default)
5. Click "Create Project"

### Step 3: Get Database Connection String

1. After project creation, you'll see the connection details
2. Copy the **Connection String** (looks like this):
   ```
   postgresql://username:password@ep-xxx.neon.tech/neondb?sslmode=require
   ```
3. **Save this!** You'll need it for backend deployment

### Step 4: Note Down Credentials

You'll see:
- **Host**: `ep-xxx.neon.tech`
- **Database**: `neondb`
- **User**: `username`
- **Password**: `xxxxx`

**Keep these safe!**

---

## 🚂 Part 2: Deploy Backend to Railway

### Step 1: Create Railway Account

1. Go to https://railway.app
2. Click "Login with GitHub"
3. Authorize Railway to access your GitHub account

### Step 2: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Click "Configure GitHub App"
4. Give Railway access to your repositories
5. Select your repository: `Wasia93/hackaton2`

### Step 3: Configure Backend Service

1. Railway will auto-detect your project
2. Click on the service that was created
3. Go to "Settings"
4. **Root Directory**: Set to `backend`
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 4: Add Environment Variables

1. Go to "Variables" tab
2. Click "Add Variable" for each:

```env
DATABASE_URL=postgresql://username:password@ep-xxx.neon.tech/neondb?sslmode=require
JWT_SECRET=your-super-secret-jwt-key-generate-a-strong-one
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=https://your-app.vercel.app
```

**Important**:
- Replace `DATABASE_URL` with your Neon connection string from Part 1
- Generate a strong `JWT_SECRET` (use a random string generator)
- We'll update `CORS_ORIGINS` after deploying frontend

### Step 5: Run Database Migration

1. In Railway, go to your service
2. Click "Deploy" to trigger first deployment
3. Wait for deployment to complete
4. Click on the service URL (e.g., `https://xxx.railway.app`)
5. You should see: `{"message": "Todo API - Phase II Full-Stack Application"}`

### Step 6: Run Migrations

**Option A: Using Railway CLI** (if installed):
```bash
railway run alembic upgrade head
```

**Option B: Manually** (recommended):
1. On Railway dashboard, click your service
2. Go to "Deployments" tab
3. Click the three dots on latest deployment
4. Click "View Logs"
5. You'll need to run migration manually on first deploy

**Note**: For now, the app will auto-create tables when first request is made due to SQLModel.

### Step 7: Test Backend

1. Copy your Railway backend URL (e.g., `https://todo-backend-xxx.railway.app`)
2. Visit `YOUR_URL/docs` to see API documentation
3. Try the health check: `YOUR_URL/health`
4. You should see: `{"status": "ok", ...}`

**Save your backend URL!** You'll need it for frontend.

---

## 🎨 Part 3: Deploy Frontend to Vercel

### Step 1: Create Vercel Account

1. Go to https://vercel.com
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel

### Step 2: Import Project

1. On Vercel dashboard, click "Add New..."
2. Select "Project"
3. Click "Import" next to your repository: `Wasia93/hackaton2`

### Step 3: Configure Project Settings

**Framework Preset**: Next.js (auto-detected)

**Root Directory**: `frontend` ⚠️ **IMPORTANT!**

**Build Settings**:
- Build Command: `npm run build` (auto-filled)
- Output Directory: `.next` (auto-filled)
- Install Command: `npm install` (auto-filled)

### Step 4: Add Environment Variables

Click "Environment Variables" and add:

```env
NEXT_PUBLIC_API_URL=https://todo-backend-xxx.railway.app
NEXT_PUBLIC_JWT_SECRET=your-super-secret-jwt-key-same-as-backend
```

**Important**:
- Use the **same JWT_SECRET** as your backend
- Use your **Railway backend URL** from Part 2

### Step 5: Deploy!

1. Click "Deploy"
2. Wait 2-3 minutes for build to complete
3. You'll get a URL like: `https://your-app.vercel.app`

### Step 6: Update Backend CORS

1. Go back to Railway dashboard
2. Open your backend service
3. Go to "Variables"
4. Update `CORS_ORIGINS` to your Vercel URL:
   ```
   CORS_ORIGINS=https://your-app.vercel.app
   ```
5. Save and redeploy backend

---

## ✅ Final Testing

### Test Complete Flow

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Click "Register" and create an account
3. You should be redirected to dashboard
4. **Add a task** - It should save!
5. **Refresh the page** - Task should still be there!
6. **Test all CRUD operations**:
   - ✅ Create tasks
   - ✅ View tasks
   - ✅ Edit tasks
   - ✅ Delete tasks
   - ✅ Toggle completion
   - ✅ Filter tasks
   - ✅ Sort tasks

### Verify Data Persistence

1. Create a few tasks
2. Log out
3. Close browser
4. Come back later
5. Log in again
6. **Tasks should still be there!** ✅

---

## 🔗 Your Deployed URLs

Fill these in after deployment:

- **Frontend (Vercel)**: `https://__________________________.vercel.app`
- **Backend (Railway)**: `https://__________________________.railway.app`
- **Database (Neon)**: `ep-__________________________.neon.tech`

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: Backend deployment fails
- Check Railway logs for errors
- Verify all environment variables are set
- Ensure DATABASE_URL is correct

**Problem**: API returns 500 errors
- Check Railway logs: Click service → Deployments → View Logs
- Verify database connection string
- Check if tables were created

**Problem**: CORS errors in browser console
- Update CORS_ORIGINS in Railway to match your Vercel URL
- Redeploy backend after changing

### Frontend Issues

**Problem**: "Failed to fetch" errors
- Verify NEXT_PUBLIC_API_URL points to Railway backend
- Check that backend is running (visit backend URL)
- Verify CORS is configured correctly

**Problem**: Build fails on Vercel
- Check build logs in Vercel dashboard
- Verify root directory is set to `frontend`
- Check that all dependencies are in package.json

**Problem**: Authentication doesn't work
- Ensure JWT_SECRET matches between frontend and backend
- Check browser console for errors
- Try clearing localStorage and logging in again

### Database Issues

**Problem**: Tables not created
- In Railway, run: `alembic upgrade head`
- Or check if SQLModel auto-creates tables on first request

**Problem**: Connection timeout
- Verify DATABASE_URL includes `?sslmode=require`
- Check Neon dashboard that project is active
- Try recreating the connection string

---

## 🚀 Performance Tips

### Frontend Optimization

1. **Enable Vercel Analytics**:
   - Go to Vercel project settings
   - Enable "Analytics"

2. **Add Caching**:
   - API responses are cached client-side
   - Static assets cached by Vercel CDN

### Backend Optimization

1. **Database Connection Pooling**:
   - Already configured in SQLModel
   - Neon handles connection pooling automatically

2. **API Response Times**:
   - Railway provides good latency
   - Neon is optimized for serverless

---

## 📊 Monitoring

### Check Application Health

**Backend Health**:
- Visit: `YOUR_BACKEND_URL/health`
- Should return: `{"status": "ok"}`

**Frontend Health**:
- Visit: `YOUR_FRONTEND_URL`
- Should load landing page

**Database Health**:
- Check Neon dashboard
- Monitor connection count
- Check query performance

---

## 🎯 Custom Domain (Optional)

### Add Custom Domain to Vercel

1. Go to Vercel project settings
2. Click "Domains"
3. Add your domain (e.g., `todo.yourdomain.com`)
4. Follow DNS configuration instructions
5. Update CORS_ORIGINS in Railway backend

### Add Custom Domain to Railway

1. Railway Pro plan required ($5/month)
2. Or use Railway's generated domain

---

## 💰 Cost Breakdown

### Free Tier Limits

**Neon (Database)**:
- ✅ 0.5 GB storage
- ✅ 1 project
- ✅ Unlimited requests
- **Cost**: $0/month

**Railway (Backend)**:
- ✅ $5 free credit/month
- ✅ ~500 hours runtime
- ✅ 1 GB RAM
- **Cost**: $0-5/month

**Vercel (Frontend)**:
- ✅ Unlimited deployments
- ✅ 100 GB bandwidth
- ✅ Automatic HTTPS
- **Cost**: $0/month

**Total**: Free for hobby projects! 🎉

---

## 🔄 Continuous Deployment

### Auto-Deploy on Git Push

**Vercel**:
- ✅ Auto-deploys on push to `main` branch
- ✅ Preview deployments for pull requests

**Railway**:
- ✅ Auto-deploys on push to `main` branch
- ✅ Checks `backend/` directory only

**Workflow**:
1. Make changes locally
2. `git add .` → `git commit -m "message"` → `git push`
3. Vercel and Railway auto-deploy
4. Check deployment status in dashboards

---

## 📝 Deployment Checklist Summary

- [ ] Neon database created ✓
- [ ] Database connection string obtained ✓
- [ ] Railway backend deployed ✓
- [ ] Backend environment variables configured ✓
- [ ] Backend health check passes ✓
- [ ] Vercel frontend deployed ✓
- [ ] Frontend environment variables configured ✓
- [ ] Backend CORS updated with Vercel URL ✓
- [ ] Full CRUD operations tested ✓
- [ ] Data persistence verified ✓
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up (optional)

---

## 🎉 You're Live!

Congratulations! Your Phase II Todo App is now deployed and accessible worldwide!

**Share your app**:
- Frontend: `https://your-app.vercel.app`
- API Docs: `https://your-backend.railway.app/docs`

**For Phase II Hackathon Submission**:
- Use your Vercel URL as the "Published App Link"
- Record your demo video showing the live app
- Submit via: https://forms.gle/KMKEKaFUD6ZX4UtY8

---

**Need help?** Check the troubleshooting section or reach out with specific error messages.

**Generated with Claude Code - Spec-Driven Development**
