import streamlit as st
from fastapi import FastAPI, HTTPException
from phi.llm.ollama import Ollama
from phi.assistant import Assistant
import uvicorn
from pydantic import BaseModel
import threading
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Optional, Dict
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import local modules
from config import (
    MODEL_NAME, MODEL_INSTRUCTIONS, API_HOST, API_START_PORT, 
    API_MAX_ATTEMPTS, UI_TITLE, UI_SUBTITLE, UI_LAYOUT, 
    UI_ICON, INTERESTS, BUDGET_OPTIONS
)
from utils import find_available_port, get_chat_response

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    category: Optional[str] = None

class TravelRequest(BaseModel):
    destination: str
    dates: Optional[str] = None
    budget: Optional[str] = None
    preferences: Optional[dict] = None

# Initialize Ollama and Assistant
llm = Ollama(
    model=MODEL_NAME,
)

assistant = Assistant(
    name="Travel Buddy AI",
    llm=llm,
    description="I am a specialized travel planning assistant powered by AI.",
    instructions=MODEL_INSTRUCTIONS
)

# API endpoints
@app.get("/")
def read_root():
    start_time = time.time()
    logger.info("Entering root endpoint")
    
    try:
        response = {"message": "Welcome to the Travel Buddy AI API"}
        execution_time = time.time() - start_time
        logger.info(f"Exiting root endpoint - Execution time: {execution_time:.2f} seconds")
        return response
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Error in root endpoint - Execution time: {execution_time:.2f} seconds - Error: {str(e)}")
        raise

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    logger.info(f"Entering chat endpoint with message: {request.message[:50]}...")
    
    try:
        response = assistant.chat(request.message)
        execution_time = time.time() - start_time
        logger.info(f"Exiting chat endpoint - Execution time: {execution_time:.2f} seconds")
        return {"response": response}
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Error in chat endpoint - Execution time: {execution_time:.2f} seconds - Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/travel-plan")
async def travel_plan_endpoint(request: TravelRequest):
    start_time = time.time()
    logger.info(f"Entering travel-plan endpoint for destination: {request.destination}")
    
    try:
        prompt = f"""
        Create a travel plan for {request.destination}
        Dates: {request.dates or 'Flexible'}
        Budget: {request.budget or 'Not specified'}
        Preferences: {json.dumps(request.preferences) if request.preferences else 'None specified'}
        
        Please provide a comprehensive plan including:
        1. Recommended itinerary
        2. Accommodation options
        3. Local food recommendations
        4. Activities and attractions
        5. Transportation tips
        """
        response = assistant.chat(prompt)
        execution_time = time.time() - start_time
        logger.info(f"Exiting travel-plan endpoint - Execution time: {execution_time:.2f} seconds")
        return {"response": response}
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Error in travel-plan endpoint - Execution time: {execution_time:.2f} seconds - Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def run_fastapi():
    start_time = time.time()
    logger.info("Starting FastAPI server")
    
    port = find_available_port(API_START_PORT, API_MAX_ATTEMPTS)
    if port is None:
        logger.error("Could not find available port")
        st.error("Could not find an available port. Please close some applications and try again.")
        return
    
    try:
        logger.info(f"Server starting on port {port}")
        uvicorn.run(app, host=API_HOST, port=port)
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Failed to start API server - Execution time: {execution_time:.2f} seconds - Error: {str(e)}")
        st.error(f"Failed to start API server: {str(e)}")

def streamlit_ui():
    st.set_page_config(
        page_title=UI_TITLE,
        page_icon=UI_ICON,
        layout=UI_LAYOUT
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .travel-category {
            padding: 10px;
            border-radius: 5px;
            margin: 5px;
            background-color: #2c3e50;
            color: white;
        }
        .chat-container {
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .user-message {
            background-color: #e6f3ff;
        }
        .assistant-message {
            background-color: #f0f0f0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title(UI_TITLE)
    st.markdown(UI_SUBTITLE)
    
    # Sidebar for travel preferences
    with st.sidebar:
        st.header("Travel Preferences")
        destination = st.text_input("Destination:")
        dates = st.text_input("Travel Dates (optional):")
        budget = st.selectbox("Budget Range:", BUDGET_OPTIONS)
        interests = st.multiselect("Interests:", INTERESTS)
    
    # Main chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Quick action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏨 Find Hotels"):
            if destination:
                prompt = f"Suggest hotels in {destination} for {budget} budget"
                with st.spinner("Finding hotels..."):
                    response = get_chat_response(assistant, prompt, "hotels")
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
            else:
                st.warning("Please specify a destination first")

    with col2:
        if st.button("🍴 Local Food"):
            if destination:
                prompt = f"Recommend local food and restaurants in {destination}"
                with st.spinner("Finding food recommendations..."):
                    response = get_chat_response(assistant, prompt, "food")
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
            else:
                st.warning("Please specify a destination first")

    with col3:
        if st.button("🎯 Activities"):
            if destination:
                prompt = f"Suggest activities and attractions in {destination}"
                with st.spinner("Finding activities..."):
                    response = get_chat_response(assistant, prompt, "activities")
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
            else:
                st.warning("Please specify a destination first")
    
    # Chat input
    user_input = st.text_input("Ask anything about your travel plans:")
    
    if st.button("Send") and user_input:
        with st.spinner("Planning your perfect trip..."):
            try:
                if destination:
                    context = f"For destination: {destination}, "
                    if dates:
                        context += f"dates: {dates}, "
                    if budget != "Not specified":
                        context += f"budget: {budget}, "
                    if interests:
                        context += f"interests: {', '.join(interests)}, "
                    enhanced_prompt = context + user_input
                else:
                    enhanced_prompt = user_input
                
                response = get_chat_response(assistant, enhanced_prompt)
                if response:
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Display chat history
    st.markdown("### Conversation History")
    for message in st.session_state.messages:
        with st.container():
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Travel Buddy:** {message['content']}")

def main():
    # Start FastAPI in a separate thread
    api_thread = threading.Thread(target=run_fastapi, daemon=True)
    api_thread.start()
    
    # Run Streamlit UI
    streamlit_ui()

if __name__ == "__main__":
    main() 