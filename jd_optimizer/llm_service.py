
import requests
import json
import logging

logger = logging.getLogger("JD_Optimizer_LLM")
logger.setLevel(logging.INFO)

class LLMService:
    def __init__(self, provider="ollama", model="llama3.1", api_key=None, base_url=None):
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.base_url = base_url or ("http://localhost:11434/api/generate" if provider == "ollama" else None)

    def call_llm(self, prompt, system_prompt=None):
        if self.provider == "ollama":
            return self._call_ollama(prompt, system_prompt)
        elif self.provider == "gemini":
            return self._call_google_gemini(prompt, system_prompt)
        else:
            return self._call_external_api(prompt, system_prompt)

    def _call_google_gemini(self, prompt, system_prompt):
        # Native Google Gemini REST API implementation
        if not self.api_key:
             return json.dumps({"error": "Gemini API Key is required"})
             
        # Construct URL - default to v1beta if no specific base_url overrides
        # We ignore the OpenAI compat URL if it was passed by accident
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            
        payload = {
            "contents": [{
                "role": "user", 
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }
        
        if system_prompt:
             payload["system_instruction"] = {
                 "parts": [{"text": system_prompt}]
             }
             
        try:
            response = requests.post(url, json=payload, timeout=300)
            if response.status_code == 200:
                result = response.json()
                # Extract text from Candidate -> Content -> Parts
                try:
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError):
                    return json.dumps({"error": "Gemini response structure unexpected", "raw": result})
            else:
                return json.dumps({"error": f"Gemini API {response.status_code}: {response.text}"})
        except Exception as e:
            return json.dumps({"error": str(e)})

    def _call_ollama(self, prompt, system_prompt):
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "system": system_prompt,
                "stream": False,
                "format": "json"
            }
            response = requests.post(self.base_url, json=payload, timeout=300)
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                logger.error(f"Ollama error: {response.text}")
                return json.dumps({"error": f"Ollama returned {response.status_code}"})
        except Exception as e:
            logger.exception("Ollama connection failed")
            return json.dumps({"error": str(e)})

    def _call_external_api(self, prompt, system_prompt):
        # Placeholder for OpenAI/Groq or other OpenAI-compatible APIs
        if not self.base_url:
            return json.dumps({"error": "External API URL not set"})
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
        }
        
        # We assume OpenAI compatible endpoint
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
        
        # Only add response_format for OpenAI or strict-compatible providers that differ from Google
        # Google's OpenAI compat layer can sometimes be picky or returns 404s on models if features mismatch
        if "googleapis" not in self.base_url:
             payload["response_format"] = {"type": "json_object"}
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=300)
            if response.status_code == 200:
                res_data = response.json()
                return res_data["choices"][0]["message"]["content"]
            else:
                return json.dumps({"error": f"API returned {response.status_code}: {response.text}"})
        except Exception as e:
            return json.dumps({"error": str(e)})
