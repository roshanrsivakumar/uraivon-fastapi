import os
import json
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")

class StoryRequest(BaseModel):
    concept: str
    hero1: Optional[str] = "Friend 1"
    hero2: Optional[str] = "Friend 2"
    villain: Optional[str] = "The Villain"
    base_narrative: Optional[str] = ""

def ask_ollama(prompt: str) -> str:
    try:
        payload = {
            "model": "qwen2.5:3b",
            "prompt": prompt,
            "stream": False,
            "temperature": 0.4
        }
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        print(f"Ollama Error: {e}")
        return None

@router.post("/story/generate")
async def generate_story(req: StoryRequest):
    """
    Generates a personalized legal story with exact BNS sections and Landmark cases.
    """
    prompt = f"""You are Uraivon, an elite legal storyteller for Indian Law Students.
Explain the legal concept of "{req.concept}" using a dramatic narrative.

Cast:
- {req.hero1} (The Protagonist)
- {req.hero2} (The Neutral Observer/Judge/Ally)
- {req.villain} (The Antagonist)

Base Narrative Context (if any): {req.base_narrative}

Your story must:
1. Explain the legal doctrine clearly through the actions of the characters.
2. Explicitly cite the relevant Indian Penal Code (IPC) and the new Bharatiya Nyaya Sanhita (BNS) section numbers in the story.
3. Explicitly cite at least ONE landmark Supreme Court of India precedent that applies to this situation.
4. Conclude with {req.hero2} delivering a fair and lawful outcome based on this principle.

Output only the story text."""
    
    ai_result = ask_ollama(prompt)
    
    if ai_result:
        return {"status": "success", "story": ai_result}
    
    return {
        "status": "fallback", 
        "story": f"Unable to reach the Local Jurimetric LLM engine. Please ensure Ollama is running.\n\n[Fallback Story]\n{req.villain} attempted to violate the principles of {req.concept}, but {req.hero2} intervened using the landmark Indian Supreme Court precedent to save {req.hero1}. (Note: Start Ollama to generate exact BNS and IPC section mappings)."
    }
