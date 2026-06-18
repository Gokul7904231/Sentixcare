"""
Mental Health Resources Display Module for AI MoodMate
Handles the display of mental health resources and professional support links
"""

import streamlit as st
from typing import Dict, List

def display_mental_health_resources(emotion: str, intensity: int = 5, title: str = "🆘 Mental Health Support"):
    """Display comprehensive mental health resources based on emotion and intensity"""
    
    st.markdown("---")
    st.subheader(title)
    st.markdown("*Professional support and resources for your emotional well-being*")
    
    # Get priority resources
    from src.features.mental_health_resources import mental_health_resources # Updated import
    priority_resources = mental_health_resources.get_priority_resources(emotion, intensity)
    
    # Display crisis resources first if high intensity
    if intensity >= 7 and emotion.lower() in ["sad", "angry", "fear"]:
        display_crisis_resources()
    
    # Display professional counseling resources
    display_professional_counseling()
    
    # Display emotion-specific resources
    display_emotion_specific_resources(emotion)
    
    # Display self-help resources
    display_self_help_resources()
    
    # Add disclaimer
    display_mental_health_disclaimer()

def display_crisis_resources():
    """Display immediate crisis support resources"""
    st.markdown("### 🚨 Immediate Crisis Support")
    st.warning("**If you're in immediate danger or having thoughts of self-harm, please reach out for help right now.**")
    
    from src.features.mental_health_resources import mental_health_resources # Updated import
    crisis_resources = mental_health_resources.get_crisis_resources()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Suicide Prevention Lifeline
        resource = crisis_resources["suicide_prevention"]
        st.markdown(f"""
        <div style="background-color: #ffebee; padding: 15px; border-radius: 10px; border-left: 5px solid #f44336; margin: 10px 0;">
            <h4>🆘 {resource['name']}</h4>
            <p><strong>Phone:</strong> {resource['phone']}</p>
            <p><strong>Text:</strong> {resource['text']}</p>
            <p><strong>Available:</strong> {resource['available']}</p>
            <p>{resource['description']}</p>
            <a href="{resource['website']}" target="_blank" style="color: #f44336; font-weight: bold;">🔗 Visit Website</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Crisis Text Line
        resource = crisis_resources["crisis_text"]
        st.markdown(f"""
        <div style="background-color: #e8f5e8; padding: 15px; border-radius: 10px; border-left: 5px solid #4caf50; margin: 10px 0;">
            <h4>💬 {resource['name']}</h4>
            <p><strong>Text:</strong> {resource['phone']}</p>
            <p><strong>Available:</strong> {resource['available']}</p>
            <p>{resource['description']}</p>
            <a href="{resource['website']}" target="_blank" style="color: #4caf50; font-weight: bold;">🔗 Visit Website</a>
        </div>
        """, unsafe_allow_html=True)
    
    # SAMHSA Helpline
    resource = crisis_resources["samhsa"]
    st.markdown(f"""
    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #2196f3; margin: 10px 0;">
        <h4>📞 {resource['name']}</h4>
        <p><strong>Phone:</strong> {resource['phone']}</p>
        <p><strong>Available:</strong> {resource['available']}</p>
        <p>{resource['description']}</p>
        <a href="{resource['website']}" target="_blank" style="color: #2196f3; font-weight: bold;">🔗 Visit Website</a>
    </div>
    """, unsafe_allow_html=True)

def display_professional_counseling():
    """Display professional counseling and therapy resources"""
    st.markdown("### 👩‍⚕️ Professional Counseling & Therapy")
    st.markdown("**Find licensed mental health professionals in your area or online:**")
    
    from src.features.mental_health_resources import mental_health_resources # Updated import
    counseling_resources = mental_health_resources.get_counseling_resources()
    
    # Psychology Today
    resource = counseling_resources["psychology_today"]
    st.markdown(f"""
    <div style="background-color: #f3e5f5; padding: 15px; border-radius: 10px; border-left: 5px solid #9c27b0; margin: 10px 0;">
        <h4>🔍 {resource['name']}</h4>
        <p>{resource['description']}</p>
        <p><strong>Features:</strong> {', '.join(resource['features'])}</p>
        <a href="{resource['website']}" target="_blank" style="color: #9c27b0; font-weight: bold;">🔗 Find Therapists</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Online Therapy Options
    col1, col2 = st.columns(2)
    
    with col1:
        resource = counseling_resources["betterhelp"]
        st.markdown(f"""
        <div style="background-color: #fff3e0; padding: 15px; border-radius: 10px; border-left: 5px solid #ff9800; margin: 10px 0;">
            <h4>💻 {resource['name']}</h4>
            <p>{resource['description']}</p>
            <p><strong>Features:</strong> {', '.join(resource['features'])}</p>
            <a href="{resource['website']}" target="_blank" style="color: #ff9800; font-weight: bold;">🔗 Get Started</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        resource = counseling_resources["talkspace"]
        st.markdown(f"""
        <div style="background-color: #e0f2f1; padding: 15px; border-radius: 10px; border-left: 5px solid #009688; margin: 10px 0;">
            <h4>📱 {resource['name']}</h4>
            <p>{resource['description']}</p>
            <p><strong>Features:</strong> {', '.join(resource['features'])}</p>
            <a href="{resource['website']}" target="_blank" style="color: #009688; font-weight: bold;">🔗 Learn More</a>
        </div>
        """, unsafe_allow_html=True)
    
    # Affordable Therapy
    resource = counseling_resources["open_path"]
    st.markdown(f"""
    <div style="background-color: #fce4ec; padding: 15px; border-radius: 10px; border-left: 5px solid #e91e63; margin: 10px 0;">
        <h4>💰 {resource['name']}</h4>
        <p>{resource['description']}</p>
        <p><strong>Features:</strong> {', '.join(resource['features'])}</p>
        <a href="{resource['website']}" target="_blank" style="color: #e91e63; font-weight: bold;">🔗 Find Affordable Therapy</a>
    </div>
    """, unsafe_allow_html=True)

def display_emotion_specific_resources(emotion: str):
    """Display resources specific to the detected emotion"""
    from src.features.mental_health_resources import mental_health_resources # Updated import
    emotion_resources = mental_health_resources.get_emotion_specific_resources(emotion)
    
    if emotion_resources:
        st.markdown(f"### 🎯 Resources for {emotion.title()} Feelings")
        st.markdown(f"**Specialized support and information for {emotion} emotions:**")
        
        for key, resource in emotion_resources.items():
            st.markdown(f"""
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 10px; border-left: 5px solid #607d8b; margin: 10px 0;">
                <h4>📚 {resource['name']}</h4>
                <p>{resource['description']}</p>
                <a href="{resource['website']}" target="_blank" style="color: #607d8b; font-weight: bold;">🔗 Visit Resource</a>
            </div>
            """, unsafe_allow_html=True)

def display_self_help_resources():
    """Display self-help and educational resources"""
    st.markdown("### 🧘 Self-Help & Educational Resources")
    st.markdown("**Tools and techniques you can use on your own:**")
    
    from src.features.mental_health_resources import mental_health_resources # Updated import
    self_help_resources = mental_health_resources.get_self_help_resources()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Mindfulness
        resource = self_help_resources["mindfulness"]
        st.markdown(f"""
        <div style="background-color: #e8f5e8; padding: 15px; border-radius: 10px; border-left: 5px solid #4caf50; margin: 10px 0;">
            <h4>🧘 {resource['name']}</h4>
            <p>{resource['description']}</p>
            <a href="{resource['website']}" target="_blank" style="color: #4caf50; font-weight: bold;">🔗 Learn Mindfulness</a>
        </div>
        """, unsafe_allow_html=True)
        
        # CBT Resources
        resource = self_help_resources["cbt"]
        st.markdown(f"""
        <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #2196f3; margin: 10px 0;">
            <h4>🧠 {resource['name']}</h4>
            <p>{resource['description']}</p>
            <a href="{resource['website']}" target="_blank" style="color: #2196f3; font-weight: bold;">🔗 Learn CBT Techniques</a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Headspace
        resource = self_help_resources["meditation"]
        st.markdown(f"""
        <div style="background-color: #fff3e0; padding: 15px; border-radius: 10px; border-left: 5px solid #ff9800; margin: 10px 0;">
            <h4>📱 {resource['name']}</h4>
            <p>{resource['description']}</p>
            <a href="{resource['website']}" target="_blank" style="color: #ff9800; font-weight: bold;">🔗 Try Headspace</a>
        </div>
        """, unsafe_allow_html=True)
        
        # Calm
        resource = self_help_resources["calm"]
        st.markdown(f"""
        <div style="background-color: #f3e5f5; padding: 15px; border-radius: 10px; border-left: 5px solid #9c27b0; margin: 10px 0;">
            <h4>🌊 {resource['name']}</h4>
            <p>{resource['description']}</p>
            <a href="{resource['website']}" target="_blank" style="color: #9c27b0; font-weight: bold;">🔗 Try Calm</a>
        </div>
        """, unsafe_allow_html=True)

def display_mental_health_disclaimer():
    """Display important disclaimer about mental health resources"""
    st.markdown("---")
    st.markdown("### ⚠️ Important Information")
    st.info("""
    **This app provides general information and resources for mental health support. It is not a substitute for professional medical advice, diagnosis, or treatment.**
    
    - **For emergencies:** Call 911 or go to your nearest emergency room
    - **For crisis support:** Use the crisis resources listed above
    - **For professional help:** Consult with a licensed mental health professional
    - **For medical concerns:** Speak with your healthcare provider
    
    Always seek the advice of qualified health providers with questions about your mental health.
    """)

def display_quick_mental_health_links(emotion: str, intensity: int = 5):
    """Display quick access links for mental health resources"""
    st.markdown("### 🆘 Quick Mental Health Links")
    
    # Priority links based on emotion and intensity
    if intensity >= 7 and emotion.lower() in ["sad", "angry", "fear"]:
        st.markdown("**🚨 Immediate Support:**")
        st.markdown("- [National Suicide Prevention Lifeline: 988](https://suicidepreventionlifeline.org/)")
        st.markdown("- [Crisis Text Line: Text HOME to 741741](https://www.crisistextline.org/)")
    
    st.markdown("**👩‍⚕️ Professional Help:**")
    st.markdown("- [Find Local Therapists](https://www.psychologytoday.com/us/therapists)")
    st.markdown("- [Online Therapy Options](https://www.betterhelp.com/)")
    
    st.markdown("**🧘 Self-Help Resources:**")
    st.markdown("- [Mindfulness Resources](https://www.mindful.org/)")
    st.markdown("- [CBT Self-Help](https://www.apa.org/ptsd-guideline/patients-and-families/cognitive-behavioral)")

def create_mental_health_sidebar():
    """Create a sidebar with mental health resources and crisis support"""
    st.markdown("---")
    st.markdown("### 🆘 Crisis Support")
    
    st.markdown("**🚨 Emergency:** Call 911")
    st.markdown("**🆘 Suicide Prevention:** 988")
    st.markdown("**💬 Crisis Text:** Text HOME to 741741")
    
    st.markdown("---")
    st.markdown("### 👩‍⚕️ Professional Help")
    st.markdown("- [Find Therapists](https://www.psychologytoday.com/us/therapists)")
    st.markdown("- [Online Therapy](https://www.betterhelp.com/)")
    st.markdown("- [Affordable Therapy](https://openpathcollective.org/)")
    
    st.markdown("---")
    st.markdown("### 🧘 Self-Help")
    st.markdown("- [Mindfulness](https://www.mindful.org/)")
    st.markdown("- [Meditation Apps](https://www.headspace.com/)")
    st.markdown("- [CBT Resources](https://www.apa.org/ptsd-guideline/patients-and-families/cognitive-behavioral)")
    
    st.markdown("---")
    st.markdown("### ⚠️ Important")
    st.markdown("**This app is not a substitute for professional mental health care. If you're in crisis, please reach out for immediate help.**")

@st.fragment
def show_chatbot(emotion):
    """Display the wellness chatbot interface based on detected emotion.
    Runs as a fragment to prevent the entire page from rerunning on input.
    """
    import streamlit as st
    from src.features.wellness_chatbot import wellness_chatbot # Updated import
    from src.ui.enhanced_ui import apply_chat_styling
    
    # Apply chat styling
    apply_chat_styling()
    
    # Diagnostics
    status_emoji = "🟢" if wellness_chatbot.gemini_available else "🟡"
    status_text = "Gemini AI Active" if wellness_chatbot.gemini_available else "Enhanced Fallback Mode"
    st.markdown(f"### 💬 Wellness Companion **{status_emoji} {status_text}**")
    
    if hasattr(wellness_chatbot, 'model') and wellness_chatbot.model:
        model_name = getattr(wellness_chatbot.model, "model_name", "gemini-1.5-flash")
        display_name = model_name.replace("models/", "").replace("-", " ").title()
        st.caption(f"🤖 Powered by {display_name}")
    
    # Get initial response based on emotion
    initial_response = wellness_chatbot.get_initial_response(emotion, 80)
    
    # Display welcome message with new styling
    st.markdown(f"""
    <div class="welcome-message">
        <h4>🤖 Your Wellness Companion</h4>
        <p>{initial_response}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # 1. Layout: Define container first so it appears above the input
    if not st.session_state.chat_history:
        # No history: draw a borderless or standard flow container (no scroll view)
        chat_container = st.container()
    else:
        # Has history: frame it with a 400px scrollable view
        chat_container = st.container(height=400, border=True)

    # 2. Render input below the container
    user_message = st.chat_input(
        "Type your message here...",
        key=f"chatbot_input_{emotion}",
    )

    # 3. Process input and update state immediately
    if user_message:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message,
        })

        if wellness_chatbot.model:
            bot_response = wellness_chatbot.get_gemini_response(user_message, emotion)
        else:
            bot_response = wellness_chatbot.get_supportive_response()

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": bot_response,
        })

    # 4. Render the chat history visually inside the container defined above
    with chat_container:
        for message in st.session_state.chat_history:
            avatar = "👤" if message["role"] == "user" else "🌟"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(f'<div style="white-space: pre-wrap; word-break: break-word; overflow-wrap: anywhere; max-width: 100%; line-height: 1.5;">{message["content"]}</div>', unsafe_allow_html=True)

    # Clear chat button
    if st.button("Clear Chat 🗑️", key="clear_chat_btn"):
        st.session_state.chat_history = []
        st.rerun(scope="fragment")

    # Show wellness tip
    st.markdown("---")
    st.markdown("#### 💡 Wellness Tip")
    tip = wellness_chatbot.get_wellness_tip(emotion)
    st.markdown(f'''
    <div class="wellness-tip">
        <h5>💡 Daily Wellness Tip</h5>
        <p>{tip}</p>
    </div>
    ''', unsafe_allow_html=True)

    # Show coping strategies
    with st.expander("🧘 Coping Strategies"):
        strategies = wellness_chatbot.coping_strategies
        st.markdown('<div class="coping-strategies"><ol>', unsafe_allow_html=True)
        for i, strategy in enumerate(strategies, 1):
            st.markdown(f'<li>{strategy}</li>', unsafe_allow_html=True)
        st.markdown('</ol></div>', unsafe_allow_html=True)

