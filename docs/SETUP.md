# Travel Buddy AI Assistant - Setup Guide

## Prerequisites
- Python 3.8 or higher
- Ollama installed
- Git (optional)
- Anaconda or Miniconda (for Conda environment)

## Installation Steps

1. **Create Project Directory**
   ```bash
   mkdir travel_ai_app
   cd travel_ai_app
   ```

2. **Set Up Virtual Environment**
   
   Choose one of the following methods:

   **Option A: Using Conda (Recommended)**
   ```bash
   # Create new conda environment
   conda create -n travel_ai python=3.10
   
   # Activate the environment
   # On Windows/Linux/macOS:
   conda activate travel_ai
   
   # Install pip in conda environment (if not installed)
   conda install pip
   ```

   **Option B: Using venv**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate the environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Ollama Service**
   ```bash
   ollama serve
   ```

5. **Pull Required Model**
   ```bash
   ollama pull deepseek-r1
   ```

6. **Run the Application**
   ```bash
   streamlit run app/main.py
   ```

## Accessing the Application

- Web Interface: http://localhost:8501
- API Documentation: http://localhost:8501 (Click API Documentation in UI)

## API Usage

1. **Travel Plan Endpoint**
   ```bash
   curl -X POST "http://localhost:[port]/travel-plan" \
        -H "Content-Type: application/json" \
        -d '{
          "destination": "Paris",
          "dates": "2024-03-01 to 2024-03-07",
          "budget": "Mid-range",
          "preferences": {
            "interests": ["Culture", "Food"]
          }
        }'
   ```

2. **Chat Endpoint**
   ```bash
   curl -X POST "http://localhost:[port]/chat" \
        -H "Content-Type: application/json" \
        -d '{
          "message": "Suggest restaurants in Paris",
          "category": "food"
        }'
   ```

## Environment Management

### Conda Commands
```bash
# List all conda environments
conda env list

# Update conda environment
conda env update -f environment.yml

# Export conda environment
conda env export > environment.yml

# Remove conda environment
conda deactivate
conda env remove -n travel_ai
```

## Troubleshooting

1. **Port Conflicts**
   - Application automatically finds available ports
   - Check if Ollama is running
   - Close competing applications

2. **Model Issues**
   - Verify Ollama is running
   - Re-pull the model
   - Check model compatibility

3. **Response Errors**
   - Check network connection
   - Verify Ollama service status
   - Review error messages in console

4. **Conda Issues**
   - Update conda: `conda update -n base conda`
   - Clean conda cache: `conda clean --all`
   - Verify conda environment activation
   - Check Python version: `python --version`

## Additional Configuration

- Model settings can be adjusted in config.py
- UI customization available in main.py
- Port configurations can be modified if needed 