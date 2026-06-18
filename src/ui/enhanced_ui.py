"""
Enhanced UI Components for AI MoodMate
Clear, engaging design with soothing pastel colors and interactive elements
"""

import streamlit as st
from typing import Dict, List
import streamlit.components.v1 as components

def apply_enhanced_styling():
    """Apply enhanced, clear styling with soothing pastel colors"""
    st.markdown("""
    <style>
    /* Enhanced App Styling */
    .main {
        padding-top: 1rem;
        padding-bottom: 2rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f4fd 50%, #f0f8ff 100%);
        min-height: 100vh;
    }
    
    /* Clear, Crisp Header Styling */
    .enhanced-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    .enhanced-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.1) 100%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    .enhanced-header::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.1);
        z-index: 1;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .enhanced-header h1 {
        font-size: 5rem;
        font-weight: 900;
        margin-bottom: 1.5rem;
        text-shadow: 5px 5px 10px rgba(0,0,0,0.8);
        position: relative;
        z-index: 3;
        letter-spacing: -2px;
        color: #ffffff !important;
        text-stroke: 2px rgba(0,0,0,0.6);
        -webkit-text-stroke: 2px rgba(0,0,0,0.6);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .enhanced-header p {
        font-size: 1.6rem;
        opacity: 1;
        margin-bottom: 0.8rem;
        font-weight: 700;
        position: relative;
        z-index: 3;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        color: #ffffff;
        text-stroke: 0.5px rgba(0,0,0,0.3);
        -webkit-text-stroke: 0.5px rgba(0,0,0,0.3);
    }
    
    /* Soothing Pastel Colors */
    .pastel-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 2.5rem;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .pastel-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(135deg, #a8e6cf 0%, #88d8c0 50%, #7fcdcd 100%);
    }
    
    .pastel-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.2);
    }
    
    /* Interactive Cursor Effects */
    .interactive-button {
        background: linear-gradient(135deg, #a8e6cf 0%, #88d8c0 50%, #7fcdcd 100%);
        color: #2c3e50;
        border: none;
        border-radius: 50px;
        padding: 1.2rem 3rem;
        font-weight: 700;
        font-size: 1.2rem;
        transition: all 0.4s ease;
        box-shadow: 0 10px 30px rgba(168, 230, 207, 0.4);
        min-height: 60px;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .interactive-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.6s;
    }
    
    .interactive-button:hover::before {
        left: 100%;
    }
    
    .interactive-button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 15px 40px rgba(168, 230, 207, 0.6);
        background: linear-gradient(135deg, #b8f6df 0%, #98e8d0 50%, #8fdddd 100%);
    }
    
    /* Soothing Radio Buttons */
    .soothing-radio {
        background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.1);
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .soothing-radio:hover {
        border-color: #a8e6cf;
        box-shadow: 0 15px 35px rgba(168, 230, 207, 0.2);
    }
    
    .soothing-radio label {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 15px;
        transition: all 0.3s ease;
        cursor: pointer;
        background: linear-gradient(135deg, #f8f9ff 0%, #e8f4fd 100%);
        border: 2px solid transparent;
    }
    
    .soothing-radio label:hover {
        background: linear-gradient(135deg, #e8f4fd 0%, #d1ecf1 100%);
        border-color: #a8e6cf;
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 8px 20px rgba(168, 230, 207, 0.3);
    }
    
    /* Pastel Color Palette */
    .pastel-blue { background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); }
    .pastel-green { background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); }
    .pastel-purple { background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); }
    .pastel-pink { background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%); }
    .pastel-orange { background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 100%); }
    
    /* Enhanced Typography */
    .stMarkdown {
        font-size: 17px;
        line-height: 1.7;
        color: #2c3e50;
    }
    
    .stMarkdown h1 {
        font-size: 3rem;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stMarkdown h2 {
        font-size: 2.4rem;
        color: #34495e;
        margin-bottom: 1.2rem;
        font-weight: 600;
    }
    
    .stMarkdown h3 {
        font-size: 1.9rem;
        color: #34495e;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Soothing Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9ff 100%);
        font-size: 16px;
        border-right: 2px solid #e8f4fd;
    }
    
    .css-1d391kg .stMarkdown {
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Enhanced Messages */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #a8e6cf;
        border-radius: 20px;
        padding: 1.2rem;
        color: #155724;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(168, 230, 207, 0.3);
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #ffd93d;
        border-radius: 20px;
        padding: 1.2rem;
        color: #856404;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(255, 217, 61, 0.3);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border: 2px solid #7fcdcd;
        border-radius: 20px;
        padding: 1.2rem;
        color: #0c5460;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(127, 205, 205, 0.3);
    }
    
    /* Custom Cursor */
    body {
        cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="%23a8e6cf" opacity="0.3"/><circle cx="12" cy="12" r="6" fill="%23667eea" opacity="0.6"/><circle cx="12" cy="12" r="2" fill="%23667eea"/></svg>'), auto;
    }
    
    /* Hover Effects */
    .hover-lift {
        transition: all 0.3s ease;
    }
    
    .hover-lift:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.2);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .enhanced-header h1 {
            font-size: 3rem;
        }
        
        .pastel-card {
            padding: 2rem;
        }
        
        .interactive-button {
            padding: 1rem 2.5rem;
            font-size: 1.1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_enhanced_header():
    """Create a clear, crisp header with enhanced styling"""
    st.markdown("""
    <div class="enhanced-header">
        <h1>🧠 Sentixcare</h1>
        <p>Your Intelligent Mental Health & Wellness Companion</p>
        <p>Emotion Detection • Music Therapy • Wellness Support</p>
    </div>
    """, unsafe_allow_html=True)

def create_soothing_navigation():
    """Create soothing navigation with pastel colors"""
    st.markdown("""
    <div class="pastel-card">
        <h2 style="text-align: center; margin: 0; color: #667eea; font-size: 2.8rem; font-weight: 700;">🎯 How would you like to start?</h2>
        <p style="text-align: center; margin: 1.5rem 0 0 0; color: #666; font-size: 1.3rem; font-weight: 400;">Select your preferred method to begin your wellness journey</p>
    </div>
    """, unsafe_allow_html=True)

def create_soothing_section(title: str, description: str = "", color_class: str = "pastel-blue"):
    """Create a soothing section with pastel colors"""
    if description:
        st.markdown(f"""
        <div class="pastel-card {color_class}">
            <h2 style="color: #667eea; margin: 0 0 1.5rem 0; font-size: 2.4rem; font-weight: 700;">{title}</h2>
            <p style="color: #666; margin: 0; font-size: 1.2rem; font-weight: 400; line-height: 1.6;">{description}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="pastel-card {color_class}">
            <h2 style="color: #667eea; margin: 0; font-size: 2.4rem; font-weight: 700;">{title}</h2>
        </div>
        """, unsafe_allow_html=True)

def create_enhanced_footer():
    """Create an enhanced, soothing footer"""
    st.markdown("""
    <div style="text-align: center; padding: 4rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 30px; margin-top: 4rem; box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4); position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%, rgba(255,255,255,0.1) 100%); animation: shimmer 4s ease-in-out infinite;"></div>
        <h3 style="color: white; margin: 0 0 1.5rem 0; font-size: 2.2rem; font-weight: 700; position: relative; z-index: 2;">🧠 Sentixcare - Professional Edition</h3>
        <p style="color: white; margin: 0 0 1rem 0; opacity: 0.95; font-size: 1.3rem; font-weight: 400; position: relative; z-index: 2;">Powered by Advanced AI • Built for Mental Health & Wellness</p>
        <p style="color: white; margin: 0; opacity: 0.8; font-size: 1rem; position: relative; z-index: 2;">© 2026 Sentixcare. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

def apply_chat_styling():
    """Apply modern chat UI styling targeting native Streamlit chat components"""
    st.markdown("""
    <style>
    /* Chat Container General Styling */
    [data-testid="stChatMessageContent"] {
        padding: 15px 20px !important;
        border-radius: 20px;
        font-size: 15px;
        line-height: 1.6 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        max-width: 100% !important;
        max-height: none !important;
        hyphens: auto;
    }
    
    /* Native Chat Box */
    [data-testid="stChatMessage"] {
        background: rgba(30, 41, 59, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease;
    }
    
    [data-testid="stChatMessage"]:hover {
        transform: translateY(-2px);
    }
    
    /* Style the Avatar Backgrounds */
    [data-testid="stChatMessageAvatar"] {
        background: transparent !important;
        font-size: 24px;
        border-radius: 50%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    /* Input Box Styling */
    [data-testid="stChatInput"] {
        border-radius: 25px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        background: rgba(15, 23, 42, 0.8) !important;
        padding-left: 10px;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }

    /* Welcome Message - Dark Theme */
    .welcome-message {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 24px;
        border-radius: 16px;
        color: #e2e8f0;
        margin-bottom: 25px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
    
    .welcome-message h4 {
        margin: 0 0 10px 0;
        font-size: 1.4rem;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .welcome-message p {
        margin: 0;
        font-size: 15px;
        color: rgba(255, 255, 255, 0.85);
        line-height: 1.6;
    }

    /* Coping Strategies */
    .coping-strategies {
        background: rgba(30, 41, 59, 0.6);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .coping-strategies li {
        margin: 10px 0;
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)
