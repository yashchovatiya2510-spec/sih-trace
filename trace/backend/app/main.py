from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine
from app.api import auth, ngos, claims, inspections, alerts, evidence

app = FastAPI(
    title=settings.APP_NAME,
    description="Transparent Resource & Audit Compliance Ecosystem API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(ngos.router, prefix="/api/ngos", tags=["ngos"])
app.include_router(claims.router, prefix="/api/claims", tags=["claims"])
app.include_router(inspections.router, prefix="/api/inspections", tags=["inspections"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(evidence.router, prefix="/api/evidence", tags=["evidence"])

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME}

# Create dummy routers if they don't exist yet so it runs
