import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
SPOTIFY_CLIENT_ID = "SPOTIFY_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "SPOTIFY_CLIENT_SECRET"
date = input("Which Day you want to travel (After 2022-02-19)?\nType the Date in This Format YYYY-MM-YY format: ")
response = requests.get(f"https://www.billboard.com/charts/india-songs-hotw/{date}/")
# response = requests.get(f"https://www.billboard.com/charts/india-songs-hotw/2024-08-09/")
y_hacker_news = response.text

soup = BeautifulSoup(y_hacker_news, "html.parser")
all_headings = soup.find_all(name="h3")
raw_names = [song.getText() for song in all_headings]
song_names = [element.replace('\n', '').replace('\t', '').strip() for element in raw_names if element.strip()][3:28]

# print(song_names)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="315hbnumxznfoqzoaykkkunsywre", 
    )
)
user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
song_names = ["The list of song", "titles from your", "web scrape"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        print(f"{song} added Successfully")
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Favourite 25", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
