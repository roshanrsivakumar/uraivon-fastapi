import os
import json
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")

class ExamQuestion(BaseModel):
    question: str
    marks: int
    subject: str

def ask_ollama(prompt: str) -> str:
    try:
        payload = {
            "model": "qwen2.5:3b",
            "prompt": prompt,
            "stream": False,
            "temperature": 0.2
        }
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        print(f"Ollama Error: {e}")
        return None

@router.post("/exam/generate_answer")
async def generate_answer(req: ExamQuestion):
    """
    Generates a structured TNDALU-format answer for a given PYQ using the local LLM.
    """
    if req.marks <= 7:
        structure = "I. INTRODUCTION\\nII. STATUTORY PROVISIONS & INGREDIENTS\\nIII. LANDMARK CASE LAWS\\nIV. CONCLUSION"
    elif req.marks == 12:
        structure = "I. FACTS\\nII. ISSUES\\nIII. LEGAL PROVISIONS\\nIV. ANALYSIS (arguing both sides)\\nV. FINAL DECISION"
    else:
        structure = "I. INTRODUCTION\\nII. STATUTORY PROVISIONS\\nIII. CASE LAWS & EXCEPTIONS\\nIV. CONCLUSION"

    prompt = f"""You are an elite Indian Law Professor. Provide a brilliant, strictly structured answer to the following university exam question for {req.subject}.
Marks: {req.marks}

Question: "{req.question}"

You must structure your answer exactly like this:
{structure}

Do not add conversational filler. Be academic and cite at least one landmark Supreme Court of India case and the relevant IPC/BNS/Statute section."""
    
    ai_result = ask_ollama(prompt)
    
    if ai_result:
        return {"status": "success", "answer": ai_result}
    
    # Fallback
    return {
        "status": "fallback", 
        "answer": f"Unable to reach the Local Jurimetric LLM engine. Please ensure Ollama is running.\n\n[Fallback Placeholder Answer for: {req.question}]\nThis question relates to the core principles of {req.subject}. A comprehensive answer requires analyzing the statutory framework and landmark Supreme Court precedents."
    }
