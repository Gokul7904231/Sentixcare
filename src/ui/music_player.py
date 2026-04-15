"""
YouTube Music Player Component
Provides embedded YouTube player with session_state-persistent playback.
Play button sets session_state.current_track — player renders from state.
No st.rerun() needed for play/stop/next/prev.
"""

import streamlit as st
import urllib.parse
from typing import List, Dict

def play_track(track: Dict):
    """Set a track as currently playing via session_state."""
    st.session_state.current_track = track
    st.session_state.setdefault("current_track_index", 0)
    if 'playlist' in st.session_state:
        for i, t in enumerate(st.session_state.playlist):
            if t.get('title') == track.get('title') and t.get('artist') == track.get('artist'):
                st.session_state.current_track_index = i
                break


def play_next_track():
    """Advance to next track in playlist via session_state."""
    playlist = st.session_state.get('playlist', [])
    if not playlist:
        return
        
    idx = st.session_state.get('current_track_index', -1)
    next_idx = (idx + 1) % len(playlist)
    st.session_state.current_track = playlist[next_idx]
    st.session_state.current_track_index = next_idx


def play_previous_track():
    """Go to previous track in playlist via session_state."""
    playlist = st.session_state.get('playlist', [])
    if not playlist:
        return
        
    idx = st.session_state.get('current_track_index', 0)
    prev_idx = (idx - 1) % len(playlist)
    st.session_state.current_track = playlist[prev_idx]
    st.session_state.current_track_index = prev_idx


# ===================================================
# Main display functions
# ===================================================

def display_music_recommendations(recommendations: List[Dict], title: str = "🎵 Music Recommendations"):
    """Display music recommendations with YouTube players."""
    if not st.session_state.get("playlist"):
        st.session_state.playlist = recommendations
    st.subheader(title)

    if not recommendations:
        st.warning("No music recommendations available")
        return

    tabs = st.tabs([f"🎵 {i+1}" for i in range(len(recommendations))])

    for i, (tab, rec) in enumerate(zip(tabs, recommendations)):
        with tab:
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
                    <h3 style="margin: 0; color: white;">{rec['title']}</h3>
                    <p style="margin: 5px 0; color: #f0f0f0;">by {rec['artist']}</p>
                    {f'<p style="margin: 5px 0; color: #e0e0e0;">Emotion: {rec.get("emotion", "N/A").title()} ({rec.get("percentage", 0):.1f}%)</p>' if "emotion" in rec else ''}
                </div>
                """, unsafe_allow_html=True)

                youtube_id = rec.get('youtube_id')
                if youtube_id:
                    thumbnail = f"https://img.youtube.com/vi/{youtube_id}/0.jpg"
                    st.image(thumbnail, use_container_width=True)

            with col2:
                st.markdown("**📊 Track Details:**")
                st.markdown(f"**Title:** {rec['title']}")
                st.markdown(f"**Artist:** {rec['artist']}")

                if 'emotion' in rec:
                    st.markdown(f"**Emotion:** {rec['emotion'].title()}")
                    st.markdown(f"**Confidence:** {rec['percentage']:.1f}%")

                if 'spotify_url' in rec:
                    st.markdown(f"[🎧 Listen on Spotify]({rec['spotify_url']})")

                if 'album_cover' in rec and rec['album_cover']:
                    st.image(rec['album_cover'], width=150)


def display_enhanced_music_recommendations(
    recommendations: List[Dict], emotion: str,
    title: str = "🎵 Enhanced Music Recommendations",
):
    """Display enhanced music recommendations with mood matching scores."""
    if not st.session_state.get("playlist"):
        st.session_state.playlist = recommendations
    st.subheader(title)

    if not recommendations:
        st.warning("No music recommendations available")
        return

    # Emotion header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {recommendations[0].get('emotion_color', '#667eea')} 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0; color: white;">🎭 {emotion.title()} Mood Music</h3>
        <p style="margin: 5px 0; color: #f0f0f0;">Perfectly matched songs for your emotional state</p>
    </div>
    """, unsafe_allow_html=True)

    # Persistent player — show current track at the top if one is selected
    if "player_container" not in st.session_state:
        st.session_state.player_container = st.empty()
        
    if st.session_state.get("current_track"):
        with st.session_state.player_container:
            _render_now_playing(st.session_state.current_track)

    # Song list
    for i, rec in enumerate(recommendations):
        with st.expander(f"🎵 {i+1}. {rec['title']} by {rec['artist']}", expanded=(i == 0)):
            col1, col2 = st.columns([3, 1])

            with col1:
                match_score = rec.get('mood_match_score', 85)
                score_color = (
                    "#4CAF50" if match_score >= 80
                    else "#FF9800" if match_score >= 60
                    else "#F44336"
                )
                st.markdown(f"""
                <div style="background: {score_color}; color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <strong>🎯 Mood Match: {match_score:.1f}%</strong>
                </div>
                """, unsafe_allow_html=True)

                if 'tempo_range' in rec:
                    st.markdown(f"**🎼 Tempo Range:** {rec['tempo_range'][0]}-{rec['tempo_range'][1]} BPM")
                if 'energy_level' in rec:
                    st.markdown(f"**⚡ Energy Level:** {rec['energy_level']}/10")
                if 'mood_keywords' in rec:
                    keywords = ", ".join(rec['mood_keywords'][:3])
                    st.markdown(f"**🏷️ Mood:** {keywords}")

            with col2:
                search_query = urllib.parse.quote(f"{rec['title']} {rec['artist']} audio")
                youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
                st.link_button("▶️ Play on YouTube", url=youtube_url, use_container_width=True)

            # Details section — use expander instead of button to avoid reruns
            with st.expander("📊 Detailed Analysis"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Musical Characteristics:**")
                    if 'tempo_range' in rec:
                        st.markdown(f"• Tempo: {rec['tempo_range'][0]}-{rec['tempo_range'][1]} BPM")
                    if 'energy_level' in rec:
                        st.markdown(f"• Energy: {rec['energy_level']}/10")
                    if 'valence_score' in rec:
                        st.markdown(f"• Positivity: {rec['valence_score']}/10")
                with col_b:
                    st.markdown("**Mood Matching:**")
                    st.markdown(f"• Match Score: {match_score:.1f}%")
                    if 'visual_style' in rec:
                        styles = ", ".join(rec['visual_style'])
                        st.markdown(f"• Visual Style: {styles}")


def display_mood_journey_playlist(playlist: List[Dict], emotion_summary: str):
    """Display a mood journey playlist with emotional flow visualization."""
    st.subheader("🎭 Your Emotional Music Journey")

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0; color: white;">🎵 Mood Journey Playlist</h3>
        <p style="margin: 5px 0; color: #f0f0f0;">{emotion_summary}</p>
        <p style="margin: 5px 0; color: #f0f0f0;">📊 {len(playlist)} songs • 🎯 Personalized emotional flow</p>
    </div>
    """, unsafe_allow_html=True)

    # Emotion flow visualization
    emotion_colors = {
        'happy': '#FFD700', 'sad': '#4169E1', 'anger': '#DC143C',
        'fear': '#8B008B', 'surprise': '#FF6347', 'disgust': '#228B22',
        'contempt': '#696969', 'neutral': '#708090',
    }

    emotion_groups = {}
    for song in playlist:
        emo = song.get('emotion', 'unknown')
        emotion_groups.setdefault(emo, []).append(song)

    st.markdown("### 🌊 Emotional Flow")
    flow_html = '<div style="display: flex; gap: 10px; margin: 20px 0; flex-wrap: wrap;">'
    for emotion, songs in emotion_groups.items():
        color = emotion_colors.get(emotion, '#708090')
        pct = songs[0].get('emotion_percentage', 0)
        flow_html += f'''
        <div style="background: {color}; color: white; padding: 10px 15px; border-radius: 20px; 
                    text-align: center; min-width: 100px;">
            <strong>{emotion.title()}</strong><br>
            <small>{len(songs)} songs ({pct:.1f}%)</small>
        </div>
        '''
    flow_html += '</div>'
    st.markdown(flow_html, unsafe_allow_html=True)

    # Persistent player
    if "player_container" not in st.session_state:
        st.session_state.player_container = st.empty()
        
    if st.session_state.get("current_track"):
        with st.session_state.player_container:
            _render_now_playing(st.session_state.current_track)

    # Song list
    st.markdown("### 🎵 Playlist")
    for i, song in enumerate(playlist):
        emotion = song.get('emotion', 'unknown')
        color = emotion_colors.get(emotion, '#708090')

        with st.expander(f"🎵 {i+1}. {song['title']} by {song['artist']} ({emotion.title()})", expanded=(i == 0)):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"""
                <div style="background: {color}; color: white; padding: 8px; border-radius: 5px; 
                            display: inline-block; margin-bottom: 10px;">
                    <strong>🎭 {emotion.title()}</strong>
                </div>
                """, unsafe_allow_html=True)
                match_score = song.get('mood_match_score', 85)
                st.markdown(f"**🎯 Mood Match:** {match_score:.1f}%")

            with col2:
                search_query = urllib.parse.quote(f"{song['title']} {song['artist']} audio")
                youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
                st.link_button("▶️ Play on YouTube", url=youtube_url, use_container_width=True)

            # Details via expander — no rerun
            with st.expander("📊 Song Info"):
                st.markdown(f"• Emotion: {emotion.title()}")
                st.markdown(f"• Match Score: {match_score:.1f}%")
                if 'tempo_range' in song:
                    st.markdown(f"• Tempo: {song['tempo_range'][0]}-{song['tempo_range'][1]} BPM")
                if 'energy_level' in song:
                    st.markdown(f"• Energy: {song['energy_level']}/10")


# ===================================================
# Player components
# ===================================================

def _render_now_playing(track: Dict):
    """Render the persistent now-playing player from session_state."""
    if not track or 'youtube_id' not in track:
        return

    st.markdown("### 🎵 Now Playing")
    st.markdown(f"**{track['title']}** by {track['artist']}")
    st.caption("🎧 Your selected track is playing below")

    # st.video is more stable than components.iframe across Streamlit reruns
    youtube_id = track.get('youtube_id')
    if youtube_id:
        st.video(f"https://www.youtube.com/watch?v={youtube_id}")

    # Controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⏮️ Previous", key="player_prev"):
            play_previous_track()
    with col2:
        if st.button("⏹️ Stop", key="player_stop"):
            st.session_state.current_track = None
    with col3:
        if st.button("⏭️ Next", key="player_next"):
            play_next_track()

    # Fallback links
    st.markdown("---")
    yt_url = f"https://www.youtube.com/watch?v={track['youtube_id']}"
    ytm_url = f"https://music.youtube.com/watch?v={track['youtube_id']}"
    st.markdown(f"[🎵 Open in YouTube]({yt_url}) · [📱 Open in YouTube Music]({ytm_url})")


def display_playlist_summary(playlist: List[Dict], emotion_summary: str):
    """Display playlist summary with emotion analysis."""
    st.markdown("---")
    st.subheader("🎭 Your Mood Analysis")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
            <h3 style="margin: 0; color: white;">{emotion_summary}</h3>
            <p style="margin: 10px 0; color: #f0f0f0;">Based on your facial expressions, here are personalized music recommendations:</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.metric("Total Songs", len(playlist))
        st.metric("Emotions Detected", len(set(r.get('emotion', 'unknown') for r in playlist)))


def create_music_player_sidebar():
    """Create a sidebar music player for continuous playback."""
    with st.sidebar:
        st.markdown("---")
        st.subheader("🎵 Now Playing")

        track = st.session_state.get('current_track')
        if track:
            st.markdown(f"""
            <div style="background: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                <h4 style="margin: 0; color: #262730;">{track['title']}</h4>
                <p style="margin: 5px 0; color: #666;">by {track['artist']}</p>
            </div>
            """, unsafe_allow_html=True)

            youtube_id = track.get('youtube_id')
            if youtube_id:
                st.video(f"https://www.youtube.com/watch?v={youtube_id}")

            if st.button("🔄 Next Track", key="sidebar_next"):
                play_next_track()
        else:
            st.info("No track selected. Choose a song from the recommendations below!")
