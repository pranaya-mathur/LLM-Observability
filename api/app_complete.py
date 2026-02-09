"""Complete FastAPI application with authentication, detection, and admin routes.

Run with:
    uvicorn api.app_complete:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from persistence.database import init_db
from api.routes import auth, admin, monitoring, detection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle management for FastAPI app."""
    # Startup
    print("🚀 Starting LLM Observability API with Phase 5 features...")
    try:
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")
    
    print("\n📋 Default credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n📋 Test user:")
    print("   Username: testuser")
    print("   Password: user123")
    print("\n🌐 Dashboard: streamlit run dashboard/admin_dashboard.py")
    print("📚 API Docs: http://localhost:8000/docs\n")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down LLM Observability API...")


app = FastAPI(
    title="LLM Observability API - Phase 5",
    description="""Production-grade LLM observability with:
    - 3-tier detection (Regex → Semantic → LLM)
    - JWT authentication
    - Rate limiting
    - Admin dashboard
    - User management
    """,
    version="5.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(monitoring.router)
app.include_router(detection.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "LLM Observability API",
        "version": "5.0.0",
        "status": "operational",
        "phase": "5 - Security & Dashboard",
        "features": [
            "3-Tier Detection System",
            "JWT Authentication",
            "Rate Limiting",
            "Admin Dashboard",
            "User Management",
            "Real-time Monitoring",
        ],
        "docs": "/docs",
        "dashboard": "Run: streamlit run dashboard/admin_dashboard.py",
        "default_login": {
            "username": "admin",
            "password": "admin123",
        },
    }


@app.get("/health")
async def health():
    """Quick health check (no auth required)."""
    return {
        "status": "healthy",
        "version": "5.0.0",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.app_complete:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
