import os
import sys
import subprocess
import webbrowser
from time import sleep
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_dependencies():
    """Check if all required packages are installed"""
    try:
        with open('requirements.txt', 'r') as f:
            required = f.read().splitlines()
        
        logger.info("Checking dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        logger.info("✅ All dependencies are installed.")
        return True
    except Exception as e:
        logger.error(f"❌ Error checking dependencies: {str(e)}")
        return False

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/version')
        if response.status_code == 200:
            logger.info("✅ Ollama is running.")
            return True
    except:
        logger.warning("⚠️ Ollama is not running.")
        return False

def check_environment():
    """Check if .env file exists and contains necessary variables"""
    try:
        if not os.path.exists('.env'):
            logger.info("Creating .env file with default settings...")
            with open('.env', 'w') as f:
                f.write("# OpenAI API Key (Required for ChatGPT)\n")
                f.write("OPENAI_API_KEY=\n\n")
                f.write("# Ollama Settings\n")
                f.write("OLLAMA_HOST=http://localhost:11434\n")
                f.write("OLLAMA_MODEL=deepseek-r1\n")
        return True
    except Exception as e:
        logger.error(f"❌ Error setting up environment: {str(e)}")
        return False

def start_application():
    """Start the Travel AI Assistant"""
    try:
        print("\n=== Starting Travel AI Assistant ===")
        print("Initializing...")
        
        # Check if we're in the correct directory
        if not os.path.exists('app/main.py'):
            logger.error("❌ Error: Please run this script from the travel_ai_app directory")
            print("\nMake sure you're in the travel_ai_app directory and it contains:")
            print("  - app/main.py")
            print("  - requirements.txt")
            print("  - .env file (will be created if missing)")
            return
        
        # Check dependencies
        if not check_dependencies():
            logger.error("❌ Failed to install dependencies")
            return
        
        # Check environment setup
        if not check_environment():
            logger.error("❌ Failed to setup environment")
            return
        
        # Check Ollama
        if not check_ollama():
            print("\n⚠️ WARNING: Ollama is not running!")
            print("To use Ollama models, please start Ollama in a separate terminal:")
            print("  $ ollama serve")
            choice = input("\nDo you want to continue anyway? (y/n): ")
            if choice.lower() != 'y':
                return
        
        # Start the application
        print("\n🚀 Starting Travel AI Assistant...")
        print("💻 The web interface will open in your default browser...")
        
        # Open browser after a short delay
        def open_browser():
            sleep(2)  # Wait for Streamlit to start
            # webbrowser.open('http://localhost:8501')
        
        from threading import Thread
        Thread(target=open_browser).start()
        
        # Start Streamlit with the correct module path
        streamlit_command = f'{sys.executable} -m streamlit run app/main.py'
        logger.info(f"Running command: {streamlit_command}")
        os.system(streamlit_command)
        
    except Exception as e:
        logger.error(f"❌ Error starting application: {str(e)}")

def display_welcome():
    """Display welcome message and instructions"""
    print("""
╔════════════════════════════════════════╗
║        Travel AI Assistant Setup        ║
╚════════════════════════════════════════╝

This script will:
1. Check and install required dependencies
2. Verify Ollama installation (if using local model)
3. Setup environment configuration
4. Start the Travel AI web interface

Requirements:
- Python 3.8 or higher
- Internet connection
- Ollama (optional, for local AI model)

For help or issues, please check the documentation
or create an issue on the project repository.
""")

if __name__ == "__main__":
    display_welcome()
    start_application() 