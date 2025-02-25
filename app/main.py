import streamlit as st
import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.config import (
    UI_TITLE, UI_SUBTITLE, UI_LAYOUT, UI_ICON,
    BUDGET_OPTIONS, INTERESTS, QUICK_ACTIONS
)
from app.utils import LLMHandler

def streamlit_ui():
    # Must be the first Streamlit command
    st.set_page_config(
        page_title=UI_TITLE,
        page_icon=UI_ICON,
        layout=UI_LAYOUT
    )

    # Custom CSS to align button with input
    st.markdown("""
    <style>
        .st-emotion-cache-ocqkz7 {
            align-items: end !important;
            padding-top: 1rem !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'llm_handler' not in st.session_state:
        st.session_state.llm_handler = LLMHandler()
    if 'current_model' not in st.session_state:
        st.session_state.current_model = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key" not in st.session_state:
        st.session_state.api_key = None
    if "api_key_submitted" not in st.session_state:
        st.session_state.api_key_submitted = False
    
    # Model Selection in Sidebar
    with st.sidebar:
        st.header("AI Model Settings")
        model_type = st.radio(
            "Select AI Model",
            ["ollama", "openai"],
            help="Choose between local Ollama model or OpenAI's ChatGPT",
            horizontal=True
        )
        
        # OpenAI API Key input if ChatGPT is selected
        if model_type == "openai":
            api_key_container = st.container()
            
            with api_key_container:
                col1, col2 = st.columns([5, 1])
                with col1:
                    api_key = st.text_input(
                        "OpenAI API Key",
                        type="password",
                        value=st.session_state.api_key if st.session_state.api_key else "",
                        help="Enter your OpenAI API key",
                        label_visibility="visible",
                        key="api_key_input"
                    )
                with col2:
                    st.write("")  # Single spacing for better alignment
                    submit_button = st.button("🔑", help="Submit API Key", use_container_width=True)
                    if submit_button:
                        if api_key:
                            submit_api_key(api_key)
                        else:
                            st.error("Enter key")
            
            if not st.session_state.api_key_submitted:
                st.warning("Please submit your OpenAI API key")
                return
        else:
            api_key = None
            # Clear API key if switching to Ollama
            if st.session_state.api_key:
                clear_api_key()
        
        # Initialize or switch model
        if st.session_state.current_model != model_type:
            try:
                st.session_state.llm_handler.initialize_model(model_type, st.session_state.api_key)
                st.session_state.current_model = model_type
                st.success(f"Successfully initialized {model_type} model")
            except Exception as e:
                st.error(f"Error initializing model: {str(e)}")
                return
        
        st.header("Travel Preferences")
        destination = st.text_input("Destination:")
        
        # Date range selection with calendars
        st.subheader("Travel Dates")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", min_value=None, help="Select your travel start date")
        with col2:
            end_date = st.date_input("End Date", min_value=start_date, help="Select your travel end date")
        
        # Format dates for use in the application
        dates = f"{start_date} to {end_date}" if start_date and end_date else ""
        
        budget = st.selectbox("Budget Range:", BUDGET_OPTIONS)
        interests = st.multiselect("Interests:", INTERESTS)
    
    # Main content area
    st.title(UI_TITLE)
    st.markdown(UI_SUBTITLE)
    
    # Display current model info
    if st.session_state.current_model:
        st.info(f"Currently using: {st.session_state.current_model.upper()}")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.container():
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Travel Buddy:** {message['content']}")
    
    # Quick action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏨 Find Hotels"):
            if destination:
                prompt = QUICK_ACTIONS["hotels"]["prompt"].format(
                    destination=destination,
                    budget=budget
                )
                with st.spinner("Finding hotels..."):
                    try:
                        response = st.session_state.llm_handler.chat(prompt, {
                            "destination": destination,
                            "budget": budget,
                            "dates": dates,
                            "interests": interests
                        })
                        
                        # Store the original prompt and create a formatted response
                        formatted_prompt = f"**You:** Looking for hotels in {destination} ({budget})"
                        
                        # Format the response with clickable links
                        formatted_response = "**Travel Buddy:** Here are some hotel recommendations:\n\n"
                        formatted_response += response.replace("Booking.com:", "[Book on Booking.com](https://www.booking.com/search.html?ss=" + destination.replace(" ", "+") + ")")
                        formatted_response = formatted_response.replace("Agoda:", "[Book on Agoda](https://www.agoda.com/search?city=" + destination.replace(" ", "+") + ")")
                        formatted_response = formatted_response.replace("MakeMyTrip:", "[Book on MakeMyTrip](https://www.makemytrip.com/hotels/hotels-" + destination.replace(" ", "-").lower() + ")")
                        formatted_response = formatted_response.replace("Expedia:", "[Book on Expedia](https://www.expedia.com/Hotel-Search?destination=" + destination.replace(" ", "+") + ")")
                        
                        st.session_state.messages.append({"role": "user", "content": formatted_prompt})
                        st.session_state.messages.append({"role": "assistant", "content": formatted_response})
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please specify a destination first")
    
    with col2:
        if st.button("🎯 Activities"):
            if destination and interests:
                prompt = QUICK_ACTIONS["activities"]["prompt"].format(
                    destination=destination,
                    interests=", ".join(interests)
                )
                with st.spinner("Finding activities..."):
                    try:
                        response = st.session_state.llm_handler.chat(prompt, {
                            "destination": destination,
                            "interests": interests,
                            "budget": budget,
                            "dates": dates
                        })
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please specify destination and interests")
    
    with col3:
        if st.button("🍽️ Restaurants"):
            if destination:
                prompt = QUICK_ACTIONS["restaurants"]["prompt"].format(
                    destination=destination,
                    budget=budget
                )
                with st.spinner("Finding restaurants..."):
                    try:
                        response = st.session_state.llm_handler.chat(prompt, {
                            "destination": destination,
                            "budget": budget,
                            "interests": interests
                        })
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please specify a destination first")
    
    # Chat input
    user_input = st.text_input("Ask anything about your travel plans:")
    
    if st.button("Send") and user_input:
        with st.spinner("Planning your perfect trip..."):
            try:
                context = {
                    "destination": destination,
                    "dates": dates,
                    "budget": budget,
                    "interests": interests
                }
                response = st.session_state.llm_handler.chat(user_input, context)
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

def submit_api_key(api_key):
    """Handle API key submission"""
    if api_key:
        st.session_state.api_key = api_key
        st.session_state.api_key_submitted = True
        return True
    return False

def clear_api_key():
    """Clear stored API key"""
    st.session_state.api_key = None
    st.session_state.api_key_submitted = False
    st.session_state.current_model = None

def main():
    streamlit_ui()

if __name__ == "__main__":
    main() 