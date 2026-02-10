# Phase 5 Quick Start ⚡

**Get Phase 5 running in 3 commands!**

## ⚠️ IMPORTANT: Use the Correct Startup Command

**DO NOT USE:** `uvicorn api.app:app`  
**USE THIS:** `python run_phase5.py` or `uvicorn api.app_complete:app`

---

## Option 1: Easiest Method (Recommended)

```bash
# 1. Clone and setup
git clone https://github.com/pranaya-mathur/LLM-Observability.git
cd LLM-Observability
git checkout phase5-security-dashboard

# 2. Install dependencies
pip install -r requirements_phase5.txt

# 3. Start API
python run_phase5.py
```

That's it! 🎉

**What you get:**
- 📊 API running on http://localhost:8000
- 📚 Docs at http://localhost:8000/docs
- 🔑 Auto-created admin user

**In another terminal, start dashboard:**
```bash
streamlit run dashboard/admin_dashboard.py
```

**Default Login:**
- Username: `admin`
- Password: `admin123`

---

## Option 2: Using uvicorn directly

```bash
# Terminal 1: Start API (use app_complete, NOT app)
python -m uvicorn api.app_complete:app --reload --port 8000

# Terminal 2: Start Dashboard
streamlit run dashboard/admin_dashboard.py
```

---

## Option 3: Automated Script (Linux/Mac)

```bash
# Makes everything easy
chmod +x start_phase5.sh
./start_phase5.sh

# To stop
./stop_phase5.sh
```

---

## Common Startup Errors & Fixes

### ❌ Error: `cannot import name 'User' from 'api.auth.models'`

**Cause:** You're trying to run the old `api/app.py` file

**Fix:** Use the correct command:
```bash
# WRONG
uvicorn api.app:app --reload

# CORRECT
python run_phase5.py
# OR
uvicorn api.app_complete:app --reload
```

### ❌ Error: Port 8000 already in use

**Fix:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### ❌ Error: Module not found

**Fix:**
```bash
# Install dependencies
pip install -r requirements_phase5.txt

# Make sure you're in project root
cd LLM-Observability
python run_phase5.py
```

---

## What to Test

### 1. Dashboard
Open http://localhost:8501
- ✅ Login with `admin / admin123`
- ✅ Check Overview page (tier charts)
- ✅ User Management (update roles/tiers)
- ✅ Detection Monitor (test responses)

### 2. API (via Browser)
Open http://localhost:8000/docs
- ✅ Click "Authorize"
- ✅ Login to get token
- ✅ Try `/api/detect` endpoint
- ✅ Test other endpoints

### 3. Automated Tests
```bash
python scripts/test_phase5_complete.py
```

Should see:
```
🎉 All tests passed! Phase 5 is fully functional.
```

---

## Quick API Test (curl)

```bash
# 1. Get token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login?username=admin&password=admin123" | jq -r '.access_token')

# 2. Test detection
curl -X POST "http://localhost:8000/api/detect" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "RAG stands for Ruthenium-Arsenic Growth"
  }' | jq

# 3. Check health
curl http://localhost:8000/api/monitoring/health | jq

# 4. List users (admin only)
curl -X GET "http://localhost:8000/api/admin/users" \
  -H "Authorization: Bearer $TOKEN" | jq
```

---

## Features to Explore

### 🔐 Authentication
- JWT tokens with 24-hour expiration
- Role-based access (admin/user/viewer)
- Secure password hashing (bcrypt)

### 🚦 Rate Limiting
- **Free:** 100 requests/hour
- **Pro:** 1,000 requests/hour
- **Enterprise:** 10,000 requests/hour

### 🛡️ 3-Tier Detection
1. **Tier 1:** Regex patterns (<1ms)
2. **Tier 2:** Semantic embeddings (5-10ms)
3. **Tier 3:** LLM agent reasoning (50-100ms)

### 👥 User Management
- Create/update/delete users
- Change roles and tiers
- Enable/disable accounts

### 📊 Monitoring
- Real-time tier statistics
- System health checks
- Detection logs

---

## File Structure (What to Use)

```
LLM-Observability/
├── api/
│   ├── app_complete.py       ✅ USE THIS (Phase 5)
│   ├── app.py                ❌ OLD (Phase 4)
│   ├── routes/
│   │   ├── auth.py           ✅ Authentication
│   │   ├── admin.py          ✅ User management
│   │   ├── detection.py      ✅ Detection with auth
│   │   └── monitoring.py     ✅ Health checks
│   └── auth/
│       ├── jwt_handler.py    ✅ JWT utilities
│       └── models.py         ✅ Pydantic models
├── run_phase5.py             ✅ Easy startup script
├── requirements_phase5.txt   ✅ All dependencies
└── dashboard/
    └── admin_dashboard.py    ✅ Streamlit UI
```

---

## Next Steps

1. ✅ **Test locally** (you are here!)
2. 📦 **Review code** in your IDE
3. 🔄 **Merge to main** when ready
4. 🚀 **Deploy** to production

---

## Documentation

- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Complete testing instructions
- **[PHASE5_COMPLETE.md](PHASE5_COMPLETE.md)** - Full documentation
- **API Docs:** http://localhost:8000/docs

---

## Default Accounts

| User | Username | Password | Role | Tier |
|------|----------|----------|------|------|
| Admin | `admin` | `admin123` | admin | enterprise |
| Test User | `testuser` | `test123` | user | free |

**⚠️ Change these passwords in production!**

---

## Support

For issues:
1. Check you're using `api.app_complete:app` not `api.app:app`
2. Check logs: `tail -f logs/api.log` (if using startup script)
3. Review [TESTING_GUIDE.md](TESTING_GUIDE.md)
4. Open GitHub issue

---

**Happy Testing! 🎉**

Phase 5 is production-ready and fully functional.
