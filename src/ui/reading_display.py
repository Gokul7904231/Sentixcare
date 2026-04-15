"""
Reading Display Module for AI MoodMate
Handles the display of reading recommendations in the Streamlit app
"""

import streamlit as st
import urllib.parse
from typing import Dict, List

def display_reading_recommendations(recommendations: Dict, emotion: str, title: str = "📚 Reading Recommendations"):
    """Display reading recommendations in an organized and attractive way"""
    
    if not recommendations or recommendations.get("total_recommendations", 0) == 0:
        st.warning("No reading recommendations available for this emotion.")
        return
    
    st.markdown("---")
    st.subheader(title)
    st.markdown(f"*Curated reading materials to support your {emotion.title()} mood*")
    
    # Display articles
    if recommendations.get("articles"):
        st.markdown("### 📰 Articles & Quick Reads")
        
        for i, article in enumerate(recommendations["articles"]):
            with st.expander(f"📖 {article['title']}", expanded=False):
                st.markdown(f"**Description:** {article['description']}")
                st.markdown(f"**Category:** {article['category']}")
                st.markdown(f"**Reading Time:** {article.get('reading_time', 'N/A')}")
                
                # Add why this is recommended for this emotion
                st.markdown("---")
                st.markdown("### 🎯 Why This Article for Your Mood")
                st.markdown(get_article_reasoning(emotion, article))
                
                # Create clickable link
                st.markdown(f"[🔗 Read Article: {article['title']}]({article['url']})")
                
                # Add a button for easy access
                url = article.get('url', '')
                if 'dev.to' in url:
                    st.link_button(f"📖 Open Article", url=url, use_container_width=True)
                else:
                    title_query = urllib.parse.quote_plus(article.get('title', 'Mental Health Article'))
                    safe_url = f"https://www.google.com/search?q={title_query}"
                    st.link_button(f"📖 Open Article", url=safe_url, use_container_width=True)
                st.code(url or 'Fallback Google Search')
    
    # Display books
    if recommendations.get("books"):
        st.markdown("### 📚 Books for Deeper Reading")
        
        for i, book in enumerate(recommendations["books"]):
            with st.expander(f"📖 {book['title']} by {book['author']}", expanded=False):
                st.markdown(f"**Author:** {book['author']}")
                st.markdown(f"**Description:** {book['description']}")
                st.markdown(f"**Category:** {book['category']}")
                
                # Add why this is recommended for this emotion
                st.markdown("---")
                st.markdown("### 🎯 Why This Book for Your Mood")
                st.markdown(get_book_reasoning(emotion, book))
                
                # Create clickable link
                st.markdown(f"[🔗 View Book: {book['title']}]({book['url']})")
                
                # Add a button for easy access
                book_title = book.get('title', 'Recommended Reading')
                search_query = urllib.parse.quote_plus(book_title)
                safe_book_url = f"https://www.google.com/search?q={search_query}"
                st.link_button(f"📚 Open Book Page", url=safe_book_url, use_container_width=True)
    
    # Display stories
    if recommendations.get("stories"):
        st.markdown("### 📖 Inspiring Stories")
        
        for i, story in enumerate(recommendations["stories"]):
            with st.expander(f"📖 {story['title']} by {story['author']}", expanded=False):
                st.markdown(f"**Author:** {story['author']}")
                st.markdown(f"**Description:** {story['description']}")
                st.markdown(f"**Category:** {story['category']}")
                
                # Add why this is recommended for this emotion
                st.markdown("---")
                st.markdown("### 🎯 Why This Story for Your Mood")
                st.markdown(get_story_reasoning(emotion, story))
                
                # Create clickable link
                st.markdown(f"[🔗 View Story: {story['title']}]({story['url']})")
                
                # Add a button for easy access
                story_title = story.get('title', 'Inspiring Story')
                search_query = urllib.parse.quote_plus(story_title)
                safe_story_url = f"https://www.google.com/search?q={search_query}"
                st.link_button(f"📖 Open Story Page", url=safe_story_url, use_container_width=True)
    
    # Add summary
    st.markdown("---")
    st.info(f"💡 **Tip:** Reading can be a powerful tool for mood improvement. These recommendations are specifically curated to support your {emotion.title()} mood and help you find inspiration, comfort, or new perspectives.")

def get_article_reasoning(emotion: str, article: Dict) -> str:
    """Get reasoning for why this article is recommended for this emotion"""
    emotion = emotion.lower()
    title = article['title'].lower()
    
    reasoning_map = {
        "happy": {
            "happiness": "This article will help you understand the science behind happiness and provide practical strategies to maintain your positive mood. You'll learn evidence-based techniques to cultivate lasting joy and spread positivity to others.",
            "gratitude": "Gratitude is a powerful amplifier of happiness. This article will teach you how to recognize and appreciate the good in your life, which can deepen your current positive feelings and create a lasting foundation for well-being.",
            "joy": "This article will help you find joy in everyday moments and teach you to appreciate life's simple pleasures. It's perfect for maintaining your current happy state and discovering new sources of delight."
        },
        "sad": {
            "cope": "This article provides practical strategies for navigating difficult emotions. It will help you understand that sadness is a normal part of life and give you tools to process your feelings healthily and move toward healing.",
            "self-compassion": "When you're feeling sad, it's crucial to be kind to yourself. This article will teach you how to treat yourself with the same compassion you'd show a friend, which is essential for emotional recovery.",
            "hope": "This article will help you find light in dark times. It provides strategies for maintaining hope and finding meaning even when everything feels difficult, which can be transformative for your emotional well-being."
        },
        "angry": {
            "anger": "This article will help you understand anger as a normal emotion and provide healthy ways to express and manage it. You'll learn to channel your anger constructively rather than letting it control you.",
            "forgiveness": "Holding onto anger can be exhausting. This article will guide you through the process of forgiveness, which can free you from resentment and help you find peace and emotional freedom.",
            "mindfulness": "Mindfulness can help you respond to anger with awareness rather than reacting impulsively. This article will teach you techniques to pause, breathe, and choose your response thoughtfully."
        },
        "fear": {
            "overcome": "This article will help you understand that fear is often a signal for growth. You'll learn practical strategies to face your fears and discover that courage isn't the absence of fear, but action despite it.",
            "vulnerability": "This article will help you see vulnerability as a strength rather than a weakness. You'll learn how embracing uncertainty can lead to deeper connections and personal growth.",
            "anxiety": "This article provides mindfulness techniques specifically designed for anxiety. You'll learn to observe your anxious thoughts without being overwhelmed by them, creating space for calm and clarity."
        },
        "surprise": {
            "surprise": "This article will help you understand how surprise and wonder can enhance your life. You'll learn to embrace unexpected moments as opportunities for growth and discovery.",
            "unexpected": "This article will teach you to find joy and meaning in life's surprises. It's perfect for helping you navigate unexpected changes with curiosity and openness rather than resistance."
        },
        "disgust": {
            "disgust": "This article will help you understand disgust as a protective emotion and learn to manage it healthily. You'll discover how to process difficult feelings without being overwhelmed by them.",
            "beauty": "This article will help you find beauty in unexpected places. It's perfect for shifting your perspective and discovering wonder even in challenging situations."
        }
    }
    
    # Find matching reasoning
    for key, reasoning in reasoning_map.get(emotion, {}).items():
        if key in title:
            return reasoning
    
    # Default reasoning based on emotion
    default_reasoning = {
        "happy": "This article will help you maintain and deepen your positive mood. It provides practical insights and strategies to enhance your current state of happiness and well-being.",
        "sad": "This article will provide comfort and guidance during difficult times. It offers evidence-based strategies for emotional healing and finding hope in challenging moments.",
        "angry": "This article will help you process and manage your anger in healthy ways. It provides tools for emotional regulation and finding constructive outlets for your feelings.",
        "fear": "This article will help you understand and work with your fears. It offers strategies for building courage and finding strength in the face of uncertainty.",
        "surprise": "This article will help you embrace life's unexpected moments with curiosity and openness. It provides insights for finding meaning in surprising experiences.",
        "disgust": "This article will help you process difficult emotions and find new perspectives. It offers strategies for emotional regulation and finding beauty in challenging situations."
    }
    
    return default_reasoning.get(emotion, "This article is specifically chosen to support your current emotional state and provide valuable insights for your well-being.")

def get_book_reasoning(emotion: str, book: Dict) -> str:
    """Get reasoning for why this book is recommended for this emotion"""
    emotion = emotion.lower()
    title = book['title'].lower()
    
    reasoning_map = {
        "happy": {
            "happiness project": "This book will help you maintain your positive mood through practical experiments and insights. You'll learn to cultivate lasting happiness and discover what truly brings you joy in life.",
            "book of joy": "This book offers profound wisdom from two spiritual leaders on finding joy even in difficult times. It will deepen your understanding of happiness and provide timeless principles for well-being.",
            "power of now": "This book will help you stay present and appreciate the current moment, which is essential for maintaining happiness. You'll learn to find peace and joy in the here and now."
        },
        "sad": {
            "gifts of imperfection": "This book will help you embrace your authentic self and find strength in vulnerability. It's perfect for healing from sadness and learning to love yourself through difficult times.",
            "when things fall apart": "This book offers Buddhist wisdom for navigating difficult times. It will help you find peace and meaning even when everything feels uncertain or painful.",
            "alchemist": "This inspiring story will remind you that every challenge has a purpose and that your personal journey, no matter how difficult, can lead to transformation and fulfillment."
        },
        "angry": {
            "anger": "This book provides Buddhist wisdom for transforming anger into understanding and compassion. It will help you work with your anger skillfully and find peace within yourself.",
            "dance of anger": "This book will help you understand the patterns in your relationships and learn to express anger in ways that lead to positive change rather than conflict.",
            "daring greatly": "This book will help you understand vulnerability as a source of strength. It's perfect for learning to express difficult emotions like anger in healthy, constructive ways."
        },
        "fear": {
            "feel the fear": "This book will help you understand that fear is a normal part of growth. You'll learn practical strategies to take action despite fear and build confidence in your abilities.",
            "daring greatly": "This book will help you embrace vulnerability and find courage in the face of fear. It teaches that being brave doesn't mean being fearless, but acting despite fear.",
            "hobbit": "This story of an ordinary person discovering courage within themselves will inspire you to face your own fears. It shows that heroism comes from taking small, brave steps forward."
        },
        "surprise": {
            "secret garden": "This magical story about discovery and healing will help you embrace life's surprises with wonder and openness. It teaches that unexpected moments can lead to transformation and growth.",
            "little prince": "This timeless tale will help you see the world with fresh eyes and find meaning in unexpected places. It's perfect for embracing surprise and wonder in your daily life."
        },
        "disgust": {
            "beauty and the beast": "This classic tale will help you look beyond surface appearances to find true beauty and meaning. It's perfect for shifting your perspective and finding value in unexpected places.",
            "little prince": "This story will help you see the world with innocent eyes and find beauty in simple, unexpected places. It teaches that what matters most is often invisible to the eye."
        }
    }
    
    # Find matching reasoning
    for key, reasoning in reasoning_map.get(emotion, {}).items():
        if key in title:
            return reasoning
    
    # Default reasoning based on emotion
    default_reasoning = {
        "happy": "This book will help you maintain and deepen your positive mood. It provides timeless wisdom and practical strategies for cultivating lasting happiness and well-being.",
        "sad": "This book will provide comfort and guidance during difficult times. It offers profound insights for emotional healing and finding hope and meaning in challenging moments.",
        "angry": "This book will help you understand and transform your anger into positive energy. It provides wisdom and tools for emotional regulation and healthy expression of difficult feelings.",
        "fear": "This book will help you understand fear as a natural part of growth. It offers strategies for building courage and finding strength in the face of uncertainty and challenges.",
        "surprise": "This book will help you embrace life's unexpected moments with curiosity and wonder. It provides insights for finding meaning and growth in surprising experiences.",
        "disgust": "This book will help you process difficult emotions and find new perspectives. It offers wisdom for emotional regulation and discovering beauty in challenging situations."
    }
    
    return default_reasoning.get(emotion, "This book is specifically chosen to support your current emotional state and provide valuable insights for your personal growth and well-being.")

def get_story_reasoning(emotion: str, story: Dict) -> str:
    """Get reasoning for why this story is recommended for this emotion"""
    emotion = emotion.lower()
    title = story['title'].lower()
    
    reasoning_map = {
        "happy": {
            "little prince": "This beautiful story will deepen your appreciation for life's simple joys and remind you of what truly matters. It's perfect for maintaining your happy mood and spreading joy to others.",
            "secret garden": "This magical story about discovery and healing will inspire you to find wonder in everyday moments. It's perfect for maintaining your positive outlook and discovering new sources of happiness."
        },
        "sad": {
            "alchemist": "This inspiring story will remind you that every challenge has a purpose and that your personal journey can lead to transformation. It's perfect for finding hope and meaning during difficult times.",
            "little prince": "This touching story about love, friendship, and seeing the world through innocent eyes will provide comfort and remind you of life's simple beauties during difficult times."
        },
        "angry": {
            "to kill a mockingbird": "This powerful story about justice, empathy, and standing up for what's right will help you channel your anger into positive action. It teaches the importance of compassion and understanding.",
            "little prince": "This gentle story will help you see the world with fresh eyes and find peace in simple moments. It's perfect for calming anger and finding perspective on what truly matters."
        },
        "fear": {
            "hobbit": "This story of an ordinary person discovering courage within themselves will inspire you to face your own fears. It shows that heroism comes from taking small, brave steps forward despite uncertainty.",
            "little prince": "This story will help you see the world with wonder and curiosity, which can help transform fear into excitement about new possibilities and adventures."
        },
        "surprise": {
            "secret garden": "This magical story about discovery and healing will help you embrace life's surprises with wonder and openness. It teaches that unexpected moments can lead to transformation and growth.",
            "little prince": "This story will help you see the world with fresh eyes and find meaning in unexpected places. It's perfect for embracing surprise and wonder in your daily life."
        },
        "disgust": {
            "beauty and the beast": "This classic tale will help you look beyond surface appearances to find true beauty and meaning. It's perfect for shifting your perspective and finding value in unexpected places.",
            "little prince": "This story will help you see the world with innocent eyes and find beauty in simple, unexpected places. It teaches that what matters most is often invisible to the eye."
        }
    }
    
    # Find matching reasoning
    for key, reasoning in reasoning_map.get(emotion, {}).items():
        if key in title:
            return reasoning
    
    # Default reasoning based on emotion
    default_reasoning = {
        "happy": "This story will help you maintain and deepen your positive mood. It provides inspiration and reminds you of life's simple joys and beautiful moments.",
        "sad": "This story will provide comfort and hope during difficult times. It offers inspiration and reminds you that even in dark moments, there is light and meaning to be found.",
        "angry": "This story will help you find perspective and peace. It provides inspiration for channeling difficult emotions into positive action and understanding.",
        "fear": "This story will inspire you to find courage and face your fears. It provides hope and shows that even ordinary people can discover extraordinary strength within themselves.",
        "surprise": "This story will help you embrace life's unexpected moments with wonder and curiosity. It provides inspiration for finding meaning and growth in surprising experiences.",
        "disgust": "This story will help you find new perspectives and discover beauty in unexpected places. It provides inspiration for seeing the world with fresh eyes and finding meaning in challenging situations."
    }
    
    return default_reasoning.get(emotion, "This story is specifically chosen to support your current emotional state and provide inspiration and comfort for your personal journey.")

def display_quick_reading_links(recommendations: Dict, emotion: str):
    """Display quick access links for reading recommendations"""
    
    if not recommendations:
        return
    
    st.markdown("### 📚 Quick Reading Links")
    
    # Create columns for different types of reading
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if recommendations.get("articles"):
            st.markdown("**📰 Articles**")
            for article in recommendations["articles"][:2]:  # Show max 2
                st.markdown(f"[{article['title'][:30]}...]({article['url']})")
    
    with col2:
        if recommendations.get("books"):
            st.markdown("**📚 Books**")
            for book in recommendations["books"][:2]:  # Show max 2
                st.markdown(f"[{book['title'][:30]}...]({book['url']})")
    
    with col3:
        if recommendations.get("stories"):
            st.markdown("**📖 Stories**")
            for story in recommendations["stories"][:2]:  # Show max 2
                st.markdown(f"[{story['title'][:30]}...]({story['url']})")

def display_reading_insights(emotion: str):
    """Display insights about reading and mood improvement"""
    
    insights = {
        "happy": "Reading uplifting content can help maintain your positive mood and inspire you to spread joy to others.",
        "sad": "Reading can provide comfort, new perspectives, and hope during difficult times. Stories of resilience can be particularly healing.",
        "angry": "Reading can help you process emotions, gain new perspectives, and find healthy ways to channel your energy.",
        "fear": "Reading about courage, facing challenges, and overcoming obstacles can help you build confidence and reduce anxiety.",
        "surprise": "Reading can help you embrace life's unexpected moments and find meaning in new experiences.",
        "disgust": "Reading can help you find beauty in unexpected places and develop a more compassionate perspective."
    }
    
    insight = insights.get(emotion.lower(), "Reading can be a powerful tool for emotional well-being and personal growth.")
    
    st.markdown("---")
    st.markdown("### 💡 Reading & Mood Insights")
    st.info(insight)

def create_reading_sidebar():
    """Create a sidebar with reading tips and quick access"""
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📚 Reading Tips")
        
        st.markdown("""
        **💡 Quick Tips:**
        - Set aside 10-15 minutes daily for reading
        - Choose materials that match your current mood
        - Keep a reading journal to track insights
        - Join online book clubs for community
        - Try audiobooks for busy schedules
        """)
        
        st.markdown("**🔗 Popular Reading Platforms:**")
        st.markdown("- [Goodreads](https://www.goodreads.com/)")
        st.markdown("- [Medium](https://medium.com/)")
        st.markdown("- [Project Gutenberg](https://www.gutenberg.org/)")
        st.markdown("- [TED Talks](https://www.ted.com/)")
