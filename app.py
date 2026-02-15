import os
import json
import urllib.parse
import requests
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# -----------------------------
# Setup
# -----------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Playlist Generator", page_icon="🪩", layout="centered")


def get_taylor_thumbnail_url():
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/Taylor_Swift"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        return data.get("thumbnail", {}).get("source")
    except Exception:
        return None


def spotify_search_url(title: str, artist: str) -> str:
    q = f"{title} {artist}".strip()
    return "https://open.spotify.com/search/" + urllib.parse.quote(q)


def apply_eras_theme(mood: str, era: str):
    era_palettes = {
        "Default": ("#ff4fb3", "#ffd6ff", "#0b0b12"),
        "Showgirl 🪩✨": ("#ff4fb3", "#ffd6ff", "#06060e"),
        "TTPD 🩶": ("#cfcfcf", "#ffffff", "#0a0a0b"),
        "Midnights 💙": ("#6b7bff", "#c6d0ff", "#07091a"),
        "Lover 🩷": ("#ff4fb3", "#ffb3d9", "#0b0610"),
        "Reputation 🖤": ("#b8ff6a", "#ffffff", "#07070b"),
        "1989 🩵": ("#35d0ff", "#b8f3ff", "#061018"),
        "Red ❤️": ("#ff3b3b", "#ffd0d0", "#12060a"),
        "Folklore 🤍": ("#d9d9d9", "#ffffff", "#0a0a0d"),
        "Evermore 🤎": ("#c58b5a", "#ffe0c7", "#0d0806"),
    }

    accent, accent2, bg = era_palettes.get(era, era_palettes["Default"])

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
              radial-gradient(circle at 18% 18%, {accent}33 0%, transparent 42%),
              radial-gradient(circle at 82% 24%, {accent2}22 0%, transparent 40%),
              linear-gradient(180deg, {bg} 0%, #04040a 100%);
        }}

        .stButton>button {{
            background: linear-gradient(90deg, {accent} 0%, {accent2} 55%, {accent} 100%);
            color: white;
            border-radius: 999px;
            font-weight: bold;
            border: none;
        }}

        h1 {{
            text-shadow: 0 0 18px {accent}88;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def safe_parse_json(text: str):
    """
    Extract JSON safely even if extra text is returned.
    """
    start = text.find("{")
    end = text.rfind("}") + 1

    if start != -1 and end != -1:
        text = text[start:end]

    return json.loads(text)


def generate_playlist(payload: dict) -> dict:
    system = (
        "You are a music curator. Create playlists that match the user's mood, activity, energy, and aesthetic.\n"
        "Return strictly valid JSON with keys: playlist_title, vibe_summary, tags, songs.\n"
        "songs must be a list of objects with keys: title, artist, reason.\n"
        "reason should be 1-2 short sentences."
    )

    prompt = (
        "Create a playlist.\n"
        "- Avoid repeating artists too much.\n"
        "- If explicit_ok is false, avoid explicit songs.\n"
        "- If taylor_inspired is true, include some Taylor Swift songs but not all.\n"
        "- Make the playlist title short and aesthetic.\n"
        "Return JSON only.\n\n"
        f"User request:\n{json.dumps(payload, indent=2)}"
    )

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
    )

    text = resp.choices[0].message.content.strip()
    return safe_parse_json(text)


# -----------------------------
# UI
# -----------------------------
st.title("🪩✨ AI Playlist Generator")

colA, colB = st.columns(2)
with colA:
    mood = st.selectbox("Mood", ["Confident", "Happy", "Chill", "Focused", "Romantic", "Sad", "Hyped"])
with colB:
    era = st.selectbox(
        "Era",
        [
            "Default",
            "Showgirl 🪩✨",
            "TTPD 🩶",
            "Midnights 💙",
            "Lover 🩷",
            "Reputation 🖤",
            "1989 🩵",
            "Red ❤️",
            "Folklore 🤍",
            "Evermore 🤎",
        ],
    )

apply_eras_theme(mood, era)

activity = st.selectbox("Activity", ["Running", "Driving", "Getting Ready", "Studying", "Gym"])
energy = st.radio("Energy", ["Low", "Medium", "High"], horizontal=True)

taylor_mode = st.toggle("Taylor Swift inspired", value=True)
explicit_ok = st.toggle("Allow explicit songs", value=False)

if taylor_mode or era != "Default":
    img = get_taylor_thumbnail_url()
    if img:
        st.image(img, width=140)

notes = st.text_input("Optional vibe note")
num_songs = st.slider("Number of songs", 8, 20, 12)

st.divider()

if st.button("Generate playlist"):
    payload = {
        "mood": mood,
        "activity": activity,
        "energy": energy,
        "taylor_inspired": taylor_mode,
        "explicit_ok": explicit_ok,
        "vibe_note": notes,
        "num_songs": num_songs,
        "era": era,
    }

    with st.spinner("Curating your playlist..."):
        try:
            data = generate_playlist(payload)

            st.subheader(data.get("playlist_title", "Your Playlist"))
            st.write(data.get("vibe_summary", ""))

            for i, s in enumerate(data.get("songs", []), start=1):
                title = s.get("title", "")
                artist = s.get("artist", "")
                reason = s.get("reason", "")
                url = spotify_search_url(title, artist)

                st.markdown(
                    f"""
                    **{i}. {title} — {artist}**  
                    {reason}  
                    [🎧 Listen on Spotify]({url})
                    """
                )

        except Exception as e:
            st.error(f"Error: {e}")
