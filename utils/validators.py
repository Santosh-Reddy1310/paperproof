import re
from typing import Tuple, List

class InputValidator:
    @staticmethod
    def validate_topic(topic: str) -> Tuple[bool, str]:
        """Validate research topic input"""
        if not topic or not topic.strip():
            return False, "Topic cannot be empty"
        
        if len(topic.strip()) < 10:
            return False, "Topic should be at least 10 characters long"
        
        if len(topic.strip()) > 200:
            return False, "Topic should be less than 200 characters"
        
        # Check for inappropriate content (basic)
        inappropriate_words = ['test', 'testing', 'hello', 'example']
        if any(word in topic.lower() for word in inappropriate_words):
            return False, "Please provide a serious academic topic"
        
        return True, "Valid topic"
    
    @staticmethod
    def validate_api_key(api_key: str) -> Tuple[bool, str]:
        """Validate OpenRouter API key format"""
        if not api_key or not api_key.strip():
            return False, "API key cannot be empty"
        
        # Basic format check (OpenRouter keys typically start with 'sk-or-' for paid, but free accounts may have different formats)
        if not (api_key.startswith('sk-or-') or api_key.startswith('free-') or len(api_key) > 10):
            return False, "Invalid API key format. Check your OpenRouter API key"
        
        if len(api_key) < 20:
            return False, "API key appears to be too short"
        
        return True, "Valid API key format"
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for download"""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Replace spaces with underscores
        filename = re.sub(r'\s+', '_', filename)
        # Limit length
        return filename[:50]