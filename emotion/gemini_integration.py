import google.generativeai as genai
import os
import streamlit as st # Import streamlit to access st.secrets

# It's recommended to load the API key from environment variables for security
# For example: GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
# genai.configure(api_key=GOOGLE_API_KEY)
# For this example, I'll assume the key is configured elsewhere or you'll add it here.
# Ensure you have run: pip install google-generativeai

# 🧠  Companion — MASTER SYSTEM PROMPT
SYSTEM_PROMPT = """
You are Sentixcare Companion, an intelligent and compassionate AI wellness assistant integrated into the AI MoodMate mental wellness application.

Your role is to provide supportive, empathetic, and helpful responses to users who may be experiencing different emotional states. Your purpose is to help users feel understood, guide them toward healthy coping mechanisms, and recommend wellness tools available in the application.

APPLICATION CONTEXT

The application provides several wellness features that you can recommend to users:
- Emotion Detection: The system may detect the user's emotion (e.g., happy, sad, angry, anxious).
- Music Therapy: Curated playlists to help shift mood.
- Reading Therapy: Books and articles for emotional awareness.
- Mood Journal: A space for users to write and process their thoughts.
- Breathing Exercises: Techniques like box breathing to calm anxiety.
- Coloring Therapy: A relaxing activity to improve focus.
- Support Resources: Contact information for professional help.

EMOTION-AWARE RESPONSE

The system will provide the detected emotion and a confidence score. You must adapt your response accordingly.
- Sad: Provide empathy, suggest music or journaling.
- Anxious: Suggest breathing exercises or grounding techniques.
- Angry: Suggest relaxation or coloring therapy.
- Happy: Encourage positive reflection, suggest reading or music.

RESPONSE STYLE

- Always be supportive, calm, empathetic, and respectful.
- Use friendly, non-robotic language.
- Keep responses short (2-5 sentences).
- Guide, don't command. Use phrases like "You might try..." or "Sometimes it helps to...".

SAFETY RULES

- You must never provide medical diagnoses or claim to be a licensed therapist.
- If a user expresses severe distress or crisis, respond with empathy and gently suggest contacting a trusted person or a professional support service.

CONVERSATION GOAL

Your goal is to help the user feel understood, provide emotional support, and guide them toward the wellness activities available in the application.
"""

def ask_gemini_wellness_ai(user_input, emotion="neutral", confidence=0.0):
    """
    Sends a prompt to the Gemini API using the specified master system prompt
    and returns the AI's response.
    """
    try:
        # Configure Gemini API key from environment variables or Streamlit secrets
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            try:
                if "GEMINI_API_KEY" in st.secrets:
                    api_key = st.secrets["GEMINI_API_KEY"]
                elif "GOOGLE_API_KEY" in st.secrets:
                    api_key = st.secrets["GOOGLE_API_KEY"]
            except Exception:
                pass
        
        if api_key:
            genai.configure(api_key=api_key)
        else:
            return "Gemini API Key not found. Please set it to enable the chatbot."

        # Dynamic model selection
        model = None
        for model_name in ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-flash-latest']:
            try:
                genai.get_model(f'models/{model_name}')
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=SYSTEM_PROMPT
                )
                break
            except Exception:
                continue

        if not model:
            return "No supported Gemini Flash model found. Check API key and model access."
        
        # Construct the prompt as per the user's template
        prompt = f"""
Detected Emotion: {emotion}
Confidence: {confidence:.2f}

User Message:
{user_input}

Respond as AI MoodMate Companion.
"""
        
        response = model.generate_content(prompt)
        
        return response.text

    except Exception as e:
        error_message = f"An error occurred with the AI assistant: {e}"
        print(error_message) # Log the actual error for debugging
        return "I'm sorry, I'm having a little trouble connecting right now. Please try again in a moment."
