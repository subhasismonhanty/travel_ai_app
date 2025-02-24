# Configuration settings for the Travel AI Assistant

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
UI_TITLE = "✈️ Travel Buddy AI"
UI_SUBTITLE = "Your personal AI travel planning assistant"
UI_LAYOUT = "wide"
UI_ICON = "✈️"

# Categories
INTERESTS = [
    "Culture",
    "Food",
    "Adventure",
    "Nature",
    "Shopping",
    "Relaxation"
]

BUDGET_OPTIONS = [
    "Not specified",
    "Budget",
    "Mid-range",
    "Luxury"
] 