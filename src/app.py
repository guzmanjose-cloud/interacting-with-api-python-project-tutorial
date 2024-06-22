import os
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt

# load the .env file variables
load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")


con = spotipy.Spotify(auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Fetch the top tracks for the artist (replace the artist_id with the correct one)
artist_id = "3JFsVIxOn7STeilPICkkB2"
response = con.artist_top_tracks(artist_id)

# Extract track IDs
track_ids = [track['id'] for track in response['tracks'][:10]]

# Fetch detailed track information
tracks_info = con.tracks(track_ids)

# Process the track information into a DataFrame
top_tracks = [{
    'name': track['name'],
    'popularity': track['popularity'],
    'album': track['album']['name'],
    'release_date': track['album']['release_date'],
    'duration_ms': track['duration_ms'],
    'preview_url': track['preview_url']
} for track in tracks_info['tracks']]

df = pd.DataFrame(top_tracks)

# Convert duration from milliseconds to minutes for easier interpretation
df['duration_minutes'] = df['duration_ms'] / 60000

# Print the DataFrame
print(df)

# Plot a scatter plot to visualize the relationship between duration and popularity
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='duration_minutes', y='popularity')
plt.title('Relationship between Track Duration and Popularity')
plt.xlabel('Duration (minutes)')
plt.ylabel('Popularity')
plt.grid(True)
plt.show()
