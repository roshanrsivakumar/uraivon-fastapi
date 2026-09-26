import os
import re

# Update api/analyze.py
with open("api/analyze.py", "r") as f:
    analyze_content = f.read()

analyze_content = re.sub(
    r'OLLAMA_API_URL = os\.environ\.get\("OLLAMA_API_URL", "http://localhost:11434/api/generate"\)',
    'GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")\nOLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")',
    analyze_content
)

old_ask_ollama_analyze = """def ask_ollama(prompt: str) -> dict:
    try:
        payload = {
            "model": "qwen2.5:3b",
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "temperature": 0.1
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        result_text = response.json().get("response", "{}")
        return json.loads(result_text)
    except Exception as e:
        print(f"Ollama Error: {e}")
        return None"""

new_ask_analyze = """def ask_ai(prompt: str) -> dict:
    import json
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.1, "response_mime_type": "application/json"}
            }
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(result_text)
        except Exception as e:
            print(f"Gemini Error: {e}")
            return None
    else:
        try:
            payload = {
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "temperature": 0.1
            }
            response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
            response.raise_for_status()
            result_text = response.json().get("response", "{}")
            return json.loads(result_text)
        except Exception as e:
            print(f"Ollama Error: {e}")
            return None"""

analyze_content = analyze_content.replace(old_ask_ollama_analyze, new_ask_analyze)
analyze_content = analyze_content.replace("ai_result = ask_ollama(prompt)", "ai_result = ask_ai(prompt)")

with open("api/analyze.py", "w") as f:
    f.write(analyze_content)

# Update api/exam.py
with open("api/exam.py", "r") as f:
    exam_content = f.read()

exam_content = re.sub(
    r'OLLAMA_API_URL = os\.environ\.get\("OLLAMA_API_URL", "http://localhost:11434/api/generate"\)',
    'GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")\nOLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")',
    exam_content
)

old_ask_ollama_exam = """def ask_ollama(prompt: str) -> str:
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
        return None"""

new_ask_exam = """def ask_ai(prompt: str) -> str:
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.2}
            }
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"Gemini Error: {e}")
            return None
    else:
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
            return None"""

exam_content = exam_content.replace(old_ask_ollama_exam, new_ask_exam)
exam_content = exam_content.replace("ai_result = ask_ollama(prompt)", "ai_result = ask_ai(prompt)")
exam_content = exam_content.replace("Unable to reach the Local Jurimetric LLM engine. Please ensure Ollama is running.", "Unable to reach the Jurimetric Engine. Please ensure GEMINI_API_KEY is configured in Render.")

with open("api/exam.py", "w") as f:
    f.write(exam_content)

# Update api/story.py
with open("api/story.py", "r") as f:
    story_content = f.read()

story_content = re.sub(
    r'OLLAMA_API_URL = os\.environ\.get\("OLLAMA_API_URL", "http://localhost:11434/api/generate"\)',
    'GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")\nOLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/generate")',
    story_content
)

old_ask_ollama_story = """def ask_ollama(prompt: str) -> str:
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
        return None"""

new_ask_story = """def ask_ai(prompt: str) -> str:
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.4}
            }
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"Gemini Error: {e}")
            return None
    else:
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
            return None"""

story_content = story_content.replace(old_ask_ollama_story, new_ask_story)
story_content = story_content.replace("ai_result = ask_ollama(prompt)", "ai_result = ask_ai(prompt)")
story_content = story_content.replace("Unable to reach the Local Jurimetric LLM engine. Please ensure Ollama is running.", "Unable to reach the Jurimetric Engine. Please ensure GEMINI_API_KEY is configured in Render.")
story_content = story_content.replace("(Note: Start Ollama to generate exact BNS and IPC section mappings).", "(Note: Configure a Gemini API Key on Render to generate exact BNS and IPC section mappings).")

with open("api/story.py", "w") as f:
    f.write(story_content)

print("Patched FastAPI for Gemini support!")
