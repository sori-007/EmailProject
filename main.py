from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import email_agent
from app.db import models, database

# -----------------------------
# App Configuration
# -----------------------------
app = FastAPI(
    title="AI Email Agent",
    description="Automated AI system for email management",
    version="1.1.0"
)

# -----------------------------
# Middleware Configuration
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Database Setup
# -----------------------------
models.Base.metadata.create_all(bind=database.engine)

# -----------------------------
# Router Registration
# -----------------------------
app.include_router(email_agent.router)

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {"status": "AI Email Agent API with DB logging ✅"}
