# Configuration settings for the Travel AI Assistant

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model Configuration
MODEL_NAME = "deepseek-r1"
MODEL_INSTRUCTIONS = [
    "You are a Travel AI Assistant specialized in providing comprehensive travel planning advice.",
    "For itineraries: Provide day-wise breakdown with timing",
    "For hotels: Include price ranges, areas, and key amenities",
    "For food: Focus on local specialties, popular restaurants, and food safety",
    "For activities: Consider weather, season, and traveler preferences",
    "Always consider budget constraints when mentioned",
    "Include local travel tips and cultural insights",
    "Mention safety precautions when relevant",
    "Structure responses clearly with sections and bullet points"
]

# API Configuration
API_HOST = "0.0.0.0"
API_START_PORT = 8000
API_MAX_ATTEMPTS = 100

# UI Configuration
UI_TITLE = "Travel AI Assistant"
UI_SUBTITLE = "Your personal AI travel planner"
UI_LAYOUT = "wide"
UI_ICON = "✈️"

# Categories
INTERESTS = [
    "Sightseeing",
    "Food & Dining",
    "Adventure",
    "Culture & History",
    "Shopping",
    "Nature & Outdoors",
    "Relaxation & Spa",
    "Nightlife",
    "Family Activities",
    "Local Experiences"
]

BUDGET_OPTIONS = [
    "Not specified",
    "Budget (Under $100/day)",
    "Moderate ($100-$300/day)",
    "Luxury ($300+/day)"
]

# LLM Models Configuration
LLM_MODELS = {
    "ollama": {
        "name": "Ollama",
        "model": "deepseek-r1",
        "provider": "local",
        "description": "Local AI model using Ollama"
    },
    "openai": {
        "name": "ChatGPT",
        "model": "gpt-3.5-turbo",
        "provider": "OpenAI",
        "description": "OpenAI's ChatGPT model"
    }
}

# OpenAI Configuration
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.7

# Quick Actions
QUICK_ACTIONS = {
    "hotels": {
        "prompt": """Find hotels in {destination} within {budget} budget range. For each recommended hotel, provide:
1. Hotel name and brief description
2. Price range per night
3. Location highlights
4. Booking links for:
   - Booking.com
   - Agoda
   - MakeMyTrip
   - Expedia
Please format each hotel recommendation with clear sections and include direct booking links."""
    },
    "activities": {
        "icon": "🎯",
        "label": "Activities",
        "prompt": "Suggest activities in {destination} matching these interests: {interests}"
    },
    "restaurants": {
        "icon": "🍽️",
        "label": "Restaurants",
        "prompt": "Recommend restaurants in {destination} for {budget} budget"
    }
}

# API Configuration
API_TIMEOUT = 30  # seconds
CACHE_DURATION = 3600  # 1 hour 