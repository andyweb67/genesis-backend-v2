# --- FastAPI Backend main.py ---

from fastapi import FastAPI
from routers import claims

app = FastAPI(
    title="Genesis Backend API",
    description="Backend services for Genesis Claim Audit System",
    version="1.0.0"
)

# Include routers
app.include_router(claims.router)

# Root Welcome Message
@app.get("/")
def read_root():
    return {"message": "Welcome to the Genesis Backend API!"}
