import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- CONFIGURATION ---
TMDB_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5NmVhMWRkNjIzY2NkODJmYmEwYmVjZGFmZjZmODEwOCIsIm5iZiI6MTc3ODU4NjAwOS40NzUwMDAxLCJzdWIiOiI2YTAzMTE5OTdhNTNiM2NkZDljYWMwMjciLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.zetZ09cMaN4P67cgqhhajImY_9L9EwE46zrsljWgvNQ"
HEADERS = {"Authorization": f"Bearer {TMDB_TOKEN}", "accept": "application/json"}

# --- STYLING (The MovieBox UI) ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MovieBox Clone</title>
    <style>
        body { background: #0b0c0e; color: white; font-family: sans-serif; margin: 0; padding: 0; }
        .sidebar { width: 200px; position: fixed; height: 100%; background: #12151a; padding: 20px; border-right: 1px solid #1a1e24; }
        .main { margin-left: 240px; padding: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 20px; }
        .card { text-decoration: none; color: white; transition: 0.2s; }
        .card:hover { transform: scale(1.05); }
        .poster { width: 100%; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        .player-container { width: 100%; height: 500px; background: #000; border-radius: 15px; margin-bottom: 30px; }
        iframe { width: 100%; height: 100%; border: none; border-radius: 15px; }
        .watch-btn { display: inline-block; background: #00dd82; color: #000; padding: 12px 25px; border-radius: 25px; text-decoration: none; font-weight: bold; margin-top: 15px; }
        @media (max-width: 768px) { .sidebar { display: none; } .main { margin-left: 0; } }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2 style="color:#00dd82">MovieBox</h2>
        <p><a href="/" style="color:white;text-decoration:none">🏠 Home</a></p>
    </div>
    <div class="main">
        {{ content | safe }}
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    url = "https://themoviedb.org"
    data = requests.get(url, headers=HEADERS).json().get('results', [])
    
    grid_html = '<h2>Trending Now</h2><div class="grid">'
    for m in data:
        poster = f"https://tmdb.org{m.get('poster_path')}"
        grid_html += f'<a href="/watch/{m["id"]}" class="card"><img src="{poster}" class="poster"><div>{m["title"]}</div></a>'
    grid_html += '</div>'
    
    return render_template_string(HTML_LAYOUT, content=grid_html)

@app.route("/watch/<tmdb_id>")
def watch(tmdb_id):
    # Fetch details to get the IMDb ID automatically
    detail_url = f"https://themoviedb.org{tmdb_id}?append_to_response=external_ids"
    data = requests.get(detail_url, headers=HEADERS).json()
    imdb_id = data.get('external_ids', {}).get('imdb_id')
    
    player_html = ""
    if imdb_id:
        player_html = f'<div class="player-container"><iframe src="https://vidsrc.to{imdb_id}" allowfullscreen></iframe></div>'
    
    info_html = f"""
    {player_html}
    <h1>{data.get('title')}</h1>
    <p style="color:#a0a5b0">{data.get('overview')}</p>
    <a href="/" class="watch-btn">Back to Home</a>
    """
    return render_template_string(HTML_LAYOUT, content=info_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
