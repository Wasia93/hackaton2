# Skill: deploy.vercel

## Description
Deploy frontend to Vercel

## Usage
```
/deploy.vercel
/deploy.vercel --production
```

## What It Does
- Builds Next.js frontend
- Deploys to Vercel
- Displays deployment URL
- Updates environment variables (if needed)

## Commands Executed

### Via Vercel CLI
```bash
cd frontend
vercel --prod  # Production deployment
# or
vercel  # Preview deployment
```

### Via Git Push (Recommended)
```bash
git add .
git commit -m "Deploy frontend"
git push origin main  # Auto-deploys if connected to Vercel
```

## Prerequisites
- Vercel account created
- Project connected to Vercel (via GitHub)
- Environment variables configured in Vercel dashboard
- Frontend build passing locally

## Environment Variables (Vercel Dashboard)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=https://your-app.vercel.app
NEXT_PUBLIC_WS_URL=wss://your-backend-url.com (Phase III+)
```

## Deployment Flow
1. Push code to GitHub
2. Vercel auto-detects changes
3. Builds Next.js application
4. Runs build checks
5. Deploys to production/preview
6. Returns deployment URL

## Flags
- `--production` - Deploy to production (main branch)
- `--preview` - Create preview deployment
- `--env` - Update environment variables

## Build Configuration (vercel.json)
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["iad1"]
}
```

## Post-Deployment Checks
- [ ] Site accessible at deployment URL
- [ ] API calls working (check browser console)
- [ ] Authentication functional
- [ ] No console errors
- [ ] Environment variables correct

## Troubleshooting

### Build Fails
- Check build logs in Vercel dashboard
- Test build locally: `npm run build`
- Verify dependencies in package.json

### API Calls Failing
- Check NEXT_PUBLIC_API_URL correct
- Verify backend is deployed and accessible
- Check CORS configuration on backend

### Environment Variables Not Working
- Ensure variables prefixed with `NEXT_PUBLIC_` for client-side
- Redeploy after changing variables
- Check for typos in variable names

## Related Files
- `frontend/` - Next.js application
- `vercel.json` - Vercel configuration
- `.vercelignore` - Files to ignore

## Related Agents
- `.claude/agents/deployment.md`
- `.claude/agents/phase2-web.md`

---

**Tip**: Connect GitHub repo to Vercel for automatic deployments on push to main.
