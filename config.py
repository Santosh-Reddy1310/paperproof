import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Turbo settings for Flash
    DEFAULT_MODEL = "gemini-1.5-flash"
    MAX_PARALLEL_REQUESTS = 3  # Balance between speed and rate limits
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 2000))
    DAILY_LIMIT = int(os.getenv('DAILY_LIMIT', 60))
    
    # Available Gemini models (free tier)
    AVAILABLE_MODELS = {
        'Gemini Flash (Fast & Free)': 'gemini-1.5-flash',
        'Gemini Pro (Standard)': 'gemini-pro'
    }
    
    # Recommended models for different paper sections
    SECTION_MODELS = {
        'abstract': 'gemini-1.5-flash',
        'introduction': 'gemini-1.5-flash',
        'literature_review': 'gemini-1.5-flash',
        'methodology': 'gemini-1.5-flash',
        'results_discussion': 'gemini-1.5-flash',
        'conclusion': 'gemini-1.5-flash',
        'references': 'gemini-1.5-flash'
    }
    SECTION_CHUNKING = True  # Break long sections into smaller parallel requests
    
    # Paper parameters
    MAX_PAPER_LENGTH = 5000  # words
    MIN_PAPER_LENGTH = 1000  # words
    DEFAULT_SECTIONS = [
        'Abstract',
        'Introduction', 
        'Literature Review',
        'Methodology',
        'Results and Discussion',
        'Conclusion',
        'References'
    ]
    
    # Rate limiting for free tier
    RATE_LIMIT = {
        'requests_per_minute': 60,
        'tokens_per_minute': 30000,
        'delay_between_requests': 1  # seconds
    }