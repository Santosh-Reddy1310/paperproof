import google.generativeai as genai
import time
from typing import Dict, List, Optional
import concurrent.futures
from config import Config
import streamlit as st

class GeminiClient:
    def __init__(self, api_key: str):  # Require key as parameter
        if not api_key:
            raise ValueError("API key is required")
        genai.configure(api_key=api_key)  # Configure with user's key
        self.last_request_time = 0
        self.request_count = 0
        self.token_count = 0
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=Config.MAX_PARALLEL_REQUESTS)
        
    def get_model(self, model_name: str = None):
        """Get a Gemini model instance with caching"""
        model_name = model_name or Config.DEFAULT_MODEL
        # This method is no longer needed as we only use one model
        return genai.GenerativeModel(model_name)

    def _generate_chunk(self, prompt_chunk: str, model: str, temperature: float, max_tokens: int) -> str:
        """Internal method to generate content for a single chunk."""
        try:
            model_instance = self.get_model(model)
            response = model_instance.generate_content(
                prompt_chunk,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": min(max_tokens, 2000)  # Flash cap
                }
            )
            self.request_count += 1
            self.token_count += len(response.text.split())  # Approximate token count
            return response.text
        except Exception as e:
            if "quota" in str(e).lower():
                st.error("You've reached your free tier quota. Please try again later.")
                raise
            print(f"Retrying chunk... Error: {str(e)}")
            time.sleep(1)
            raise  # Re-raise to be caught by the main retry logic if needed

    def generate_content(self,
                       prompt: str,
                       model: str = None,
                       retry_count: int = 3, **kwargs) -> str:
        model = model or 'gemini-1.5-flash'  # Default to Flash
        temperature = kwargs.get('temperature', 0.7)
        max_tokens = kwargs.get('max_tokens', 2000)

        if self.request_count >= Config.DAILY_LIMIT:
            raise Exception(f"Daily limit of {Config.DAILY_LIMIT} requests reached")

        if len(prompt.split()) < 100 or not Config.SECTION_CHUNKING:  # Short prompts or chunking disabled
            for attempt in range(retry_count):
                try:
                    return self._generate_chunk(prompt, model, temperature, max_tokens)
                except Exception as e:
                    if attempt == retry_count - 1:
                        raise Exception(f"API request failed after {retry_count} attempts: {str(e)}")
                    time.sleep(2 ** attempt)  # Exponential backoff
            raise Exception("Failed to generate content after all retry attempts")

        # Split long prompts into parallelizable chunks
        words = prompt.split()
        chunk_size = len(words) // Config.MAX_PARALLEL_REQUESTS
        chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

        futures = [self.executor.submit(self._generate_chunk, chunk, model, temperature, max_tokens) for chunk in chunks]

        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            time.sleep(Config.RATE_LIMIT['delay_between_requests'])  # Maintain rate limit

        return " ".join(results)
    
    def get_usage_stats(self) -> Dict:
        """Get current usage statistics"""
        return {
            "request_count": self.request_count,
            "token_count": self.token_count,
            "daily_limit": Config.DAILY_LIMIT,
            "remaining_requests": max(0, Config.DAILY_LIMIT - self.request_count)
        }