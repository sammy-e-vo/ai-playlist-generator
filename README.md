# AI Playlist Generator 🪩✨

A sparkly, Taylor-inspired AI playlist generator built with Streamlit.  
Generate playlists based on mood, activity, and energy, with themed vibes and Spotify links.

This project was built as a creative way to learn AI, APIs, and building small apps.

---

## Features
- Mood + activity + energy based playlists  
- Taylor-inspired vibe mode  
- Spotify links for every track  
- Themed UI with a fun aesthetic  
- Built with Python and Streamlit  

---

## Tech Stack
- Python  
- Streamlit  
- OpenAI API  

---

## Run Locally

Open Terminal and run:

```
git clone https://github.com/sammy-e-vo/ai-playlist-generator.git
cd ai-playlist-app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open your browser to:
http://localhost:8501

Before running the app, create a file named `.env` in the project folder and add:

```
OPENAI_API_KEY=your_key_here
```

---

## Project Structure

```
ai-playlist-app/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
```

---

## Notes
- The `.env` file is excluded from GitHub for security.
- This project is for learning and portfolio purposes.

---

## Future Improvements
- Spotify authentication and playlist export  
- More themes and visuals  
- Mood-based cover art  
- Deployment for public access  

---

## Author
Built by Sammy Vo