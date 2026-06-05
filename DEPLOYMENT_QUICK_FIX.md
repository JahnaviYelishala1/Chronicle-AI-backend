# 🔧 Quick Debugging Checklist for Render Deployment Error

## Error: "No open ports detected" / "Timed Out"

This means your FastAPI app isn't binding to a port. Follow this checklist:

---

## ✅ Step 1: Local Validation (Do This First)

```powershell
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Run the validation script
python scripts/validate_startup.py
```

**Expected output:** All checks should show ✓ PASS

---

## ✅ Step 2: Test Locally

```powershell
# Start the app locally
uvicorn app.main:app --host 0.0.0.0 --port 8000

# In another terminal, test health check
curl http://localhost:8000/health
curl http://localhost:8000/health/detailed

# Check API docs
# Open browser: http://localhost:8000/docs
```

**Expected:** Should bind successfully and respond to requests

---

## ✅ Step 3: Verify Environment Variables in Render

Go to Render Dashboard → Your Service → Environment:

| Variable | Status | Action |
|----------|--------|--------|
| `DATABASE_URL` | ? | Must be set ✅ |
| `SUPABASE_URL` | ? | Must be set ✅ |
| `SUPABASE_SERVICE_KEY` | ? | Must be set ✅ |
| `OPENROUTER_API_KEY` | ? | Must be set ✅ |

**Missing variables = App crashes at startup**

---

## ✅ Step 4: Check Render Logs

Dashboard → Service → **Logs** tab

Look for error messages like:
- `ModuleNotFoundError` → Missing dependency
- `KeyError` → Missing env variable  
- `ConnectionError` → Database connection failed
- `Import Error` → Code syntax issue

---

## ✅ Step 5: Validate render.yaml

```powershell
# Check if render.yaml is correct
cat render.yaml

# Should have:
# - startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
# - healthCheckPath: /health
# - preDeployCommand: python scripts/validate_startup.py
```

---

## 🚀 Next Steps to Fix

### If validation script shows ❌ errors:
1. Fix the errors shown in the output
2. Test locally again
3. Push to git
4. Retry deploy

### If environment variables are missing:
1. Add them in Render Dashboard
2. Trigger manual redeploy
3. Check logs again

### If logs show import errors:
```powershell
# Make sure all dependencies are in requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
# Retry deployment in Render
```

### If database connection fails:
```powershell
# Test database connection locally
python -c "
import os
from supabase import create_client
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_SERVICE_KEY')
if url and key:
    client = create_client(url, key)
    print('✓ Database connection OK')
else:
    print('✗ Missing SUPABASE_URL or SUPABASE_SERVICE_KEY')
"
```

---

## 🧪 Health Check After Deployment

Once deployed, test these endpoints:

```bash
# Basic status
curl https://your-service.onrender.com/health

# Detailed diagnostics  
curl https://your-service.onrender.com/health/detailed

# API documentation
# Visit: https://your-service.onrender.com/docs
```

---

## 💡 Pro Tips

- ✅ Always run `python scripts/validate_startup.py` locally before deploying
- ✅ Check Render logs immediately after failed deploy
- ✅ Use `/health/detailed` endpoint to verify all services are configured
- ✅ Keep `requirements.txt` updated with `pip freeze > requirements.txt`
- ✅ Test with: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

---

## 📋 Files Created for Debugging

- **`render.yaml`** - Updated with validation and health check
- **`scripts/validate_startup.py`** - Comprehensive startup validator
- **`.RENDER_DEPLOYMENT_GUIDE.md`** - Full deployment guide
- **`app/main.py`** - Enhanced with logging and health endpoints

---

**Need more help?** Check `.RENDER_DEPLOYMENT_GUIDE.md` for detailed troubleshooting
