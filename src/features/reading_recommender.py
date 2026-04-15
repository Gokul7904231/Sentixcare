"""
Reading Recommender for AI MoodMate
Suggests articles, books, and reading materials based on detected emotions
"""

import random
import requests
import streamlit as st
from typing import Dict, List

@st.cache_data(ttl=600, show_spinner=False)
def fetch_devto_articles(tag, limit=4):
    """Fetches articles from Dev.to API with a strict timeout."""
    url = f"https://dev.to/api/articles?tag={tag}&per_page={limit}"
    try:
        response = requests.get(url, timeout=5) 
        response.raise_for_status()
        data = response.json() 
        
        mapped_articles = []
        for art in data: 
            mapped_articles.append({
                "title": art.get("title", "Wellness Article"),
                "description": (art.get("description", "")[:250] + "...") if art.get("description") else "Read more about this topic...",
                "url": art.get("url", "https://dev.to"), 
                "category": art.get("tag_list", ["wellness"])[0].title() if art.get("tag_list") else "Wellness",
                "reading_time": f"{art.get('reading_time_minutes', 5)} min read"
            })
        return mapped_articles
    except Exception as e:
        print(f"API Error: {e}") 
        return None

class ReadingRecommender:
    def __init__(self):
        # Map emotions to Dev.to tags
        self.emotion_tag_map = {
            "happy": "happiness",
            "sad": "mentalhealth",
            "anger": "mindfulness",
            "fear": "anxiety",
            "neutral": "productivity",
            "disgust": "selfcare",
            "surprise": "learning",
            "contempt": "communication"
        }
        # Your hardcoded mapping as backup
        self._hardcoded_backup = {

            "happy": {
                "articles": [
                    {
                        "title": "The Science of Happiness: 10 Proven Ways to Stay Happy",
                        "url": "https://www.psychologytoday.com/us/blog/what-mentally-strong-people-dont-do/201501/10-scientifically-proven-ways-stay-happy-all-time",
                        "description": "Discover scientifically-backed strategies to maintain happiness and positivity in your daily life.",
                        "reading_time": "8 min read",
                        "category": "Psychology & Wellness"
                    },
                    {
                        "title": "How to Cultivate Gratitude and Transform Your Life",
                        "url": "https://www.mindful.org/how-to-cultivate-gratitude/",
                        "description": "Learn the powerful practice of gratitude and how it can change your perspective on life.",
                        "reading_time": "6 min read",
                        "category": "Mindfulness"
                    },
                    {
                        "title": "The Art of Finding Joy in Simple Moments",
                        "url": "https://www.tinybuddha.com/blog/finding-joy-in-simple-moments/",
                        "description": "Explore how to find happiness in everyday moments and appreciate life's simple pleasures.",
                        "reading_time": "5 min read",
                        "category": "Lifestyle"
                    }
                ],
                "books": [
                    {
                        "title": "The Happiness Project",
                        "author": "Gretchen Rubin",
                        "url": "https://www.goodreads.com/book/show/6398634-the-happiness-project",
                        "description": "A year-long experiment in living happier, with practical tips and insights.",
                        "category": "Self-Help"
                    },
                    {
                        "title": "The Book of Joy",
                        "author": "Dalai Lama & Desmond Tutu",
                        "url": "https://www.goodreads.com/book/show/30753886-the-book-of-joy",
                        "description": "Two spiritual leaders share their wisdom on finding joy in difficult times.",
                        "category": "Spirituality"
                    }
                ],
                "stories": [
                    {
                        "title": "The Little Prince",
                        "author": "Antoine de Saint-Exupéry",
                        "url": "https://www.goodreads.com/book/show/157993.The_Little_Prince",
                        "description": "A timeless tale about love, friendship, and seeing the world through innocent eyes.",
                        "category": "Children's Literature"
                    }
                ]
            },
            
            "sad": {
                "articles": [
                    {
                        "title": "How to Cope with Sadness: A Guide to Emotional Healing",
                        "url": "https://www.helpguide.org/articles/depression/coping-with-depression.htm",
                        "description": "Practical strategies for dealing with sadness and moving toward emotional recovery.",
                        "reading_time": "10 min read",
                        "category": "Mental Health"
                    },
                    {
                        "title": "The Power of Self-Compassion During Difficult Times",
                        "url": "https://self-compassion.org/the-three-elements-of-self-compassion-2/",
                        "description": "Learn how to be kinder to yourself when you're going through tough times.",
                        "reading_time": "7 min read",
                        "category": "Self-Care"
                    },
                    {
                        "title": "Finding Hope When Everything Feels Hopeless",
                        "url": "https://www.psychologytoday.com/us/blog/the-squeaky-wheel/201507/7-ways-find-hope-when-you-feel-hopeless",
                        "description": "Discover ways to find hope and meaning even in your darkest moments.",
                        "reading_time": "8 min read",
                        "category": "Inspiration"
                    }
                ],
                "books": [
                    {
                        "title": "The Gifts of Imperfection",
                        "author": "Brené Brown",
                        "url": "https://www.goodreads.com/book/show/7015403-the-gifts-of-imperfection",
                        "description": "A guide to embracing your imperfections and living wholeheartedly.",
                        "category": "Self-Help"
                    },
                    {
                        "title": "When Things Fall Apart",
                        "author": "Pema Chödrön",
                        "url": "https://www.goodreads.com/book/show/25028.When_Things_Fall_Apart",
                        "description": "Wisdom for difficult times from a Buddhist perspective.",
                        "category": "Spirituality"
                    }
                ],
                "stories": [
                    {
                        "title": "The Alchemist",
                        "author": "Paulo Coelho",
                        "url": "https://www.goodreads.com/book/show/18144590-the-alchemist",
                        "description": "A beautiful story about following your dreams and finding your personal legend.",
                        "category": "Inspirational Fiction"
                    }
                ]
            },
            
            "angry": {
                "articles": [
                    {
                        "title": "How to Manage Anger: 10 Healthy Ways to Deal with Anger",
                        "url": "https://www.mayoclinic.org/healthy-lifestyle/adult-health/in-depth/anger-management/art-20045434",
                        "description": "Learn healthy techniques for managing and expressing anger constructively.",
                        "reading_time": "9 min read",
                        "category": "Mental Health"
                    },
                    {
                        "title": "The Art of Forgiveness: Letting Go of Resentment",
                        "url": "https://www.psychologytoday.com/us/blog/the-forgiving-life/201208/10-ways-become-more-forgiving",
                        "description": "Discover the healing power of forgiveness and how to release anger and resentment.",
                        "reading_time": "7 min read",
                        "category": "Personal Growth"
                    },
                    {
                        "title": "Mindfulness Techniques for Anger Management",
                        "url": "https://www.mindful.org/mindfulness-for-anger/",
                        "description": "Use mindfulness practices to respond to anger with awareness and compassion.",
                        "reading_time": "6 min read",
                        "category": "Mindfulness"
                    }
                ],
                "books": [
                    {
                        "title": "Anger: Wisdom for Cooling the Flames",
                        "author": "Thich Nhat Hanh",
                        "url": "https://www.goodreads.com/book/show/17690.Anger",
                        "description": "Buddhist wisdom for transforming anger into understanding and compassion.",
                        "category": "Spirituality"
                    },
                    {
                        "title": "The Dance of Anger",
                        "author": "Harriet Lerner",
                        "url": "https://www.goodreads.com/book/show/17691.The_Dance_of_Anger",
                        "description": "A woman's guide to changing the patterns of intimate relationships.",
                        "category": "Psychology"
                    }
                ],
                "stories": [
                    {
                        "title": "To Kill a Mockingbird",
                        "author": "Harper Lee",
                        "url": "https://www.goodreads.com/book/show/2657.To_Kill_a_Mockingbird",
                        "description": "A powerful story about justice, empathy, and standing up for what's right.",
                        "category": "Classic Literature"
                    }
                ]
            },
            
            "fear": {
                "articles": [
                    {
                        "title": "How to Overcome Fear: 10 Strategies for Facing Your Fears",
                        "url": "https://www.psychologytoday.com/us/blog/here-there-and-everywhere/201701/10-ways-overcome-your-fears",
                        "description": "Practical strategies for confronting and overcoming your fears.",
                        "reading_time": "8 min read",
                        "category": "Personal Growth"
                    },
                    {
                        "title": "The Courage to Be Vulnerable: Embracing Uncertainty",
                        "url": "https://www.ted.com/talks/brene_brown_the_power_of_vulnerability",
                        "description": "Learn how vulnerability can be a source of strength and connection.",
                        "reading_time": "20 min watch",
                        "category": "TED Talk"
                    },
                    {
                        "title": "Mindfulness for Anxiety: Finding Peace in the Present",
                        "url": "https://www.mindful.org/mindfulness-for-anxiety/",
                        "description": "Use mindfulness techniques to manage anxiety and find calm.",
                        "reading_time": "7 min read",
                        "category": "Mindfulness"
                    }
                ],
                "books": [
                    {
                        "title": "Feel the Fear and Do It Anyway",
                        "author": "Susan Jeffers",
                        "url": "https://www.goodreads.com/book/show/17690.Feel_the_Fear_and_Do_It_Anyway",
                        "description": "A practical guide to overcoming fear and taking action in your life.",
                        "category": "Self-Help"
                    },
                    {
                        "title": "Daring Greatly",
                        "author": "Brené Brown",
                        "url": "https://www.goodreads.com/book/show/13588356-daring-greatly",
                        "description": "How the courage to be vulnerable transforms the way we live, love, and lead.",
                        "category": "Personal Development"
                    }
                ],
                "stories": [
                    {
                        "title": "The Hobbit",
                        "author": "J.R.R. Tolkien",
                        "url": "https://www.goodreads.com/book/show/5907.The_Hobbit",
                        "description": "A tale of an ordinary person who discovers courage within himself.",
                        "category": "Fantasy"
                    }
                ]
            },
            
            "surprise": {
                "articles": [
                    {
                        "title": "The Science of Surprise: How Unexpected Events Shape Our Lives",
                        "url": "https://www.psychologytoday.com/us/blog/the-science-wonder/201801/the-science-surprise",
                        "description": "Explore how surprise and wonder can enhance our lives and creativity.",
                        "reading_time": "6 min read",
                        "category": "Psychology"
                    },
                    {
                        "title": "Embracing the Unexpected: Finding Joy in Life's Surprises",
                        "url": "https://www.tinybuddha.com/blog/embracing-the-unexpected-finding-joy-in-lifes-surprises/",
                        "description": "Learn to welcome life's surprises and find meaning in unexpected moments.",
                        "reading_time": "5 min read",
                        "category": "Lifestyle"
                    }
                ],
                "books": [
                    {
                        "title": "The Surprise of a Lifetime",
                        "author": "Various Authors",
                        "url": "https://www.goodreads.com/book/show/collection/12345",
                        "description": "A collection of stories about life's most surprising and meaningful moments.",
                        "category": "Short Stories"
                    }
                ],
                "stories": [
                    {
                        "title": "The Secret Garden",
                        "author": "Frances Hodgson Burnett",
                        "url": "https://www.goodreads.com/book/show/2998.The_Secret_Garden",
                        "description": "A magical story about discovery, healing, and the power of nature.",
                        "category": "Children's Literature"
                    }
                ]
            },
            
            "disgust": {
                "articles": [
                    {
                        "title": "Understanding Disgust: The Emotion That Protects Us",
                        "url": "https://www.psychologytoday.com/us/blog/hot-thought/201411/understanding-disgust-the-emotion-protects-us",
                        "description": "Learn about the evolutionary purpose of disgust and how to manage it healthily.",
                        "reading_time": "7 min read",
                        "category": "Psychology"
                    },
                    {
                        "title": "Finding Beauty in Unexpected Places",
                        "url": "https://www.mindful.org/finding-beauty-in-unexpected-places/",
                        "description": "Discover how to find beauty and meaning even in difficult or unpleasant situations.",
                        "reading_time": "6 min read",
                        "category": "Mindfulness"
                    }
                ],
                "books": [
                    {
                        "title": "The Beauty of the Beast",
                        "author": "Various Authors",
                        "url": "https://www.goodreads.com/book/show/collection/12346",
                        "description": "Stories that find beauty and meaning in unexpected places.",
                        "category": "Literature"
                    }
                ],
                "stories": [
                    {
                        "title": "Beauty and the Beast",
                        "author": "Various",
                        "url": "https://www.goodreads.com/book/show/4144.Beauty_and_the_Beast",
                        "description": "A timeless tale about looking beyond appearances to find true beauty.",
                        "category": "Fairy Tale"
                    }
                ]
            }
        }
    
    def get_reading_recommendations(self, emotion: str, num_recommendations: int = 3) -> Dict:
        """Get reading recommendations for a specific emotion"""
        clean_emotion = emotion.lower()
        
        tag = self.emotion_tag_map.get(clean_emotion, "wellness")
        
        # Start with hardcoded backup
        recommendations = self._hardcoded_backup.get(clean_emotion, {}).copy()
        
        # Try API articles
        api_articles = fetch_devto_articles(tag, num_recommendations)
        
        if api_articles:
            recommendations["articles"] = api_articles
        elif "articles" not in recommendations:
            recommendations["articles"] = []
            
        # Random sample if too many
        if "articles" in recommendations and len(recommendations["articles"]) > num_recommendations:
            recommendations["articles"] = random.sample(recommendations["articles"], num_recommendations)
            
        # Add total
        recommendations["total_recommendations"] = len(recommendations.get("articles", [])) + len(recommendations.get("books", [])) + len(recommendations.get("stories", []))
        recommendations["emotion"] = clean_emotion
            
        return recommendations

    def _get_default_recommendations(self) -> Dict:
        """Default recommendations for unknown emotions"""
        return self.get_reading_recommendations("neutral")
    
    def _get_default_recommendations(self) -> Dict:
        """Default recommendations for unknown emotions"""
        return {
            "emotion": "general",
            "articles": [
                {
                    "title": "The Power of Positive Thinking",
                    "url": "https://www.psychologytoday.com/us/blog/what-mentally-strong-people-dont-do/201501/10-scientifically-proven-ways-stay-happy-all-time",
                    "description": "Discover the benefits of positive thinking and how to cultivate optimism.",
                    "reading_time": "7 min read",
                    "category": "Self-Help"
                }
            ],
            "books": [
                {
                    "title": "The Power of Now",
                    "author": "Eckhart Tolle",
                    "url": "https://www.goodreads.com/book/show/6708.The_Power_of_Now",
                    "description": "A guide to spiritual enlightenment and living in the present moment.",
                    "category": "Spirituality"
                }
            ],
            "stories": [
                {
                    "title": "The Little Prince",
                    "author": "Antoine de Saint-Exupéry",
                    "url": "https://www.goodreads.com/book/show/157993.The_Little_Prince",
                    "description": "A timeless tale about love, friendship, and seeing the world through innocent eyes.",
                    "category": "Children's Literature"
                }
            ],
            "total_recommendations": 3
        }
    
    def get_mood_improvement_reading(self, emotion: str) -> Dict:
        """Get reading materials specifically for mood improvement"""
        mood_improvement_map = {
            "sad": "happy",
            "angry": "calm",
            "fear": "courage",
            "disgust": "beauty",
            "surprise": "wonder"
        }
        
        target_emotion = mood_improvement_map.get(emotion.lower(), "happy")
        return self.get_reading_recommendations(target_emotion, 2)

# Create global instance
reading_recommender = ReadingRecommender()
