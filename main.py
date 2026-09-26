from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.analyze import router as analyze_router
from api.story import router as story_router

app = FastAPI(
    title="Uraivon Jurimetrics Engine API",
    description="Sovereign AI backend for corporate risk analysis.",
    version="1.0.0"
)

# Allow requests from the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "operational", "engine": "Uraivon Core", "llm": "Local (Llama-3 stubs)"}

app.include_router(analyze_router, prefix="/api/v1")
app.include_router(story_router, prefix="/api/v1")
