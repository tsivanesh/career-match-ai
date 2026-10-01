import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'careermatch-ai-secret-key-production-grade-2026')
    DATABASE_PATH = os.path.join(BASE_DIR, 'career_match.db')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 'yes']
    
    # Recommendation Engine Weights (Total = 1.0 / 100%)
    # Configurable for experimentation and placement demonstrations
    RECOMMENDATION_WEIGHTS = {
        'skill_match': float(os.environ.get('WEIGHT_SKILL', 0.50)),
        'education_match': float(os.environ.get('WEIGHT_EDUCATION', 0.15)),
        'experience_match': float(os.environ.get('WEIGHT_EXPERIENCE', 0.15)),
        'interest_match': float(os.environ.get('WEIGHT_INTEREST', 0.10)),
        'location_workmode_match': float(os.environ.get('WEIGHT_LOCATION', 0.10))
    }
    
    # Matching thresholds & constants
    MIN_DISPLAY_SCORE = 10.0  # Minimum % to show in recommendations
    DEFAULT_PAGE_SIZE = 12
