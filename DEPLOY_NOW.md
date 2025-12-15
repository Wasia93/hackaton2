# 🚀 Deploy Your Todo App NOW - Quick Start

**Time to deploy**: 20 minutes | **All FREE tiers**

---

## ⚡ Quick Steps

### 1️⃣ Database (5 min)

1. Go to https://neon.tech → Sign up with GitHub
2. Create new project: "todo-app"
3. **Copy the connection string** (starts with `postgresql://`)
4. Save it somewhere safe!

---

### 2️⃣ Backend (10 min)

1. Go to https://railway.app → Login with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select: `Wasia93/hackaton2`
4. After deployment starts:
   - Settings → Root Directory: `backend`
   - Variables → Add these:

```
DATABASE_URL=your-neon-connection-string-here
JWT_SECRET=make-up-a-long-random-string-here
CORS_ORIGINS=https://your-app.vercel.app
```

5. Click service URL → Should see API message
6. **Copy your Railway URL** (e.g., `https://xxx.railway.app`)

---

### 3️⃣ Frontend (5 min)

1. Go to https://vercel.com → Sign up with GitHub
2. Click "Add New..." → "Project"
3. Import: `Wasia93/hackaton2`
4. **Important**: Root Directory = `frontend`
5. Add Environment Variables:

```
NEXT_PUBLIC_API_URL=your-railway-url-here
NEXT_PUBLIC_JWT_SECRET=same-as-backend-jwt-secret
```

6. Deploy!
7. **Copy your Vercel URL**

---

### 4️⃣ Update CORS (2 min)

1. Go back to Railway
2. Variables → Update `CORS_ORIGINS` with your Vercel URL
3. Redeploy

---

## ✅ Test It!

1. Visit your Vercel URL
2. Register an account
3. Create tasks
4. Refresh page → Tasks should still be there!

---

## 🎯 Your Live URLs

After deployment, fill these in:

- **Your Live App**: https://________________________.vercel.app
- **Backend API**: https://________________________.railway.app
- **Database**: Neon dashboard

---

## 📹 For Hackathon Submission

Use your **Vercel URL** as the "Published App Link" in the submission form:
https://forms.gle/KMKEKaFUD6ZX4UtY8

---

## ❓ Need Help?

See full guide: `DEPLOYMENT_GUIDE.md`

**Common Issues**:
- CORS errors → Update CORS_ORIGINS in Railway
- Build fails → Check root directory is `frontend`
- API errors → Check DATABASE_URL in Railway
